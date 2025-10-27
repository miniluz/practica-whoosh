import os
import shutil
from datetime import datetime

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
    title: str = result["title"]
    try:
        numDiners: int | None = result["numDinner"]
    except:
        numDiners = None
    author: str = result["author"]
    additionalCharacteristics: str = result["additionalCharacteristics"]
    updateDate: datetime = result["updateDate"]
    introduction: str = result["introduction"]
    return Recipe(
        title=title,
        numDiners=numDiners,
        author=author,
        additionalCharacteristics=additionalCharacteristics,
        updateDate=updateDate,
        introduction=introduction,
    )


def getAllRecipes() -> list[Recipe]:
    with open_dir("Index").searcher() as searcher:
        return list(map(resultToRecipe, searcher.documents()))


def getRecipesByTitleOrIntroduction(phrase: str) -> list[Recipe]:
    with open_dir("Index").searcher() as searcher:
        query = QueryParser("")
        return list(map(resultToRecipe, searcher.documents()))


def getRecipesByDate(startDate: str, endDate) -> list[Recipe]:
    return []


def getRecipesByCharacteristicsAndTitle(phrase: str) -> list[Recipe]:
    return []
