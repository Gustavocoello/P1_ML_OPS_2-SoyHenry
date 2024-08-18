from fastapi import FastAPI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import os 


app = FastAPI()

# Puerto de fastapi 127.0.0.1:8000
# pi-env\scripts\Activate.bat (Activar el entorno virtual)
# uvicorn main:app --reload (Activar fastApi)

# Cambiar el directorio de trabajo a la carpeta 'Fastapi-deploy'
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
def index():
    return "Hola, mundo"

@app.get("/recomendacion/")
async def recomendacion(name):
    movies = pd.read_csv("movies.csv")
    
    indice = movies[movies['movie'] == name].index[0]
    recomendacion = movies.iloc[indice]['recomendations']
    return recomendacion
    

@app.get("/cantidad_filmaciones_mes/")
async def cantidad_filmaciones_mes(Mes):
    per_month = pd.read_parquet("mes.parquet")
    Mes = Mes.capitalize()
    
    mes_filtrado = per_month[per_month['mes_name'] == Mes]
    
    if not mes_filtrado.empty:
        cantidad = mes_filtrado['count'].values[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {Mes}"
    
@app.get("/cantidad_filmaciones_dia/")    
async def cantidad_filmaciones_dia(dia):
    
    day = pd.read_parquet("day.parquet")
    dia = dia.capitalize()
    
    mes_filtrado = day[day['dia_name'] == dia]
    
    if not mes_filtrado.empty:
        cantidad = mes_filtrado['count'].values[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el día de {dia}" 