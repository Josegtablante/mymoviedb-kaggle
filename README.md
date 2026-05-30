# 🎬 Análisis de Base de Datos de Películas

## 📋 Descripción del Proyecto

Este proyecto realiza un análisis exhaustivo de una base de datos de películas, enfocándose en las tendencias de los últimos 5 años (2021-2026). El análisis incluye visualizaciones interactivas, estadísticas detalladas y reportes sobre las películas más vistas, géneros favoritos por país y tendencias temporales.

---

## 📊 Origen de los Datos

### Fuente de Datos
- **Archivo:** `mymoviedb.csv`
- **Fuente:** The Movie Database (TMDb)
- **Formato:** CSV con delimitador punto y coma (;)
- **Codificación:** UTF-8
- **Total de registros:** 9,847 películas
- **Período analizado:** Últimos 5 años (2021-2026)
- **Registros en período:** 695 películas

### Estructura del Dataset

El archivo CSV contiene las siguientes columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `Release_Date` | Fecha | Fecha de estreno (formato: DD/MM/YYYY) |
| `Title` | Texto | Título de la película |
| `Overview` | Texto | Sinopsis/descripción de la película |
| `Popularity` | Numérico | Puntuación de popularidad de TMDb |
| `Vote_Count` | Entero | Número total de votos/calificaciones |
| `Vote_Average` | Decimal | Calificación promedio (0-10) |
| `Original_Language` | Código | Código ISO del idioma original (en, es, fr, ja, etc.) |
| `Genre` | Texto | Géneros separados por comas |
| `Poster_Url` | URL | Enlace a la imagen del póster |

---

## 🎯 Problemas que Soluciona

### 1. **Análisis de Tendencias de Mercado**
- Identifica las películas más exitosas en términos de audiencia
- Permite entender qué contenido genera mayor engagement
- Ayuda a productores y distribuidores a tomar decisiones informadas

### 2. **Análisis de Preferencias Culturales**
- Identifica géneros favoritos por región/país
- Revela diferencias culturales en preferencias cinematográficas
- Útil para estrategias de marketing localizado

### 3. **Análisis Temporal**
- Muestra tendencias de producción por año
- Identifica patrones estacionales de estrenos
- Permite predecir comportamientos futuros

### 4. **Evaluación de Calidad vs Popularidad**
- Correlaciona ratings con popularidad
- Identifica películas sobrevaloradas o infravaloradas
- Ayuda a entender qué factores impulsan el éxito

### 5. **Visualización de Datos Complejos**
- Transforma datos crudos en insights visuales
- Facilita la comunicación de hallazgos
- Permite análisis rápido de grandes volúmenes de información

---

## 🔧 Variables y Métricas Utilizadas

### Variables Principales

#### 1. **Vote_Count (Número de Votos)**
- **Tipo:** Variable cuantitativa discreta
- **Uso:** Indicador de popularidad y alcance de audiencia
- **Interpretación:** Mayor número = mayor exposición y engagement
- **Rango:** 0 - 25,011 votos en el dataset

#### 2. **Popularity (Popularidad)**
- **Tipo:** Variable cuantitativa continua
- **Uso:** Métrica compuesta de TMDb que considera múltiples factores
- **Factores incluidos:** Votos del día, vistas, usuarios que agregaron a listas, fecha de estreno
- **Interpretación:** Valor más alto = mayor relevancia actual
- **Rango:** 0 - 5,083,954 en el dataset

#### 3. **Vote_Average (Calificación Promedio)**
- **Tipo:** Variable cuantitativa continua
- **Uso:** Indicador de calidad percibida
- **Escala:** 0.0 - 10.0
- **Interpretación:** Refleja la satisfacción de la audiencia
- **Promedio del dataset:** 5.57/10

#### 4. **Release_Date (Fecha de Estreno)**
- **Tipo:** Variable temporal
- **Uso:** Análisis de tendencias temporales y estacionalidad
- **Formato:** DD/MM/YYYY
- **Transformaciones aplicadas:**
  - Extracción de año para análisis anual
  - Extracción de mes para análisis de estacionalidad
  - Filtrado por período (últimos 5 años)

