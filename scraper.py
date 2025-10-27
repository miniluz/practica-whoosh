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

from database import Activity


def processSite() -> list[Activity]:
    url = "https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades/"
    siteHTML = cast(str, urllib.request.urlopen(url))
    siteSoup = BeautifulSoup(siteHTML, "lxml")

    activitiesHtml = siteSoup.find("div", id="content-core").find_all("article")

    activities: list[Activity] = [
        parseActivity(activityHtml) for activityHtml in activitiesHtml
    ]

    # print(activities[0])

    return activities


def parseActivity(activityHtml: Tag) -> Activity:

    titleTag = activityHtml.find("h2", class_="tileHeadline")

    title = titleTag.text.strip()

    link = titleTag.find("a").get("href")

    try:
        place = extractPlace(link)
    except:
        place = None
    startDate = datetime.fromisoformat(
        activityHtml.find("abbr", class_="dtstart").get("title")
    )

    try:
        endDate = datetime.fromisoformat(
            activityHtml.find("abbr", class_="dtend").get("title")
        )
    except:
        endDate = None

    hasStartTime = startDate.time() != time(0, 0, 0)

    try:
        description = activityHtml.find("p", class_="description").text.strip()
    except:
        description = None
    pass

    return Activity(
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
