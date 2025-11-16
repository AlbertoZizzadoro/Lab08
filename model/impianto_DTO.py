from dataclasses import dataclass
from database.consumo_DAO import ConsumoDAO

'''
    DTO (Data Transfer Object) dell'entità Impianto
'''

@dataclass()
class Impianto:
    id: int
    nome: str
    indirizzo: str
    # RELAZIONI
    lista_consumi: list = None

    def get_consumi(self):
        """
        Aggiorna e Restituisce la lista di consumi (self.lista_consumi) associati all'impianto
        :return: lista di oggetti Consumo relativi all'impianto
        """
        self.lista_consumi = []
        for consumo in ConsumoDAO.get_consumi(self.id):
            self.lista_consumi.append(consumo)
        return self.lista_consumi


    def __eq__(self, other):
        return isinstance(other, Impianto) and self.id == other.id

    def __repr__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

    def get_media(self, mese:int):
        if self.lista_consumi is None:
            self.get_consumi()

        consumi_mese = []
        for consumo in self.lista_consumi:
            if consumo.data.month == mese:
                consumi_mese.append(consumo.kwh)


        if len(consumi_mese) > 0:
            return sum(consumi_mese) / len(consumi_mese)
        else:
            return 0



