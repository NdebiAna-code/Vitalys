import os
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path

from flask import (Flask, render_template, request, redirect, url_for,
                   flash, abort)
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)
from werkzeug.utils import secure_filename

from models import db, User, Meal, WeightEntry, StepEntry
from data.gyms import all_gyms, total_count
from data.sport_programs import build_program, GOALS
from data.meal_plans import get_plan, all_plans

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTS = {"png", "jpg", "jpeg", "webp", "gif"}


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "dev-only-change-me")
    db_path = BASE_DIR / "data" / "app.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024  # 6MB

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Connecte-toi pour accéder à ton espace."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


def save_upload(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        return None
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    path = UPLOAD_DIR / name
    file_storage.save(path)
    return f"uploads/{name}"


def register_routes(app):

    @app.route("/")
    def home():
        return render_template("home.html", gym_count=total_count())

    # ---------------- AUTH ----------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""
            confirm = request.form.get("confirm") or ""
            if not email or not password:
                flash("Email et mot de passe requis.", "error")
                return render_template("auth/register.html")
            if password != confirm:
                flash("Les mots de passe ne correspondent pas.", "error")
                return render_template("auth/register.html")
            if len(password) < 6:
                flash("Le mot de passe doit faire au moins 6 caractères.", "error")
                return render_template("auth/register.html")
            if User.query.filter_by(email=email).first():
                flash("Un compte existe déjà avec cet email.", "error")
                return render_template("auth/register.html")
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Bienvenue ! Complète maintenant ton profil.", "success")
            return redirect(url_for("profile"))
        return render_template("auth/register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""
            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                flash("Identifiants incorrects.", "error")
                return render_template("auth/login.html")
            login_user(user, remember=True)
            return redirect(url_for("profile"))
        return render_template("auth/login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("À bientôt !", "info")
        return redirect(url_for("home"))

    # ---------------- PROFILE ----------------
    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        if request.method == "POST":
            try:
                current_user.first_name = (request.form.get("first_name") or "").strip()[:80]
                age = request.form.get("age")
                weight = request.form.get("weight")
                height = request.form.get("height")
                current_user.age = int(age) if age else None
                current_user.weight = float(weight) if weight else None
                current_user.height = float(height) if height else None
                requested_goal = request.form.get("goal")
                if requested_goal in GOALS:
                    if requested_goal not in current_user.allowed_goals:
                        flash("Avec un IMC inférieur à 18.5, la perte de poids n'est pas recommandée. Choisis prise de masse ou maintien.", "error")
                    else:
                        current_user.goal = requested_goal
                db.session.commit()
                flash("Profil mis à jour.", "success")
            except (TypeError, ValueError):
                db.session.rollback()
                flash("Valeurs invalides — vérifie age, poids et taille.", "error")
            return redirect(url_for("profile"))

        # Build week of meals (last 7 days)
        week_start = datetime.utcnow() - timedelta(days=7)
        week_meals = (Meal.query
                      .filter(Meal.user_id == current_user.id, Meal.eaten_at >= week_start)
                      .order_by(Meal.eaten_at.desc())
                      .all())
        weights = current_user.weight_entries[:12]
        steps = current_user.step_entries[:14]
        steps_today = next((s for s in steps if s.recorded_on == date.today()), None)
        return render_template(
            "profile.html",
            week_meals=week_meals,
            weights=list(reversed(weights)),
            steps=steps,
            steps_today=steps_today,
            goals=GOALS,
        )

    # ---------------- JOURNAL ACTIONS ----------------
    @app.route("/meals/add", methods=["POST"])
    @login_required
    def add_meal():
        name = (request.form.get("name") or "").strip()
        meal_type = (request.form.get("meal_type") or "").strip()[:50]
        notes = (request.form.get("notes") or "").strip()
        if not name:
            flash("Donne un nom à ton plat.", "error")
            return redirect(url_for("profile"))
        photo_path = save_upload(request.files.get("photo"))
        meal = Meal(user_id=current_user.id, name=name[:200],
                    meal_type=meal_type, notes=notes, photo=photo_path)
        db.session.add(meal)
        db.session.commit()
        flash("Repas enregistré.", "success")
        return redirect(url_for("profile") + "#journal")

    @app.route("/meals/<int:meal_id>/delete", methods=["POST"])
    @login_required
    def delete_meal(meal_id):
        meal = db.session.get(Meal, meal_id)
        if not meal or meal.user_id != current_user.id:
            abort(404)
        db.session.delete(meal)
        db.session.commit()
        return redirect(url_for("profile") + "#journal")

    @app.route("/weight/add", methods=["POST"])
    @login_required
    def add_weight():
        try:
            w = float(request.form.get("weight"))
            entry_date = request.form.get("date") or date.today().isoformat()
            d = datetime.strptime(entry_date, "%Y-%m-%d").date()
            entry = WeightEntry(user_id=current_user.id, weight=w, recorded_on=d)
            db.session.add(entry)
            current_user.weight = w
            db.session.commit()
            flash("Poids enregistré.", "success")
        except (TypeError, ValueError):
            db.session.rollback()
            flash("Poids invalide.", "error")
        return redirect(url_for("profile") + "#journal")

    @app.route("/steps/add", methods=["POST"])
    @login_required
    def add_steps():
        try:
            s = int(request.form.get("steps"))
            entry_date = request.form.get("date") or date.today().isoformat()
            d = datetime.strptime(entry_date, "%Y-%m-%d").date()
            existing = (StepEntry.query
                        .filter_by(user_id=current_user.id, recorded_on=d).first())
            if existing:
                existing.steps = s
            else:
                db.session.add(StepEntry(user_id=current_user.id, steps=s, recorded_on=d))
            db.session.commit()
            flash("Pas enregistrés.", "success")
        except (TypeError, ValueError):
            db.session.rollback()
            flash("Nombre de pas invalide.", "error")
        return redirect(url_for("profile") + "#journal")

    # ---------------- SPORT ----------------
    @app.route("/sport", methods=["GET", "POST"])
    @login_required
    def sport():
        if request.method == "POST":
            choices = request.form.getlist("sport")
            allowed = {"gym", "pilates", "yoga"}
            choices = [c for c in choices if c in allowed]
            if not choices:
                flash("Choisis au moins une discipline.", "error")
                return redirect(url_for("sport"))
            current_user.sport_choice = ",".join(choices)
            db.session.commit()
            flash("Programme mis à jour.", "success")
            return redirect(url_for("sport"))

        program = []
        if current_user.sport_choice and current_user.goal:
            program = build_program(current_user.sport_choice, current_user.goal)
        active = set((current_user.sport_choice or "").split(",")) if current_user.sport_choice else set()
        return render_template("sport.html", program=program, active=active, goals=GOALS)

    # ---------------- GYMS ----------------
    @app.route("/gyms")
    def gyms():
        category = request.args.get("category", "classic")
        city = (request.args.get("city") or "").strip().lower()
        data = all_gyms()
        if category not in data:
            category = "classic"
        items = data[category]
        if city:
            items = [g for g in items if city in g["city"].lower()]
        cities = sorted({g["city"] for g in data[category]})
        return render_template("gyms.html",
                               category=category,
                               items=items,
                               cities=cities,
                               counts={k: len(v) for k, v in data.items()},
                               selected_city=city)

    # ---------------- MEAL PLAN ----------------
    @app.route("/meal-plan")
    @login_required
    def meal_plan():
        if not current_user.goal:
            flash("Renseigne ton objectif dans le profil pour débloquer ton plan.", "info")
            return redirect(url_for("profile"))
        plan = get_plan(current_user.goal)
        return render_template("meal_plan.html", plan=plan, goal_label=GOALS.get(current_user.goal))

    @app.route("/meal-plans/preview")
    def meal_plans_preview():
        return render_template("meal_plan_preview.html", plans=all_plans(), goals=GOALS)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def too_large(_):
        flash("Photo trop volumineuse (max 6 Mo).", "error")
        return redirect(url_for("profile") + "#journal")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
