import copy

from database.DAO import DAO

class Model:
    def __init__(self):
        self._limitCase = -1
        self._mostRecent = -1

        self._solBest = []
        self._coinvoltiMax = -1

        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc, maxH)
        self._solBest = []
        self._coinvoltiMax = -1
        self._limitCase = self.search_limit_case(maxY, self._listEvents)
        self.ricorsione([], maxH, maxY, self._listEvents)
        return self._solBest, self._coinvoltiMax, self.sommaOreParziale(self._solBest)



    def ricorsione(self, parziale, maxH, maxY, zone_events):
        if self.sommaOreParziale(parziale) > maxH and len(parziale) != 0:
            print(self.sommaOreParziale(parziale))
            parziale.pop()
            print(parziale)
            print(self.sommaOreParziale(parziale))
            coinvolti = self.sommaCoinvoltiParziale(parziale)
            if coinvolti > self._coinvoltiMax:
                self._coinvoltiMax = coinvolti
                self._solBest = copy.deepcopy(parziale)

        elif self.sommaOreParziale(parziale) == self._limitCase:
            coinvolti = self.sommaCoinvoltiParziale(parziale)
            if coinvolti > self._coinvoltiMax:
                self._coinvoltiMax = coinvolti
                self._solBest = copy.deepcopy(parziale)

        else:
            for event in zone_events:
                if len(parziale) == 0:
                    parziale.append(event)
                    self._mostRecent = int(event.date_event_began.strftime("%Y"))
                    self.ricorsione(parziale, maxH, maxY, zone_events)

                else:
                    if event not in parziale and (int(event.date_event_began.strftime("%Y")) >= self._mostRecent
                            and int(event.date_event_began.strftime("%Y")) - self._mostRecent <= maxY):
                        parziale.append(event)
                        self.ricorsione(parziale, maxH, maxY, zone_events)

            if len(parziale) != 0:
                parziale.pop()

    def search_limit_case(self, maxY, zone_events):
        limit_list = []
        for event in zone_events:
            if len(limit_list) == 0:
                limit_list.append(event)
            elif (int(event.date_event_began.strftime("%Y")) - int(limit_list[0].date_event_began.strftime("%Y"))) <= maxY:
                limit_list.append(event)
        return self.sommaOreParziale(limit_list)







    def loadEvents(self, nerc, maxH):
        self._listEvents = DAO.getAllEvents(nerc, maxH)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

    def durataEventoInOre(self, event):
        differenza = event.date_event_finished - event.date_event_began
        differenza_in_ore = differenza.total_seconds() / 3600
        return differenza_in_ore


    def sommaOreParziale(self, parziale):
        ore_tot = 0
        for event in parziale:
            ore_tot += self.durataEventoInOre(event)
        return ore_tot

    def sommaCoinvoltiParziale(self, parziale):
        coinvolti = 0
        for event in parziale:
            coinvolti += event.customers_affected
        return coinvolti


