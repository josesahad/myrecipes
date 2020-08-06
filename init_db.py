import os
from config import db
from models import Recipe, Ingredient

RECIPE = [
    {
        "title": "Fideos con salsa", 
        "ingredients": [
            ("Fideos"), ("salsa"),
        ], 
    },
    {
        "title": "Sorrentinos de jamon", 
        "ingredients": [
            ("Sorrentinos"), ("salsa"),
        ],
    },
    {
        "title": "Ravioles con tuco", 
        "ingredients": [
            ("Ravioles"), ("tuco"),
        ],
    },
]

if os.path.exists("recipe.db"):
    os.remove("recipe.db")

db.create_all()

for recipe in RECIPE:
    r = Recipe(title=recipe.get("title"))
    
    for ingredient in recipe.get("ingredients"):
        content = ingredient
        r.ingredients.append(
            Ingredient(
                content=content
            )
        )
    db.session.add(r)

db.session.commit()