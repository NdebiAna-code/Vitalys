"""Programmes de sport adaptés au choix utilisateur et à l'objectif."""

GOALS = {
    "loss": "Perte de poids",
    "gain": "Prise de masse",
    "maintain": "Maintien",
}


def _gym_program(goal):
    if goal == "loss":
        return [
            {"day": "Lundi", "focus": "HIIT brûle-graisses", "exercises": [
                "10 min de tapis de course à allure modérée (échauffement)",
                "5 tours : 30s burpees / 30s mountain climbers / 30s squat jumps / 30s repos",
                "3x12 tractions assistées",
                "3x15 relevés de jambes suspendus",
                "10 min de vélo elliptique en cool-down",
            ]},
            {"day": "Mardi", "focus": "Cardio long & abdos", "exercises": [
                "45 min de course à pied à allure modérée (zone 2)",
                "4x20 crunchs / 4x20 obliques / 4x60s gainage planche",
                "Étirements 10 min",
            ]},
            {"day": "Mercredi", "focus": "Repos actif", "exercises": [
                "30 min de marche rapide ou yoga doux",
                "Mobilité des hanches et des épaules",
            ]},
            {"day": "Jeudi", "focus": "Renforcement bas du corps", "exercises": [
                "4x12 squats à la barre (charge légère)",
                "4x12 fentes marchées avec haltères",
                "3x15 hip thrust",
                "3x20 mollets debout",
                "15 min de stepper",
            ]},
            {"day": "Vendredi", "focus": "Circuit full-body", "exercises": [
                "5 tours sans repos : 15 kettlebell swings / 12 push-ups / 15 box jumps / 12 rowing haltère / 30s gainage",
                "10 min de corde à sauter",
            ]},
            {"day": "Samedi", "focus": "Cardio fractionné", "exercises": [
                "Sprints sur tapis : 10x (45s vite / 75s lent)",
                "3x30 abdos roulettes",
            ]},
            {"day": "Dimanche", "focus": "Repos complet", "exercises": [
                "Marche en extérieur, sieste, hydratation",
            ]},
        ]
    if goal == "gain":
        return [
            {"day": "Lundi", "focus": "Pectoraux & triceps", "exercises": [
                "Développé couché barre 4x6-8 (charge lourde)",
                "Développé incliné haltères 4x10",
                "Écarté à la poulie 3x12",
                "Dips lestés 3x8",
                "Extensions triceps poulie 4x12",
            ]},
            {"day": "Mardi", "focus": "Dos & biceps", "exercises": [
                "Tractions lestées 4x6",
                "Rowing barre 4x8",
                "Tirage poitrine prise large 3x10",
                "Curl barre EZ 4x10",
                "Curl marteau 3x12",
            ]},
            {"day": "Mercredi", "focus": "Repos / mobilité", "exercises": [
                "20 min vélo très léger",
                "Mobilité épaules + hanches 15 min",
            ]},
            {"day": "Jeudi", "focus": "Jambes complet", "exercises": [
                "Squat barre 5x5 (charge lourde)",
                "Soulevé de terre roumain 4x8",
                "Presse à cuisses 4x10",
                "Leg curl 4x12",
                "Mollets assis 4x15",
            ]},
            {"day": "Vendredi", "focus": "Épaules & abdos", "exercises": [
                "Développé militaire barre 4x6",
                "Élévations latérales 4x12",
                "Oiseau haltères 3x12",
                "Shrugs 3x15",
                "Crunchs lestés 4x15 / Gainage 4x60s",
            ]},
            {"day": "Samedi", "focus": "Bras + erreurs visées", "exercises": [
                "Curl barre 4x10 + dips 4x10 (superset)",
                "Curl pupitre 3x12 + extensions verticales 3x12",
                "Avant-bras : flexion poignets 4x15",
            ]},
            {"day": "Dimanche", "focus": "Repos complet", "exercises": [
                "Récupération, alimentation hypercalorique",
            ]},
        ]
    return [
        {"day": "Lundi", "focus": "Full body modéré", "exercises": [
            "Squat 4x10 / Développé couché 4x10 / Rowing 4x10",
            "Gainage 3x45s",
        ]},
        {"day": "Mardi", "focus": "Cardio doux", "exercises": ["30 min vélo elliptique zone 2"]},
        {"day": "Mercredi", "focus": "Renforcement haut du corps", "exercises": [
            "Tractions assistées 4x8 / Développé épaules 4x10 / Curl 3x12",
        ]},
        {"day": "Jeudi", "focus": "Repos / étirements", "exercises": ["20 min de mobilité"]},
        {"day": "Vendredi", "focus": "Renforcement bas du corps", "exercises": [
            "Fentes 4x12 / Hip thrust 4x12 / Mollets 4x15",
        ]},
        {"day": "Samedi", "focus": "Cardio plaisir", "exercises": ["45 min nature : course, vélo ou marche rapide"]},
        {"day": "Dimanche", "focus": "Repos", "exercises": ["Récupération, hydratation"]},
    ]


