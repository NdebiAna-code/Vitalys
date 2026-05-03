from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    goal = db.Column(db.String(20))
    sport_choice = db.Column(db.String(80))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    meals = db.relationship('Meal', backref='user', lazy=True,
                            cascade='all, delete-orphan',
                            order_by='Meal.eaten_at.desc()')
    weight_entries = db.relationship('WeightEntry', backref='user', lazy=True,
                                     cascade='all, delete-orphan',
                                     order_by='WeightEntry.recorded_on.desc()')
    step_entries = db.relationship('StepEntry', backref='user', lazy=True,
                                   cascade='all, delete-orphan',
                                   order_by='StepEntry.recorded_on.desc()')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def bmi(self):
        if self.weight and self.height:
            try:
                return round(self.weight / ((self.height / 100) ** 2), 1)
            except ZeroDivisionError:
                return None
        return None

    @property
    def bmi_category(self):
        b = self.bmi
        if b is None:
            return None
        if b < 18.5:
            return "Insuffisance pondérale"
        if b < 25:
            return "Corpulence normale"
        if b < 30:
            return "Surpoids"
        return "Obésité"

    @property
    def allowed_goals(self):
        b = self.bmi
        if b is None:
            return ["loss", "gain", "maintain"]
        if b < 18.5:
            return ["gain", "maintain"]
        return ["loss", "gain", "maintain"]


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    meal_type = db.Column(db.String(50))
    photo = db.Column(db.String(300))
    notes = db.Column(db.Text)
    eaten_at = db.Column(db.DateTime, default=datetime.utcnow)


class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    recorded_on = db.Column(db.Date, default=date.today)


class StepEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    recorded_on = db.Column(db.Date, default=date.today)
