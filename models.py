from datetime import datetime
from config import db
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

class Recipe(db.Model):
    __tablename__ = "recipe"
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))   
    ingredients = db.relationship(
        'Ingredient',
        backref='recipe',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Ingredient.ingredient_id)'
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class RecipeSchema(ModelSchema):
    class Meta:
        model = Recipe
        sqla_session = db.session
    ingredients = fields.List(fields.Nested(lambda: IngredientSchema(only=("ingredient_id", "content", "timestamp"))))

class RecipeIngredientsSchema(ModelSchema):
    """
    Flatten the object
    """
    ingredient_id = fields.Int()
    recipe_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

class IngredientSchema(ModelSchema):
    class Meta:
        model = Ingredient
        sqla_session = db.session
    recipe = fields.Nested(lambda: RecipeSchema(only=("recipe_id", "title", "timestamp")))

class IngredientRecipeSchema(ModelSchema):
    """
    Flatten the object
    """
    recipe_id = fields.Int()
    title = fields.Str()
    timestamp = fields.Str()