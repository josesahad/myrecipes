"""
Recipe module
"""
from flask import make_response, abort
from config import db
from models import Recipe, RecipeSchema, IngredientSchema, Ingredient
from sqlalchemy import engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_all():
    """
    Get a list of recipes

    :return:        List of recipes
    """
    recipe = Recipe.query.order_by(Recipe.recipe_id).all()
    return RecipeSchema(many=True).dump(recipe)


def get_one(recipe_id):
    """
    Retrieves a recipe

    :param recipe_id:      id of the recipe
    :return:        Recipe for the given id
    """
    recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).one_or_none()

    if recipe is not None:
        return RecipeSchema().dump(recipe)

    else:
        abort(
            404, "Recipe {recipe_id} not found".format(recipe_id=recipe_id)
        )

def create(recipe):
    """
    Creates a recipe

    :param recipe:  recipe to create
    :return:        201 on success
    """
    title = recipe.get("title")

    recipe_in_db = (
        Recipe.query.filter(Recipe.title == title).one_or_none()
    )

    if recipe_in_db is None:
        recipe_schema = RecipeSchema()
        session_s = scoped_session(sessionmaker(bind=engine))        
        new_recipe = recipe_schema.load(recipe, session=session_s)
        
        db.session.add(new_recipe)
        db.session.commit()

        return recipe_schema.dump(new_recipe), 201

    else:
        abort(
            406,
            "Recipe {title} already exists".format(title=title),
        )


def update(recipe_id, recipe):
    """
    Updates a recipe

    :param recipe_id:      recipe id
    :param recipe:  recipe to update
    :return:        updated recipe
    """
    title = recipe.get("recipeTitle")
    ingredients = recipe.get("recipeIngredients")

    recipe_to_update = (
        Recipe.query.filter(Recipe.recipe_id == recipe_id).one_or_none()
    )

    recipe_in_db = (
        Recipe.query.filter(Recipe.title == title).filter(Recipe.ingredients == ingredients).one_or_none()
    )

    if recipe_to_update is None:
        abort(
            404, "Recipe {id} not found".format(id=recipe_id)
        )

    elif recipe_in_db is None:
        schema = RecipeSchema()
        recipe_update = schema.load(recipe, session=db.session)

        recipe_update.recipe_id = recipe_to_update.recipe_id

        db.session.merge(recipe_update)
        db.session.commit()

        return schema.dump(recipe_to_update), 200
    else:
        abort(
            406, "Recipe {title} already exists".format(title=title),
        )


def delete(recipe_id):
    """
    Deletes a recipe

    :param recipe_id:      Id of the recipe
    :return:        200 on successful delete
    """
    recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).one_or_none()

    if recipe is not None:
        db.session.delete(recipe)
        db.session.commit()
        return make_response(
            "Recipe {recipe_id} has been deleted".format(recipe_id=recipe_id), 200
        )

    else:
        abort(
            404, "Recipe {recipe_id} not found".format(recipe_id=recipe_id)
        )