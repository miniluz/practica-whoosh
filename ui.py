from tkinter import (
    BOTH,
    BOTTOM,
    END,
    LEFT,
    RIGHT,
    X,
    Y,
    Button,
    Entry,
    Label,
    Listbox,
    Menu,
    Scrollbar,
    Spinbox,
    Tk,
    Toplevel,
    messagebox,
)

from typing import Callable
from datetime import date, datetime
from database import Activity


def main_window(
    load: Callable[[], None],
    getTotalActivities: Callable[[], int],
    getAllActivities: Callable[[], list[Activity]],
    getNextActivities: Callable[[], list[Activity]],
    getMorningActivities: Callable[[], list[Activity]],
    getPlaces: Callable[[], set[str]],
    getActivitiesByPlace: Callable[[str], list[Activity]],
    getActivitiesByDate: Callable[[date], list[Activity]],
) -> None:
    root = Tk()

    mainMenu = Menu(root)

    # Data
    dataMenu = Menu(mainMenu, tearoff=0)
    dataMenu.add_command(
        label="Cargar", command=lambda: confirmLoad(load, getTotalActivities)
    )
    dataMenu.add_command(label="Salir", command=mainMenu.quit)
    mainMenu.add_cascade(label="Datos", menu=dataMenu)

    # List
    listMenu = Menu(mainMenu, tearoff=0)
    listMenu.add_command(
        label="Todas las actividades",
        command=lambda: listActivities(getAllActivities()),
    )
    listMenu.add_command(
        label="Próximas actividades",
        command=lambda: listActivities(getNextActivities()),
    )
    mainMenu.add_cascade(label="Listar", menu=listMenu)

    # Search
    searchMenu = Menu(mainMenu, tearoff=0)
    searchMenu.add_command(
        label="Actividades por lugar",
        command=lambda: searchByPlace(getPlaces, getActivitiesByPlace),
    )
    searchMenu.add_command(
        label="Actividades por fecha", command=lambda: searchByDate(getActivitiesByDate)
    )
    searchMenu.add_command(
        label="Actividades matinales",
        command=lambda: listActivities(getMorningActivities()),
    )
    mainMenu.add_cascade(label="Buscar", menu=searchMenu)

    _ = root.config(menu=mainMenu)

    root.mainloop()


def searchByPlace(
    getPlaces: Callable[[], set[str]],
    getActivitiesByPlace: Callable[[str], list[Activity]],
) -> None:
    places = getPlaces()
    searchPicker(
        "lugar", list(places), lambda place: listActivities(getActivitiesByPlace(place))
    )


def searchByDate(
    getByDate: Callable[[date], list[Activity]],
) -> None:
    top = Toplevel()
    top.title("Filtrar por fecha")
    top.geometry("350x100")
    L1 = Label(top, text="Introduzca la fecha formato DD/MM/YYYY")
    L1.pack(side=LEFT)
    textEntry = Entry(top)
    textEntry.pack(fill=X, side=RIGHT)
    _ = textEntry.bind(
        "<Return>",
        lambda _: listActivities(
            getByDate(
                datetime(
                    int(textEntry.get().split("/")[2]),
                    int(textEntry.get().split("/")[1]),
                    int(textEntry.get().split("/")[0]),
                ).date()
            )
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


def listActivities(activities: list[Activity]) -> None:
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
        "Resultado de la carga", f"Se han añadido un total de {total} actividades"
    )
