from typing import Any

from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    _lista_consumi: list[Any]

    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()
        if self._impianti is None:
            print(" Errore durante il caricamento")


    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        self._lista_consumi = []
        for impianto in self._impianti:
            impianto.get_consumi()
            self._lista_consumi.append((impianto.nome, impianto.get_media(mese)))
        return self._lista_consumi
        


    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):



        # Se abbiamo superato i 7 giorni (siamo al "giorno 8")
        if giorno == 8:
            # Controlliamo se questa soluzione è migliore di quella ottima attuale
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)  # Salva una copia
            return


        # Per il giorno corrente, proviamo a visitare entrambi gli impianti
        for impianto in self._impianti:
            id_impianto_scelto = impianto.id

            # Calcoliamo il costo di questa mossa
            costo_passo = 0

            # 1. Costo variabile (consumo kWh)
            #    Recuperiamo il consumo dal dizionario (giorno è 1-based, l'indice della lista 0-based)
            costo_variabile = consumi_settimana[id_impianto_scelto][giorno - 1]
            costo_passo += costo_variabile

            # 2. Costo fisso (spostamento)
            #    Si paga 5€ se non è il primo giorno (ultimo_impianto != None)
            #    e se l'impianto è diverso da quello del giorno prima.
            if ultimo_impianto is not None and id_impianto_scelto != ultimo_impianto:
                costo_passo += 5  # Costo fisso per lo spostamento

            nuovo_costo_totale = costo_corrente + costo_passo


            # Se il costo parziale è già peggiore del costo ottimo trovato,

            if self.__costo_ottimo != -1 and nuovo_costo_totale >= self.__costo_ottimo:
                continue  # Salta questa scelta e prova l'altro impianto

            # RICORSIONE
            sequenza_parziale.append(id_impianto_scelto)
            self.__ricorsione(sequenza_parziale,
                              giorno + 1,  # Passa al giorno successivo
                              id_impianto_scelto,  # L'impianto attuale diventa "ultimo_impianto"
                              nuovo_costo_totale,
                              consumi_settimana)


            sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto."""

        consumi_settimana = {}


        for impianto in self._impianti:
            if impianto.lista_consumi is None:
                impianto.get_consumi()

            # Inizializza la lista dei consumi per i 7 giorni
            consumi_giornalieri = []

            # Cicla per i primi 7 giorni del mese
            for giorno in range(1, 8):
                consumo_giorno_trovato = None
                # Cerca il consumo per quel giorno specifico
                for consumo in impianto.lista_consumi:
                    if consumo.data.month == mese and consumo.data.day == giorno:
                        consumo_giorno_trovato = consumo.kwh
                        break  # Trovato, passa al giorno successivo

                # Aggiungi il consumo alla lista (o 0 se non dovesse esistere)
                if consumo_giorno_trovato is not None:
                    consumi_giornalieri.append(consumo_giorno_trovato)
                else:
                    consumi_giornalieri.append(0)
            # Assegna la lista dei 7 consumi all'ID dell'impianto
            consumi_settimana[impianto.id] = consumi_giornalieri

        return consumi_settimana

