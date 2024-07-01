from dataclasses import dataclass


@dataclass
class Airport:
    ID: int
    IATA_CODE: str
    AIRPORT: str
    CITY: str
    numCompagnie: int

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return self.ID == other.ID

    def __str__(self):
        return f"{self.CITY} ({self.AIRPORT})"
