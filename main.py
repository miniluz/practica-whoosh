from sqlite3 import Cursor

from database import (
    emptyDatabase,
    addActivitiesToDatabase,
    getAllActivities,
    getNextActivities,
    getMorningActivities,
    getPlaces,
    getActivitiesByPlace,
    getActivitiesByDate,
    getTotalActivities,
    initDB,
)
from scraper import processSite
from ui import main_window


def main():
    def loadActivities(cursor: Cursor) -> None:
        emptyDatabase(cursor)
        activities = processSite()
        addActivitiesToDatabase(cursor, activities)

    cursor = initDB()

    main_window(
        lambda: loadActivities(cursor),
        lambda: getTotalActivities(cursor),
        lambda: getAllActivities(cursor),
        lambda: getNextActivities(cursor),
        lambda: getMorningActivities(cursor),
        lambda: getPlaces(cursor),
        lambda place: getActivitiesByPlace(cursor, place),
        lambda date: getActivitiesByDate(cursor, date),
    )


if __name__ == "__main__":
    main()
