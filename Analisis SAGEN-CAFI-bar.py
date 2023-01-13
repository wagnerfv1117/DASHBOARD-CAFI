#----------------------------------------------------------------------------------------
#1-Se procede a importar las  librerías necesarias, para hacer funcionar el algoritmo
#----------------------------------------------------------------------------------------
# Solución grafico de barras en Dash

import os # permite acceder a funcionalidades dependientes del Sistema Operativo. Sobre todo, aquellas que nos refieren información sobre el entorno del mismo y permiten manipular la estructura de archivos y carpetas
import pandas as pd # Se importa Pandas para estructurar los datos en forma de tabla
import plotly.express as px  # Se importa la librería Plotly quie muestre las graficas en el aplicativo web
import dash # se importa la librería, para que muestre el estilo web deseado, ya que integra componentes nod.js javascript y html
import dash_core_components as dcc # se importan los componentes y del nucleo de la librería para que pueda funcionar
import dash_html_components as html # se importa un componente html que tiene Dash para mostrar el estilo web 
from dash.dependencies import Input, Output # componentes Dash para procesar archivos de entrada y salida

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]#API  de Google, para personalizar el aplicativo Dashboard en cuestión de mascaras e interfaz grafica
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #variable para definir los estilos de fuentes
server = app.server #variable que convierte la maquina local en un servidor para ejecutar el aplicativo web
app.title = "Analisis de Gastos SAGEN" # se le asigna titulo a la APP para que la muestre en la pestaña del navegador que se use

# ------------------------------------------------------------------------------
#2-Se procede a limpiar/importar y cargar los datos 
#-------------------------------------------------------------------------------

df = pd.read_csv("cafi.csv") # variable que con la ayuda de la libreria pandas se puedan leer los datos de su fuente, en este caso archivo .csv 

df = df.groupby(['Financiacion', 'ANSI', 'Afectacion', 'Anualidad', 'COFI'])[['Monto']].mean() # metodo para agrupar y mostrar los datos conforme a las columnas clave seleccionada para el analisis; también para calcular estadisticamente la media
df.reset_index(inplace=True)#Reinicia el DataFrame y renombra un nuevo indice
print(df[:5])#Instrucción para que al momento de ejecutar el archivo python, muestre los primeros cinco registros, teniendo en cuenta que python empeiza a leer desde cero

# -------------------------------------------------------------------------------------
#3-Se procede a crear los elementos que componen la pagina web que mostrará la grafica 
# ------------------------------------------------------------------------------------- 
#Diseño de la aplicación tablero

app.layout = html.Div([

   
    html.H1("ANALISIS DE GASTOS SAGEN", style={'text-align': 'center'},className="header-title"),

    html.P(children="Analisis comparativo de gastos SAGEN/CAFI en el año 2021-2022, según su fuente de financiación", className="header-description", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year", #el Dropdown que es la lista desplegable para poder seleccionar los datos que se analizarán en el tablero
                 options=[
                     {"label": "2021", "value": 2021},
                     {"label": "2022", "value": 2022}], #etiquetas de los valores que se analizarán mediante graficas, y que serán mostradas en la lista desplegable
                 multi=False,
                 value=2021,
                 className="dropdown", # la clase que se le asigna
                 style={'width': "45%"} #el tamaño de la lista desplegable
                 
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
    
], className="body")# termina la estructura de la pagina web


# -----------------------------------------------------------------------------------
#4- Conectar el modulo de la librería Plotly con los componentes de la librería Dash
#-------------------------------------------------------------------------------------

@app.callback(
    [Output(component_id='output_container', component_property='children'),#la forma en como se seleccionarán los datos, en este caso lista desplegable
     Output(component_id='my_bee_map', component_property='figure')],# el metodo de salida, que es una figura
    [Input(component_id='slct_year', component_property='value')]# el metodo de entrada que hará el usuario al momento de dar clic en la lista desplegable
)# en la siguiente linea, se desarrollará la variable que se pueda actualizar las graficas en el tablero
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "El año seleccionado fue: {}".format(option_slctd) # mensaje debajo de la lista desplegable, enunciando un mensaje
    #a continuación se tomarán los datos ...
    dff = df.copy()
    dff = dff[dff["Anualidad"] == option_slctd]#al momento de dar clic en la lista desplegable, deberá mostrar el año a evaluar
    dff = dff[dff["Afectacion"] == "EGRESOS"] # data que se tomará para el analisis
#a continuación se define el tipo de grafica, que en este caso será de barra:
    fig = px.bar(
        data_frame=dff,
        x='Financiacion', #lo que se mostrará en el eje x
        y='Monto', # lo que se mostrará en el eje y
        hover_data=['Financiacion', 'Monto'], # la data seleccionada para ser graficada y analizada
        labels={'Monto': 'Monto'}, #etiquetas para los ejes x & y
        template='plotly_dark', #el o mascara en el que se mostrará la gráfica
        
    )

    return container, fig

# ------------------------------------------------------------------------------
#5- Poner en marcha la aplicación en el servidor o pc donde correrá
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

#-------------------------------------------------------------------------------