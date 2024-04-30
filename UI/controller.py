import flet as ft
from UI import view

from model.nerc import Nerc


class Controller:
    def __init__(self, view: view.View, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        nerc = self._view._ddNerc.value
        yearMax = self._view._txtYears.value
        hourMax = self._view._txtHours.value
        if nerc == "":
            self._view.create_alert("Choose a NERC")
        elif yearMax == "" or not yearMax.isnumeric() or int(yearMax) < 1:
            self._view.create_alert("Choose a correct value for Years")
        elif hourMax == "" or not hourMax.isnumeric() or int(hourMax) < 1:
            self._view.create_alert("Choose a correct value for Hours")
        else:
            self._view.txt_result.controls.clear()
            nerc = self._view._ddNerc.value
            yearMax = int(self._view._txtYears.value)
            hourMax = int(self._view._txtHours.value)
            result = self._model.worstCase(nerc, yearMax, hourMax)
            self._view.txt_result.controls.append(ft.Text(f"Tot people affected: {result[1]}"))
            self._view.txt_result.controls.append(ft.Text(f"Tot hours of outage: {result[2]}"))
            for event in result[0]:
                self._view.txt_result.controls.append(ft.Text(event.__str__()))
            self._view.update_page()






    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.id, text=n.value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
