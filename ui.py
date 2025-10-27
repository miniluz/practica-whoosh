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

from database import Recipe


def main_window(
    load: Callable[[], None],
    getTotalRecipes: Callable[[], int],
    getAllRecipes: Callable[[], list[Recipe]],
    getRecipesByTitleOrIntroduction: Callable[[str], list[Recipe]],
    getRecipesByDate: Callable[[str, str], list[Recipe]],
    getRecipesByCharacteristicsAndTitle: Callable[[str], list[Recipe]],
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


def searchByTitleOrIntro(
    getRecipesByTitleOrIntroduction: Callable[[str], list[Recipe]],
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
    getRecipesByDate: Callable[[str, str], list[Recipe]],
) -> None:
    top = Toplevel()
    top.title("Buscar por fecha")
    top.geometry("350x100")
    L1 = Label(top, text="Introduzca la un rango de fechas en formato DD/MM/YYYY")
    L1.pack(side=LEFT)
    firstDateEntry = Entry(top)
    firstDateEntry.pack(fill=X, side=RIGHT)
    secondDateEntry = Entry(top)
    secondDateEntry.pack(fill=X, side=RIGHT)

    search = lambda _: listRecipes(
        getRecipesByDate(
            firstDateEntry.get(),
            secondDateEntry.get(),
        )
    )

    _ = firstDateEntry.bind("<Return>", search)
    _ = secondDateEntry.bind("<Return>", search)


def searchByCharacteristicAndTitle(
    getRecipesByCharacteristicsAndTitle: Callable[[str], list[Recipe]],
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


def listRecipes(activities: list[Recipe]) -> None:
    topLevel = Toplevel()
    scrollbar = Scrollbar(topLevel)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(topLevel, width=150, yscrollcommand=scrollbar.set)
    for activity in activities:
        listbox.insert(END, f"Titulo: {activity.title}")
        listbox.insert(END, "-" * len(activity.title))
        listbox.insert(END, f"Descripcion: {activity.description}")
        listbox.insert(END, f"Lugar de celebracion: {activity.place}")
        listbox.insert(END, f"Inicio: {activity.start}")
        listbox.insert(END, f"Fin: {activity.end}")
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
