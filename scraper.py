import os
import ssl
import urllib.request
from datetime import datetime
from typing import NamedTuple, cast

from bs4 import BeautifulSoup, Tag

if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context


class Recipe(NamedTuple):
    title: str
    numDiners: int | None
    author: str
    updateDate: datetime
    additionalCharacteristics: str
    introduction: str


def processSite() -> list[Recipe]:
    url = "https://www.recetasgratis.net/Recetas-de-Aperitivos-tapas-listado_receta-1_1.html"
    siteHTML = cast(str, urllib.request.urlopen(url))
    siteSoup = BeautifulSoup(siteHTML, "lxml")

    recipesHtml = siteSoup.find_all("div", class_="resultado link")

    recipes: list[Recipe] = [parseElement(recipeHtml) for recipeHtml in recipesHtml]

    # print(activities[0])

    return recipes


def parseElement(recipeHtml: Tag) -> Recipe:
    url = recipeHtml.find("a").get("href")
    recipeHtml = cast(str, urllib.request.urlopen(url))
    recipeSoup = BeautifulSoup(recipeHtml, "lxml")

    title = recipeSoup.find("h1").text

    try:
        numDinners = int(
            recipeSoup.find("span", class_="property comensales").text.split(" ")[0]
        )
    except:
        numDinners = None
    author = recipeSoup.find("div", class_="nombre_autor").a.text

    import locale

    locale.setlocale(locale.LC_TIME, "es_ES.UTF8")
    updateDate = datetime.strptime(
        recipeSoup.find("span", class_="date_publish").text.replace(
            "Actualizado: ", ""
        ),
        "%d %B %Y",
    )
    additionalCharacteristics = recipeSoup.find("div", class_="properties inline").text
    additionalCharacteristics = ",".join(
        [
            char.strip()
            for char in additionalCharacteristics.replace(
                "Características adicionales:\n", ""
            ).split(",")
        ]
    )
    introduction = recipeSoup.find("div", class_="intro").p.text

    return Recipe(
        title=title.strip(),
        numDiners=numDinners,
        author=author.strip(),
        updateDate=updateDate,
        additionalCharacteristics=additionalCharacteristics,
        introduction=introduction.strip(),
    )


if __name__ == "__main__":
    print(processSite())
