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

from scraper import Recipe, processSite
from whoosher import (
    getAllRecipes,
    getRecipesByCharacteristicsAndTitle,
    getRecipesByDate,
    getRecipesByTitleOrIntroduction,
    writeRecipes,
)


def main_window() -> None:
    root = Tk()

    mainMenu = Menu(root)

    # Data
    dataMenu = Menu(mainMenu, tearoff=0)
    dataMenu.add_command(label="Cargar", command=confirmLoad)
    dataMenu.add_command(label="Listar", command=lambda: listRecipes(getAllRecipes()))
    dataMenu.add_command(label="Salir", command=mainMenu.quit)
    mainMenu.add_cascade(label="Datos", menu=dataMenu)

    # Search
    searchMenu = Menu(mainMenu, tearoff=0)
    searchMenu.add_command(label="Título o introducción", command=searchByTitleOrIntro)
    searchMenu.add_command(label="Fecha", command=searchByDate)
    searchMenu.add_command(
        label="Características y título", command=searchByCharacteristicAndTitle
    )
    mainMenu.add_cascade(label="Buscar", menu=searchMenu)

    _ = root.config(menu=mainMenu)

    root.mainloop()


def searchByTitleOrIntro() -> None:
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


def searchByDate() -> None:
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


def searchByCharacteristicAndTitle() -> None:
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
    for Recipe in activities:
        listbox.insert(END, f"Titulo: {Recipe.title}")
        listbox.insert(END, "-" * len(Recipe.title))
        listbox.insert(END, f"Autor: {Recipe.author}")
        listbox.insert(END, f"Num Dinner: {Recipe.numDiners}")
        listbox.insert(END, f"Additional chars: {Recipe.additionalCharacteristics}")
        listbox.insert(END, f"Introducción: {Recipe.introduction}")
        listbox.insert(END, f"Date: {Recipe.updateDate}")
        listbox.insert(END, "")
        listbox.insert(END, "")
    listbox.pack(side=LEFT, fill=BOTH)
    _ = scrollbar.config(
        command=listbox.yview  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    )


def confirmLoad() -> None:
    answer = messagebox.askyesno(
        title="Confirmar",
        message="Estas seguro de que quieres cargar los datos?\nEsto puede tomar un rato.",
    )
    if answer:
        total = writeRecipes(processSite())
        _ = messagebox.showinfo(
            "Resultado de la carga", f"Se han añadido un total de {total} recetas"
        )
