from datetime import date, datetime
import sqlite3
from sqlite3 import Cursor
from typing import NamedTuple

type DBActivity = tuple[int, str, str | None, str | None, str, bool, str | None]


class Activity(NamedTuple):
    title: str
    description: str | None
    place: str | None
    start: datetime
    startHasTime: bool
    end: datetime | None


def initDB() -> Cursor:
    connection = sqlite3.connect("activities.db")
    cursor = connection.cursor()
    cursor = cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            place TEXT,
            start TEXT NOT NULL,
            startHasTime INTEGER NOT NULL,
            end TEXT
        );
        """
    )
    return cursor


def emptyDatabase(cursor: Cursor) -> None:
    cursor = cursor.execute("DELETE FROM activities")
    cursor.connection.commit()


def addActivitiesToDatabase(cursor: Cursor, activities: list[Activity]) -> None:
    cursor = cursor.executemany(
        "INSERT INTO activities (title, description, place, start, startHasTime, end) VALUES (?, ?, ?, ?, ?, ?)",
        map(
            lambda activity: [
                activity.title,
                activity.description,
                activity.place,
                activity.start.isoformat(),
                activity.startHasTime,
                (None if activity.end == None else activity.end.isoformat()),
            ],
            activities,
        ),
    )
    cursor.connection.commit()


def getTotalActivities(cursor: Cursor) -> int:
    cursor = cursor.execute("SELECT COUNT(*) FROM activities")
    result: tuple[int] = cursor.fetchone()
    return result[0]


def parseDBActivity(dbActivity: DBActivity) -> Activity:
    (
        _id,
        title,
        description,
        place,
        start,
        startHasTime,
        end,
    ) = dbActivity
    return Activity(
        title,
        description,
        place,
        datetime.fromisoformat(start),
        bool(startHasTime),
        None if end == None else datetime.fromisoformat(end),
    )


def getAllActivities(cursor: Cursor) -> list[Activity]:
    dbActivities = cursor.execute("SELECT * FROM activities").fetchall()
    return list(map(parseDBActivity, dbActivities))


def getNextActivities(cursor: Cursor) -> list[Activity]:
    dbActivities = cursor.execute(
        """
        SELECT * FROM activities
        WHERE unixepoch(start) > unixepoch(datetime('now'))
        ORDER BY unixepoch(start)
        LIMIT 5
        """
    ).fetchall()
    return list(map(parseDBActivity, dbActivities))


def getMorningActivities(cursor: Cursor) -> list[Activity]:
    dbGames = cursor.execute(
        """
        SELECT * FROM activities
        WHERE TIME(start) BETWEEN '00:00:00' AND '11:59:59'
        AND startHasTime > 0
        """
    ).fetchall()
    return list(map(parseDBActivity, dbGames))


def getPlaces(cursor: Cursor) -> set[str]:
    places: list[tuple[str]] = cursor.execute(
        "SELECT DISTINCT place FROM activities"
    ).fetchall()
    return set([place for (place,) in places])


def getActivitiesByPlace(cursor: Cursor, place: str) -> list[Activity]:
    dbActivities = cursor.execute(
        f"""
            SELECT * FROM activities 
            WHERE place LIKE ?
        """,
        (f"%{place}%",),
    ).fetchall()
    return list(map(parseDBActivity, dbActivities))


def getActivitiesByDate(cursor: Cursor, date: date) -> list[Activity]:
    dbActivities = cursor.execute(
        f"""SELECT * FROM activities 
          WHERE start LIKE ?""",
        (f"%{date.strftime('%Y-%m-%d')}%",),
    ).fetchall()
    return list(map(parseDBActivity, dbActivities))
