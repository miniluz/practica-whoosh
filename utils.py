from bs4 import Tag
from bs4.element import NavigableString, PageElement


type FindResult = Tag | NavigableString | PageElement | None


def tagOrNone(tag: FindResult) -> Tag | None:
    if not isinstance(tag, Tag):
        return None
    return tag


def checkIsTag(tag: FindResult, context: str = "") -> Tag:
    if not isinstance(tag, Tag):
        error = LookupError(f"Lookup resulted in {type(tag)}")
        error.add_note(context)
        raise error

    return tag


def listToString(listOrString: str | list[str], context: str = "") -> str:
    if isinstance(listOrString, list):
        if len(listOrString) == 0:
            error = LookupError("Lookup resulted in an empty list")
            error.add_note(context)
            raise error

        return listOrString[0]

    return listOrString


def splitOnVarious(string: str, splitChars: list[str]) -> list[str]:
    buffer = [string]
    for splitChar in splitChars:
        buffer = [
            substring for string in buffer for substring in string.split(splitChar)
        ]
    return buffer
