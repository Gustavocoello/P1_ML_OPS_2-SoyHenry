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
# Datos
day = pd.read_parquet("day.parquet")
per_month = pd.read_parquet("mes.parquet")
matriz = pd.read_parquet("ml1.parquet")
# Crear el CountVectorizer y transformar los datos
cv = CountVectorizer(max_features = 3000, stop_words= 'english')
vectors = cv.fit_transform(matriz['tags']).toarray()
# Calcular la similitud  del coseno
similarity = cosine_similarity(vectors)

@app.get("/")
def index():
    return "Hola, mundo"

@app.get("/recomendacion/")
async def recomendacion(movie):
    movie_index = matriz[matriz['name'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
   
    recommend_movies = [matriz.iloc[i[0]]['name'] for i in movies_list]
    return {"Recommend_movies": recommend_movies}

@app.get("/cantidad_filmaciones_mes/")
async def cantidad_filmaciones_mes(Mes):
    
    Mes = Mes.capitalize()
    
    mes_filtrado = per_month[per_month['mes_name'] == Mes]
    
    if not mes_filtrado.empty:
        cantidad = mes_filtrado['count'].values[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {Mes}"
    
@app.get("/cantidad_filmaciones_dia/")    
async def cantidad_filmaciones_dia(dia):
    
    dia = dia.capitalize()
    
    mes_filtrado = day[day['dia_name'] == dia]
    
    if not mes_filtrado.empty:
        cantidad = mes_filtrado['count'].values[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el día de {dia}" 