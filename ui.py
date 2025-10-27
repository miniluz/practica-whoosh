from tkinter import (
    BOTH,
    END,
    LEFT,
    RIGHT,
    Entry,
    Label,
    Listbox,
    Menu,
    Scrollbar,
    Tk,
    Toplevel,
    X,
    Y,
    messagebox,
)
from typing import Callable

from scraper import Recipe


def main_window(
    load: Callable[[], None],
    getTotalActivities: Callable[[], int],
    getAllActivities: Callable[[], list[Recipe]],
    getNextActivities: Callable[[], list[Recipe]],
    getMorningActivities: Callable[[], list[Recipe]],
    getPlaces: Callable[[], set[str]],
    getActivitiesByPlace: Callable[[str], list[Recipe]],
    getActivitiesByDate: Callable[[date], list[Recipe]],
) -> None:
    root = Tk()

    mainMenu = Menu(root)

    # Data
    dataMenu = Menu(mainMenu, tearoff=0)
    dataMenu.add_command(
        label="Cargar", command=lambda: confirmLoad(load, getTotalRecipes)
    )
    dataMenu.add_command(label="Listar", command=lambda: listRecipes(getAllRecipes()))
    dataMenu.add_command(label="Salir", command=mainMenu.quit)
    mainMenu.add_cascade(label="Datos", menu=dataMenu)

    # Search
    searchMenu = Menu(mainMenu, tearoff=0)
    searchMenu.add_command(
        label="Título o introducción",
        command=lambda: searchByTitleOrIntro(getRecipesByTitleOrIntroduction),
    )
    searchMenu.add_command(
        label="Fecha",
        command=lambda: searchByDate(getRecipesByDate),
    )
    searchMenu.add_command(
        label="Características y título",
        command=lambda: searchByCharacteristicAndTitle(
            getRecipesByCharacteristicsAndTitle
        ),
    )
    mainMenu.add_cascade(label="Buscar", menu=searchMenu)

    _ = root.config(menu=mainMenu)

    root.mainloop()


def searchByPlace(
    getPlaces: Callable[[], set[str]],
    getActivitiesByPlace: Callable[[str], list[Recipe]],
) -> None:
    top = Toplevel()
    top.title("Buscar por título o introducción")
    top.geometry("350x100")
    L1 = Label(top, text="Introduzca una frase con la que buscar:")
    L1.pack(side=LEFT)
    textEntry = Entry(top)
    textEntry.pack(fill=X, side=RIGHT)
    _ = textEntry.bind(
        "<Return>",
        lambda _: listRecipes(
            getRecipesByTitleOrIntroduction(
                textEntry.get(),
            )
        ),
    )


def searchByDate(
    getByDate: Callable[[date], list[Recipe]],
) -> None:
    top = Toplevel()
    top.title("Buscar por características y título")
    top.geometry("350x100")
    L1 = Label(top, text="Introduzca una frase con la que buscar:")
    L1.pack(side=LEFT)
    textEntry = Entry(top)
    textEntry.pack(fill=X, side=RIGHT)
    _ = textEntry.bind(
        "<Return>",
        lambda _: listRecipes(
            getRecipesByCharacteristicsAndTitle(
                textEntry.get(),
            ),
        ),
    )


def searchPicker(
    name: str, options: list[str], callback: Callable[[str], None]
) -> None:
    topLevel = Toplevel()

    label = Label(topLevel, text=f"Escoge {name}")
    label.pack(side=LEFT)
    picker = Spinbox(topLevel, values=options, state="readonly")
    _ = picker.bind("<Return>", lambda event: callback(str(picker.get())))
    picker.pack(side=LEFT)


def listActivities(activities: list[Recipe]) -> None:
    topLevel = Toplevel()
    scrollbar = Scrollbar(topLevel)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(topLevel, width=150, yscrollcommand=scrollbar.set)
    for Recipe in activities:
        listbox.insert(END, f"Titulo: {Recipe.title}")
        listbox.insert(END, "-" * len(Recipe.title))
        listbox.insert(END, f"Descripcion: {Recipe.description}")
        listbox.insert(END, f"Lugar de celebracion: {Recipe.place}")
        listbox.insert(END, f"Inicio: {Recipe.start}")
        listbox.insert(END, f"Fin: {Recipe.end}")
        listbox.insert(END, "")
        listbox.insert(END, "")
    listbox.pack(side=LEFT, fill=BOTH)
    _ = scrollbar.config(
        command=listbox.yview  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    )


def confirmLoad(
    load: Callable[[], None], getTotalActivities: Callable[[], int]
) -> None:
    answer = messagebox.askyesno(
        title="Confirmar",
        message="Estas seguro de que quieres cargar los datos?\nEsto puede tomar un rato.",
    )
    if answer:
        load()
    total = getTotalActivities()
    _ = messagebox.showinfo(
        "Resultado de la carga", f"Se han añadido un total de {total} recetas"
    )
