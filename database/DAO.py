from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select a.ID, a.IATA_CODE, a.AIRPORT, a.CITY, count(distinct f.AIRLINE_ID) as numCompagnie	
            from airports a, flights f 
            where (a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID)
            group by a.ID, a.IATA_CODE, a.AIRPORT, a.CITY
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(origin, destination):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select f.ORIGIN_AIRPORT_ID as a1, f.DESTINATION_AIRPORT_ID as a2, count(distinct f.ID) as numVoli
        from flights f
        where (f.ORIGIN_AIRPORT_ID = %s and f.DESTINATION_AIRPORT_ID = %s)
            or (f.DESTINATION_AIRPORT_ID  = %s and f.ORIGIN_AIRPORT_ID  = %s)
        """
        cursor.execute(query, (origin, destination, origin, destination, ))
        result = []
        for row in cursor:
            result.append((row["a1"], row["a2"], row["numVoli"]))
        cursor.close()
        conn.close()
        return result