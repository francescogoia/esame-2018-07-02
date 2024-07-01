import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizza(self, e):
        numCompagnie = self._view._txtInNumC.value
        try:
            intNumC = int(numCompagnie)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore, inserire un valore numerico in 'Num compagnie'"))
            self._view.update_page()
            return
        self._model._crea_grafo(intNumC)
        nNodi, nArchi = self._model.get_dettagli_grafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato. \n"
                                                      f"Grafo con {nNodi} nodi e {nArchi} archi."))
        self._view._DD_aeroprtiPartenza.disabled = False
        self._view._DD_aeroprtiArrivo.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._txtInNumTratte.disabled = False
        self._view._btnCercaItinerario.disabled = False
        self._fillDDAeroporti()
        self._view.update_page()

    def _fillDDAeroporti(self):
        aeroporti = self._model._nodes
        for a in aeroporti:
            self._view._DD_aeroprtiPartenza.options.append(
                ft.dropdown.Option(data=a, text=f"{a.CITY} {a.IATA_CODE}", on_click=self._selectPartenza))
            self._view._DD_aeroprtiArrivo.options.append(
                ft.dropdown.Option(data=a, text=f"{a.CITY} {a.IATA_CODE}", on_click=self._selectArrivo))
        self._view.update_page()

    def _selectPartenza(self, e):
        if e.control.data is None:
            self._choicePartenza = None
        else:
            self._choicePartenza = e.control.data

    def _selectArrivo(self, e):
        if e.control.data is None:
            self._choiceArrivo = None
        else:
            self._choiceArrivo = e.control.data

    def handleConnessi(self, e):
        connessi = self._model.get_connessi(self._choicePartenza)
        self._view.txt_result.controls.append(ft.Text(f"Connessi ad {self._choicePartenza}: {len(connessi)} aeroporti connessi."))
        for c in connessi:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]}: {c[1]} voli"))
        self._view.update_page()

    def handleCercaItinerario(self, e):
        lunghezzaMax = self._view._txtInNumTratte.value
        try:
            intLunMax = int(lunghezzaMax)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore, inserire un valore numerico in 'Numero tratte max'"))
            self._view.update_page()
            return
        percorso, peso = self._model.handle_percorso(self._choicePartenza, self._choiceArrivo, intLunMax)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il percorso di lunghezza {intLunMax} trovato ha peso: {peso}"))
        for p in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{p[0]} ---> {p[1]}: {p[2]}"))
        self._view.update_page()


