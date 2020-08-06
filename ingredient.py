"""
Ingredient module
"""
from flask import make_response, abort
from config import db
from models import Ingredient, IngredientSchema, Recipe


def get_all():
    """
    Get all ingredients

    :return:        List of ingredients
    """
    ingredient = Ingredient.query.order_by(Ingredient.ingredient_id).all()
    return IngredientSchema(many=True).dump(ingredient)


def get_one(ingredient_id):
    """
    Retrieves a ingredient

    :param ingredient_id:      id of the ingredient
    :return:        Ingredient for the given id
    """
    ingredient = Ingredient.query.filter(Ingredient.ingredient_id == ingredient_id).one_or_none()

    if ingredient is not None:
        return IngredientSchema().dump(Ingredient)

    else:
        abort(
            404, "Ingredient {ingredient_id} not found".format(ingredient_id=ingredient_id)
        )

def get_ingredients_by_recipe(recipe_id):
    """
    Gets the list of ingredients by recipe
    :param recipe_id:    the recipe
    :return:             list of the ingredients for the given recipe
    """
    ingredient = (
        Ingredient.query.join(Recipe, Recipe.recipe_id == Ingredient.recipe_id).filter(Recipe.recipe_id == recipe_id).all()
    )
    return IngredientSchema(many=True).dump(ingredient)


def delete(recipe_id, ingredient_id):
    """
    Deletes an ingredient in a recipe

    :param recipe_id:      Id of the recipe
    :param ingredient_id:  Id of the ingredient
    :return:        200 on successful delete
    """
    ingredient = Ingredient.query.filter(Ingredient.recipe_id == recipe_id).filter(Ingredient.ingredient_id == ingredient_id).first()

    if ingredient is not None:
        db.session.delete(ingredient)
        db.session.commit()
        return make_response(
            "Ingredient {ingredient_id} has been deleted".format(ingredient_id=ingredient_id), 200
        )

    else:
        abort(
            404, "Ingredient {ingredient_id} not found".format(ingredient_id=ingredient_id)
        )


def create(recipe_id, ingredient):
    """
    Creates an ingredient for a recipe
    :param recipe_id:       Id of the recipe
    :param ingredient:      The ingredient to create
    :return:                201 on success
    """
    recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).one_or_none()

    if recipe is None:
        abort(404, f"Recipe not found for Id: {recipe_id}")

    ingredient_schema = IngredientSchema()
    new_ingredient = ingredient_schema.load(note, session=db.session).data

    recipe.ingredients.append(new_ingredient)
    db.session.commit()

    return ingredient_schema.dump(new_ingredient).data, 201