def _pilates_program(goal):
    base = [
        {"day": "Lundi", "focus": "Pilates Reformer — gainage profond", "exercises": [
            "Hundred (100 pulses)",
            "Roll-Up x10",
            "Single Leg Stretch 2x10",
            "Spine Stretch Forward x8",
            "Saw x6 par côté",
        ]},
        {"day": "Mardi", "focus": "Pilates Mat — fessiers & jambes", "exercises": [
            "Side-lying leg lifts 3x15",
            "Clamshells 3x15",
            "Bridge 3x12",
            "Single Leg Circle 2x8 par côté",
        ]},
        {"day": "Mercredi", "focus": "Repos actif", "exercises": ["Marche 30 min, étirements 15 min"]},
        {"day": "Jeudi", "focus": "Pilates Reformer — dos & épaules", "exercises": [
            "Long Box Pulling Straps 2x10",
            "Swan Dive (préparation) 3x6",
            "Mermaid 2x6 par côté",
        ]},
        {"day": "Vendredi", "focus": "Pilates Mat — abdos profonds", "exercises": [
            "Teaser (préparation) 3x6",
            "Criss-Cross 3x16",
            "Plank Pilates 3x30s",
            "Roll Over 2x6",
        ]},
        {"day": "Samedi", "focus": "Stretching profond", "exercises": ["30 min étirements globaux et respiration"]},
        {"day": "Dimanche", "focus": "Repos complet", "exercises": ["Récupération"]},
    ]
    if goal == "loss":
        base.insert(2, {"day": "Mercredi (extra)", "focus": "Cardio léger", "exercises": ["30 min de marche rapide ou vélo extérieur"]})
    if goal == "gain":
        base.append({"day": "Bonus", "focus": "Travail charge avec bandes", "exercises": ["3x12 squats avec bande forte / 3x12 rowing élastique / 3x12 développé épaules élastique"]})
    return base


def _yoga_program(goal):
    base = [
        {"day": "Lundi", "focus": "Vinyasa Flow dynamique", "exercises": [
            "Salutation au soleil A x5",
            "Salutation au soleil B x5",
            "Guerrier I, II, III enchaînés",
            "Chien tête en bas — 5 respirations",
            "Savasana 5 min",
        ]},
        {"day": "Mardi", "focus": "Hatha Yoga — alignement", "exercises": [
            "Posture de la montagne",
            "Triangle x 4 par côté",
            "Posture de l'arbre x 1 min par jambe",
            "Posture de l'enfant 2 min",
        ]},
        {"day": "Mercredi", "focus": "Yin Yoga — relâcher", "exercises": [
            "Papillon 4 min",
            "Dragon 3 min par côté",
            "Sphinx 3 min",
            "Posture du cadavre 8 min",
        ]},
        {"day": "Jeudi", "focus": "Ashtanga modifié", "exercises": [
            "Série primaire allégée — 30 min",
            "Pranayama 10 min",
        ]},
        {"day": "Vendredi", "focus": "Power Yoga", "exercises": [
            "Flow soutenu 45 min",
            "Travail d'équilibres : aigle, demi-lune",
        ]},
        {"day": "Samedi", "focus": "Yoga restauratif", "exercises": [
            "Postures avec bolster — 45 min",
            "Méditation guidée 10 min",
        ]},
        {"day": "Dimanche", "focus": "Repos / méditation", "exercises": ["Méditation 15 min, marche douce"]},
    ]
    if goal == "loss":
        base.insert(2, {"day": "Mercredi (extra)", "focus": "Cardio doux", "exercises": ["30 min de marche rapide en pleine conscience"]})
    if goal == "gain":
        base.append({"day": "Bonus", "focus": "Renforcement complémentaire", "exercises": ["3x10 push-ups / 3x10 chair pose tenue 30s / 3x10 boat pose"]})
    return base


def build_program(sport_choice, goal):
    """Construit un programme complet selon le choix sport et l'objectif."""
    choices = (sport_choice or "").lower().split(",")
    choices = [c.strip() for c in choices if c.strip()]
    blocks = []
    if "gym" in choices:
        blocks.append({"title": "Bloc Salle de sport", "days": _gym_program(goal)})
    if "pilates" in choices:
        blocks.append({"title": "Bloc Pilates", "days": _pilates_program(goal)})
    if "yoga" in choices:
        blocks.append({"title": "Bloc Yoga", "days": _yoga_program(goal)})
    return blocks
