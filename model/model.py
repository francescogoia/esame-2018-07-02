import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._grafo = nx.Graph()

    def _crea_grafo(self, num_compagnie):
        self._grafo.clear()
        aeroporti = DAO.getAllAirports()
        self._nodes = []
        for a in aeroporti:
            if a.numCompagnie >= num_compagnie:
                self._grafo.add_node(a)
                self._nodes.append(a)
                self._idMap[a.ID] = a
        for u in self._nodes:
            for v in self._nodes:
                arco = DAO.getEdge(u.ID, v.ID)
                if arco[0][0] != None:
                    self._grafo.add_edge(u, v, weight=arco[0][2])

    def get_dettagli_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_connessi(self, nodo):
        vicini = self._grafo.neighbors(nodo)
        result = []
        for c in vicini:
            numVoli = self._grafo[nodo][c]["weight"]
            result.append((c, numVoli))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def handle_percorso(self, partenza, arrivo, lunghezza):
        self._bestPath = []
        self._bestPeso = 0
        self._ricorsione(partenza, arrivo, [], lunghezza)
        return self._bestPath, self._bestPeso

    def _ricorsione(self, nodo, arrivo, parziale, lunghezza):
        pesoParziale = self._getPesoParziale(parziale)
        if len(parziale) > 0:
            if pesoParziale > self._bestPeso and parziale[-1][1] == arrivo:
                self._bestPeso = pesoParziale
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == lunghezza:
            return          # non posso andare oltre, numero max di tratte raggiunto
        vicini = self._grafo.neighbors(nodo)
        for v in vicini:
            if self.filtroNodi(v, parziale):
                pesoArco = self._grafo[nodo][v]["weight"]
                parziale.append((nodo, v, pesoArco))
                self._ricorsione(v, arrivo, parziale, lunghezza)
                parziale.pop()


    def filtroNodi(self, nodo, parziale):
        for a in parziale:
            if a[0] == nodo or a[1] == nodo:
                return False
        return True

    def _getPesoParziale(self, parziale):
        totP = 0
        for a in parziale:
            totP += a[2]
        return totP
