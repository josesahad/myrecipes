"""
Recipe module
"""
from flask import make_response, abort

# Testing data
RECIPE = {
    1: {
        "id": 1,
        "recipeTitle": "Ravioles con Tuco",
        "recipeIngredients": "Ravioles, Tuco"
    },
    2: {
        "id": 2,
        "recipeTitle": "Fideos con Bolognesa",
        "recipeIngredients": "Fideos, Tuco, Carne"
    },
}


def get_all():
    """
    Get a list of recipes

    :return:        List of recipes
    """
    return [RECIPE[key] for key in sorted(RECIPE.keys())]


def get_one(recipeId):
    """
    Retrieves a recipe

    :param id:      id of the recipe
    :return:        Recipe for the given id
    """
    if recipeId in RECIPE:
        recipe = RECIPE.get(recipeId)

    else:
        abort(
            404, "Recipe {recipeId} not found".format(recipeId=recipeId)
        )

    return recipe


def create(recipe):
    """
    Creates a recipe

    :param recipe:  recipe to create
    :return:        201 on success
    """
    recipeId = recipe.get("id", None)
    recipeTitle = recipe.get("recipeTitle", None)
    recipeIngredients = recipe.get("recipeIngredients", None)

    if recipeId not in RECIPE and recipeId is not None:
        RECIPE[recipeId] = {
            "id": recipeId,
            "recipeTitle": recipeTitle,
            "recipeIngredients": recipeIngredients,
        }
        return RECIPE[recipeId], 201

    else:
        abort(
            406,
            "Recipe {recipeId} already exists".format(recipeId=recipeId),
        )


def update(recipeId, recipe):
    """
    Updates a recipe

    :param id:      recipe id
    :param recipe:  recipe to update
    :return:        updated recipe
    """
    if recipeId in RECIPE:
        RECIPE[recipeId]["recipeTitle"] = recipe.get("recipeTitle")
        RECIPE[recipeId]["recipeIngredients"] = recipe.get("recipeIngredients")

        return RECIPE[recipeId]

    else:
        abort(
            404, "Recipe {recipeId} not found".format(recipeId=recipeId)
        )


def delete(recipeId):
    """
    Deletes a recipe

    :param id:      Id of the recipe
    :return:        200 on successful delete
    """
    if recipeId in RECIPE:
        del RECIPE[recipeId]
        return make_response(
            "{recipeId} successfully deleted".format(recipeId=recipeId), 200
        )

    else:
        abort(
            404, "Recipe {recipeId} not found".format(recipeId=recipeId)
        )