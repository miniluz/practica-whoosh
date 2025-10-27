from typing import cast
from bs4 import BeautifulSoup, Tag
import urllib.request
import lxml  # pyright: ignore[reportUnusedImport, reportMissingTypeStubs]
from typing import NamedTuple

from datetime import datetime, time

import os, ssl

if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context

class Recipe(NamedTuple):
    title: str
    numDiners: int
    author: str 
    updateDate: datetime
    additionalCharacteristics: list[str]
    introduction: str


def processSite() -> list[Recipe]:
    url = "https://www.recetasgratis.net/Recetas-de-Aperitivos-tapas-listado_receta-1_1.html"
    siteHTML = cast(str, urllib.request.urlopen(url))
    siteSoup = BeautifulSoup(siteHTML, "lxml")

    recipesHtml = siteSoup.find("div", id="content-core").find_all("article")

    recipes: list[Recipe] = [
        parseElement(recipeHtml) for recipeHtml in recipesHtml
    ]

    # print(activities[0])

    return recipes


def parseElement(recipeHtml: Tag) -> Recipe:

    titleTag = recipeHtml.find("h2", class_="tileHeadline")

    title = titleTag.text.strip()

    link = titleTag.find("a").get("href")

    try:
        place = extractPlace(link)
    except:
        place = None
    startDate = datetime.fromisoformat(
        recipeHtml.find("abbr", class_="dtstart").get("title")
    )

    try:
        endDate = datetime.fromisoformat(
            recipeHtml.find("abbr", class_="dtend").get("title")
        )
    except:
        endDate = None

    hasStartTime = startDate.time() != time(0, 0, 0)

    try:
        description = recipeHtml.find("p", class_="description").text.strip()
    except:
        description = None
    pass

    return Recipe(
        title=title,
        description=description,
        place=place,
        start=startDate,
        startHasTime=hasStartTime,
        end=endDate,
    )


def extractPlace(link):
    siteHTML = cast(str, urllib.request.urlopen(link))
    siteSoup = BeautifulSoup(siteHTML, "lxml")
    return siteSoup.find("span", itemprop="location").text


if __name__ == "__main__":
    processSite()
