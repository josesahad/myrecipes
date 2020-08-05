import os
from config import db
from models import Recipe

# Data to initialize database with
RECIPE = [
    {"title": "Fideos con salsa", "ingredients": "Fideos, salsa"},
    {"title": "Sorrentinos de jamon", "ingredients": "Sorrentinos, salsa"},
    {"title": "Ravioles con tuco", "ingredients": "Ravioles, tuco"},
]

if os.path.exists("recipe.db"):
    os.remove("recipe.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for recipe in RECIPE:
    r = Recipe(title=recipe.get("title"), ingredients=recipe.get("ingredients"))
    db.session.add(r)

db.session.commit()