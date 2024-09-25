from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from querys import consulta

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/consulta")
async def get_query(parametro: str = Query(None, description="Parámetro para filtrar consulta")):
    conn = psycopg2.connect(
        dbname="refsa_test",
        user="postgres",
        password="postgres",
        host="172.0.1.18",
        port="5432"
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql = consulta
    cursor.execute(sql, (parametro,))
    result = cursor.fetchall()
    json_response = {}
    for row in result:
        ojtid = row['ojtid']
        json_response[ojtid] = {
            "Suministro": row[17],
            "Titular": row[20],
            "Domicilio": row[27]
        }
    cursor.close()
    conn.close()
    return json_response