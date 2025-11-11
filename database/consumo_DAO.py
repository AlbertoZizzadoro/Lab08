from database.DB_connect import ConnessioneDB
from model.consumo_DTO import Consumo

"""
    CONSUMO DAO
    Gestisce le operazioni di accesso alla tabella consumo.
"""

class ConsumoDAO:
    @staticmethod
    def get_consumi(id_impianto) -> list[Consumo] | None:

        """
        Restituisce tutti i consumi di un impianto
        :return: lista di tutti i Consumi di un certo impianto
        """
        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM consumo WHERE id_impianto = %s"""
        try:
            cursor.execute(query, (id_impianto,))
            for row in cursor:
                consumo = Consumo(
                    data=row["data"],
                    kwh=row["kwh"],
                    id_impianto=row["id_impianto"],
                )
                result.append(consumo)
        except Exception as e:
            print(f"Errore durante la query get_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