#### 5. **Original_Language (Idioma Original)**
- **Tipo:** Variable categórica nominal
- **Uso:** Proxy para identificar país/región de producción
- **Valores principales:** en (inglés), es (español), fr (francés), ja (japonés), etc.
- **Mapeo a países:**
  - `en` → USA/UK
  - `es` → España/Latinoamérica
  - `fr` → Francia
  - `ja` → Japón
  - `ko` → Corea del Sur
  - `hi` → India
  - Y más...

#### 6. **Genre (Género)**
- **Tipo:** Variable categórica múltiple
- **Uso:** Clasificación temática de películas
- **Formato:** Valores separados por comas
- **Procesamiento:** Split y conteo individual de cada género
- **Géneros principales:** Drama, Comedy, Thriller, Action, Horror, etc.

### Variables Derivadas

#### 7. **Year (Año)**
- **Derivada de:** Release_Date
- **Uso:** Agrupación temporal para análisis de tendencias
- **Cálculo:** `df['Year'] = df['Release_Date'].dt.year`

#### 8. **Country (País)**
- **Derivada de:** Original_Language
- **Uso:** Agrupación geográfica
- **Cálculo:** Mapeo de códigos de idioma a nombres de países
- **Ejemplo:** `'en' → 'USA/UK'`

#### 9. **YearMonth (Año-Mes)**
- **Derivada de:** Release_Date
- **Uso:** Análisis de estacionalidad mensual
- **Cálculo:** `df['YearMonth'] = df['Release_Date'].dt.to_period('M')`

---

## 📁 Estructura del Proyecto

```
practica-kaggle/
│
├── mymoviedb.csv                          # Dataset original
│
├── README.md                              # Este archivo
│
├── Scripts de Análisis:
│   ├── analyze_movies.py                  # Script Python para análisis
│   ├── analyze_movies.ps1                 # Script PowerShell para análisis
│   └── create_visualizations.py           # Script Python para gráficas
│
├── Reportes Generados:
│   └── movie_analysis_report.txt          # Reporte textual completo
│
└── Visualizaciones Generadas:
    ├── movie_analysis_visualizations.png  # Dashboard principal (8 gráficas)
    ├── genre_distribution_by_country.png  # Distribución de géneros por país
    └── movie_releases_timeline.png        # Línea de tiempo de estrenos
```

---

## 🚀 Cómo Usar Este Proyecto

### Requisitos Previos

#### Software Necesario:
- **Python 3.12+** (instalado en el sistema)
- **PowerShell** (incluido en Windows)

#### Librerías Python:
```bash
pip install pandas matplotlib seaborn
```

### Ejecución del Análisis

#### Opción 1: Análisis con PowerShell (Sin gráficas)
```powershell
powershell -ExecutionPolicy Bypass -File analyze_movies.ps1
```
**Genera:** `movie_analysis_report.txt`

#### Opción 2: Análisis Completo con Python (Con gráficas)
```bash
python analyze_movies.py
python create_visualizations.py
```
**Genera:** Reporte + 3 archivos PNG con gráficas

### Personalización

#### Cambiar el Período de Análisis
En `create_visualizations.py`, línea 23:
```python
# Cambiar de 5 a N años
five_years_ago = datetime.now() - timedelta(days=5*365)
```

#### Agregar Nuevos Géneros al Mapeo
En `analyze_movies.ps1` o `create_visualizations.py`:
```python
language_to_country = {
    'en': 'USA/UK',
    'es': 'Spain/LatAm',
    # Agregar más aquí...
}
```

---

## 📊 Visualizaciones Generadas

### 1. Dashboard Principal (movie_analysis_visualizations.png)

Contiene 8 gráficas:

1. **Top 15 Películas Más Vistas** (Barras horizontales)
   - Métrica: Vote_Count
   - Ordenado: Descendente

2. **Top 15 Películas Más Populares** (Barras horizontales)
   - Métrica: Popularity
   - Ordenado: Descendente

3. **Películas por Año** (Barras verticales)
   - Muestra distribución temporal
   - Colores diferenciados por año

4. **Top 10 Géneros** (Gráfica circular/donut)
   - Porcentajes de cada género
   - Colores distintivos

5. **Películas por País** (Barras horizontales)
   - Top 10 países productores
   - Basado en idioma original

