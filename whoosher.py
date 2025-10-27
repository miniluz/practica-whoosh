import os
import shutil

from whoosh.fields import DATETIME, KEYWORD, STORED, TEXT, Schema
from whoosh.index import create_in, open_dir

from scraper import Recipe


def writeRecipes(recipes: list[Recipe]) -> int:
    schema = Schema(
        title=TEXT(stored=True),
        numDinners=STORED,
        author=STORED,
        additionalCharacteristics=KEYWORD(stored=True, lowercase=True, commas=True),
        updateDate=DATETIME(stored=True),
        introduction=TEXT(stored=True),
    )

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    index = create_in("Index", schema=schema)

    writer = index.writer()

    for recipe in recipes:
        writer.add_document(
            title=str(recipe.title),
            numDinners=recipe.numDiners,
            author=str(recipe.author),
            additionalCharacteristics=str(recipe.additionalCharacteristics),
            updateDate=recipe.updateDate,
            introduction=str(recipe.introduction),
        )

    writer.commit()

    return len(recipes)


def resultToRecipe(result) -> Recipe:
    return Recipe(
        title=result.row["title"],
        numDiners=result.row["numDinner"],
        author=result.row["author"],
        additionalCharacteristics=result.row["additionalCharacteristics"],
        updateDate=result.row["updateDate"],
        introduction=result.row["introduction"],
    )


def getAllRecipes() -> list[Recipe]:
    with open_dir("Index").searcher() as searcher:
        return list(map(resultToRecipe, searcher.documents()))


def getRecipesByTitleOrIntroduction(phrase: str) -> list[Recipe]:
    return []


def getRecipesByDate(startDate: str, endDate) -> list[Recipe]:
    return []


def getRecipesByCharacteristicsAndTitle(phrase: str) -> list[Recipe]:
    return []
