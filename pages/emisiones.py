
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import lib.graficos as graficos 

# Configuracion Pagina
st.set_page_config(
     page_title="KPI Emisiones CO2",
     page_icon="🌍",
     layout="wide",
     initial_sidebar_state= "collapsed",
)

# Funcion para definir hoja de estilo
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("./styles/css_emisiones.css")


#@st.cache
def crear_dataframe(nombre_archivo):
    df = pd.read_csv('./dataset/'+nombre_archivo)
    return df

#Colores graficos
color_fuente_graf = '#407F46'
color_fuente_titulo_graf = '#407F46'
color_fondo_graf = '#EAEAEA'
color_marco_graf = '#FFFFFF'
color_dibujo_graf = 'rgba(92,175,138, 1)'
color_escala_mapa = 'Blugrn'
transp = 'rgba(0,0,0,0)' 


def main():


    df = crear_dataframe('emisiones_cod.csv')
    df_compromisos = crear_dataframe('compromisos.csv')
    df_compromisos.drop('Pais', axis= 1, inplace= True)
    df_compromisos.rename(columns= {'Cod_Pais' : 'ISO'}, inplace= True)

    # Calculos
    df_sin_america_del_norte = df[df['Región'] != 'América del Norte']
    df_merge = pd.merge(df_sin_america_del_norte, df_compromisos, how= 'left', on= 'ISO')
    df_merge['reduccion'] = (df_merge['Emisiones_de_CO2']* df_merge['Compromiso'])/100

    anio_maximo = df_merge.Anio.max()
    df_ultima_observacion = df_merge[df_merge['Anio'] == anio_maximo]
    suma_emisiones_actual = df_ultima_observacion.Emisiones_de_CO2.sum()

    # Calculo Emision Objetivo
    df_inicio_medicion = df_merge[df_merge['Anio'] == 2015]
    suma_emisiones_inicial = df_inicio_medicion.Emisiones_de_CO2.sum()
    suma_reducciones = df_inicio_medicion.reduccion.sum()
    emisiones_objetivo = suma_emisiones_inicial - suma_reducciones
    reduccion_pct = (suma_reducciones/suma_emisiones_inicial)*100 

    # Porcentaje KPi

    kpi_pct= round((suma_emisiones_inicial-suma_emisiones_actual)/(suma_reducciones)*100) #usare este kpi



    with st.sidebar:
        st.button('Introduccion')
        #st.button('Hoja 1')
        #st.button('hoja 2')

    #lista_paises = sorted(df.Pais.unique())
    lista_paises_latinoamerica = sorted(df_sin_america_del_norte.Pais.unique())


    # Seleccion paises
    region = st.sidebar.radio("Seleccione Region", ('Latinoamerica', 'Personalizado'))

    if region == 'Latinoamerica':
        seleccion_paises =  lista_paises_latinoamerica
    #elif region == 'Toda America':
        #seleccion_paises = lista_paises
    elif region == 'Personalizado':
        seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises_latinoamerica)


    #seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises, default= lista_paises)
    df_ultima_observacion = df_ultima_observacion[df_ultima_observacion['Pais'].isin(seleccion_paises)]

    # Datos Grafico
    df_agrupacion_sum = df[df['Pais'].isin(seleccion_paises)].groupby('Anio', as_index= False).sum()
    df_agrupacion_promedio = df[df['Pais'].isin(seleccion_paises)].groupby('Anio', as_index= False).mean()
    #df_agrupacion['Anio'] = pd.to_datetime(df_agrupacion['Anio'], format= '%Y')

    st.image('./images/ComisionLat1.png')
    st.image('./images/kpi6_1.png')


    # card(title="Hello World!", text="Some description", image="http://placekitten.com/200/300")

    progreso = 60

    #Contenedor
    with st.container():
        #Columnas
        col1, col2, col3 = st.columns((3,3,3))

        with col1:
            st.header("Cumplimiento KPI's")
            st.title(str(kpi_pct) + "%")
            st.progress(kpi_pct)
            

        with col2:
            st.header("Emisiones Actuales CO2")
            st.title(str(round(suma_emisiones_actual)))
            

        with col3:
            st.header("Emisiones Objetivo CO2")
            st.title(str(round(emisiones_objetivo)))
            
        
        col_mapa, col_grafico = st.columns((2,2))

        with col_mapa:
        # tab_latino_america, tab_mundo = st.tabs(["Latinoamerica", "Mundial"])
            
            #with tab_latino_america:
            
            #   figura_mapa = grafico_mapa(df_ultima_observacion, "south america")
            #  st.plotly_chart(figura_mapa)

            #with tab_mundo:
                #st.subheader('Mapa Emisiones CO2 - Latinoamerica')
                figura_mapa = graficos.grafico_mapa(df_ultima_observacion, 'Emisiones_de_CO2', "ISO","world", "Mapa Cromatico - EmisionesCO2/Pais", "CO2", "Pais", color_escala_mapa, color_fuente_graf, color_marco_graf, color_fondo_graf, color_fuente_titulo_graf)
                st.plotly_chart(figura_mapa,  use_container_width=True)


        with col_grafico:
                #st.subheader('Emisiones CO2 - Agrupacion Anual')
                try:
                    figura2 = graficos.grafico_linea(df_agrupacion_sum, 'Anio', 'Emisiones_de_CO2', "Emisiones CO2 Total", 'Año', 'Emision CO2 (Mill Tn)', color_fuente_graf, color_marco_graf, color_fondo_graf, color_fuente_titulo_graf, color_dibujo_graf)
                    st.plotly_chart(figura2,  use_container_width=True)
                except ValueError:
                    st.error("Seleccionar por lo menos 1 (uno) Pais")
            
        #st.sidebar.title('Configuracion Graficos de Barras')          
        
        
        col_top, col_down = st.columns((0.5,0.5))

        with col_top:
            
            #st.subheader('Paises con Mayor Emision CO2')
            try:
                opciones_mayor = st.slider('Seleccionar cantidad de Paises Top', 1, 10, 5)
                df_top = df_ultima_observacion.sort_values(by = 'Emisiones_de_CO2' ,ascending= False).head(opciones_mayor)
                figura_top = graficos.grafico_barras(df_top, 'Pais', 'Emisiones_de_CO2', 'Paises con Mayor Emision CO2', 'Pais', 'Emision CO2 (Mill Tn)', color_fuente_graf, color_marco_graf, color_fondo_graf, color_fuente_titulo_graf, color_dibujo_graf)
                st.plotly_chart(figura_top,  use_container_width=True)
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")
        
        with col_down:
            #st.subheader('Paises con Menor Emision CO2')
            try:
                opciones_menor = st.slider('Seleccionar cantidad de Paises', 1, 10, 5)
                df_down = df_ultima_observacion.sort_values(by = 'Emisiones_de_CO2' ,ascending= True).head(opciones_menor)   
            
                figura_down = graficos.grafico_barras(df_down, 'Pais', 'Emisiones_de_CO2', 'Paises con Menor Emision CO2', 'Pais', 'Emision CO2 (Mill Tn)', color_fuente_graf, color_marco_graf, color_fondo_graf, color_fuente_titulo_graf, color_dibujo_graf)
                st.plotly_chart(figura_down,  use_container_width=True)
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")


if __name__ == '__main__':
    main()