6. **Rating Promedio por Año** (Línea)
   - Tendencia de calidad temporal
   - Escala 0-10

7. **Top Géneros por País** (Barras agrupadas)
   - Compara top 3 países
   - Muestra preferencias culturales

8. **Rating vs Popularidad** (Scatter plot)
   - Correlación entre variables
   - Color indica Vote_Count

### 2. Distribución de Géneros por País (genre_distribution_by_country.png)

- 6 gráficas circulares (una por país)
- Top 6 países con más películas
- Muestra top 8 géneros por país
- Porcentajes claramente etiquetados

### 3. Línea de Tiempo (movie_releases_timeline.png)

- Gráfica de línea con área rellena
- Estrenos mensuales en el período
- Identifica picos de producción
- Útil para análisis de estacionalidad

---

## 📈 Resultados Clave del Análisis

### Hallazgos Principales:

1. **Dominio del Mercado Anglosajón**
   - 67% de las películas son en inglés
   - USA/UK lidera en producción

2. **Géneros Más Populares**
   - Drama (14.6%) es el género dominante
   - Comedy (12.5%) en segundo lugar
   - Thriller (10.8%) en tercer lugar

3. **Tendencia Temporal**
   - 2021 fue el año con más estrenos (478 películas)
   - Disminución en 2022 (208 películas)
   - Posible efecto post-pandemia

4. **Calidad vs Popularidad**
   - No siempre correlacionan
   - Películas populares no necesariamente mejor calificadas

5. **Preferencias Culturales**
   - Japón: 62.5% Animation
   - España/LatAm: 44.8% Comedy
   - Francia: 39.5% Drama

---

## ⚠️ Limitaciones del Dataset

### Datos Faltantes:

1. **Información de Actores/Cast**
   - No disponible en el dataset actual
   - Requiere enriquecimiento con TMDb API

2. **Información de Directores**
   - No incluida
   - Importante para análisis de autoría

3. **Presupuesto y Recaudación**
   - Datos financieros ausentes
   - Limitaría análisis de ROI

4. **Información de Streaming**
   - No indica plataformas de distribución
   - Relevante para análisis de mercado actual

### Consideraciones:

- **Sesgo de Idioma:** Predominio de películas en inglés
- **Sesgo Temporal:** Más datos recientes que históricos
- **Sesgo de Popularidad:** Películas populares sobre-representadas
- **Calidad de Datos:** Algunos registros pueden tener información incompleta

---

## 🔮 Posibles Extensiones

### Análisis Adicionales:

1. **Análisis de Sentimiento**
   - Procesar campo `Overview` con NLP
   - Correlacionar sentimiento con ratings

2. **Predicción de Éxito**
   - Modelo ML para predecir popularidad
   - Features: género, idioma, mes de estreno

3. **Análisis de Redes**
   - Si se agregan datos de cast
   - Colaboraciones entre actores/directores

4. **Análisis de Series Temporales**
   - Forecasting de tendencias
   - Predicción de géneros emergentes

5. **Clustering de Películas**
   - Agrupación por características similares
   - Sistema de recomendación

---

## 🛠️ Tecnologías Utilizadas

### Lenguajes:
- **Python 3.12** - Análisis y visualización
- **PowerShell** - Análisis alternativo en Windows

### Librerías Python:
- **pandas 3.0.3** - Manipulación de datos
- **matplotlib 3.10.9** - Visualizaciones base
- **seaborn 0.13.2** - Visualizaciones estadísticas avanzadas
- **numpy 2.4.6** - Operaciones numéricas

### Herramientas:
- **VS Code** - Editor de código
- **Git** - Control de versiones (recomendado)

---

## 👥 Autor

**Jose Tablante**
- Ubicación: Buenos Aires, Argentina
- Proyecto: Práctica de Análisis de Datos con IA

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos y de investigación.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Contacto

Para preguntas o sugerencias sobre este proyecto, por favor abre un issue en el repositorio.

---

## 🙏 Agradecimientos

- **The Movie Database (TMDb)** por proporcionar los datos
- **Comunidad de Python** por las excelentes librerías de análisis de datos
- **Matplotlib y Seaborn** por las herramientas de visualización

---

**Última actualización:** Mayo 2026