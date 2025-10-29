import os
import shutil
from datetime import date, datetime

from whoosh.fields import DATETIME, KEYWORD, STORED, TEXT, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser

from scraper import Recipe

schema = Schema(
    title=TEXT(stored=True),
    numDinners=STORED,
    author=STORED,
    additionalCharacteristics=KEYWORD(stored=True, lowercase=True, commas=True),
    updateDate=DATETIME(stored=True),
    introduction=TEXT(stored=True),
)


def writeRecipes(recipes: list[Recipe]) -> int:
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
        query_parser = MultifieldParser(["title", "introduction"], schema=schema)
        query = query_parser.parse(phrase)
        results = searcher.search(query, limit=None)
        return list(map(resultToRecipe, results))


def getRecipesByDate(startDate: date, endDate: date) -> list[Recipe]:
    with open_dir("Index").searcher() as searcher:
        query_parser = QueryParser("updateDate", schema=schema)
        query_string = (
            f"[{startDate.strftime('%Y%m%d')} to {endDate.strftime('%Y%m%d')}]"
        )
        print(query_string)
        query = query_parser.parse(query_string)
        print(query)
        results = searcher.search(query, limit=None)
        print(results)
        return list(map(resultToRecipe, results))


def getCharacteristics() -> list[str]:
    recipes = getAllRecipes()
    characteristics = [
        char
        for recipe in recipes
        for char in recipe.additionalCharacteristics.split(",")
    ]
    return list(set(characteristics))


def getRecipesByCharacteristicsAndTitle(
    characteristic: str, phrase: str
) -> list[Recipe]:
    with open_dir("Index").searcher() as searcher:
        query_parser = QueryParser("title", schema=schema)
        query = query_parser.parse(
            f"'{phrase}' AND additionalCharacteristics:'{characteristic}'",
        )
        results = searcher.search(query, limit=None)
        return list(map(resultToRecipe, results))
