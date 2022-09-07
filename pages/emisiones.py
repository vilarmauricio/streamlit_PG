
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import lib.graficos as graficos
import lib.filtros as filtro 

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

    #listas
    
    lista_periodos = filtro.lista_anios(df_sin_america_del_norte, 'Anio')
    sel_fecha_fin = lista_periodos[-1]
    lista_periodo_min = [x for x in range(lista_periodos[0], sel_fecha_fin+1)]
    
    sel_fecha_inicio = st.sidebar.selectbox("Seleccionar Fecha Inicio", lista_periodo_min)
    lista_periodo_max = [x for x in range(sel_fecha_inicio, lista_periodos[-1]+1)]

    sel_fecha_fin = st.sidebar.selectbox("Seleccionar Fecha Fin", reversed(lista_periodo_max))
    st.sidebar.write(sel_fecha_inicio, '-', sel_fecha_fin)
    #fecha_tupla = st.sidebar.slider('Seleccione Periodo',  min_value= lista_periodos[0], max_value= lista_periodos[-1], value= (lista_periodos[0], lista_periodos[-1]))
    #st.sidebar.write(fecha_tupla)
    #st.sidebar.write(fecha_fin)

    # Seleccion paises
    region = st.sidebar.radio("Seleccione Region", ('Latinoamerica', 'Personalizado'))
    lista_paises = filtro.lista_paises(df_sin_america_del_norte, 'pais')
    if region == 'Latinoamerica':
        seleccion_paises =  lista_paises
    #elif region == 'Toda America':
        #seleccion_paises = lista_paises
    elif region == 'Personalizado':
        seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises)


    #seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises, default= lista_paises)
    df_ultima_observacion = df_ultima_observacion[df_ultima_observacion['Pais'].isin(seleccion_paises)]

    # Datos Grafico
    df_agrupacion_sum = df[df['Pais'].isin(seleccion_paises)].groupby('Anio', as_index= False).sum()
    df_agrupacion_promedio = df[df['Pais'].isin(seleccion_paises)].groupby('Anio', as_index= False).mean()
    #df_agrupacion['Anio'] = pd.to_datetime(df_agrupacion['Anio'], format= '%Y')

    #st.image('./images/ComisionLat1.png')
    st.image('./images/kpi6_1.png')


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
        #fecha_tupla = st.slider('Seleccione Periodos',  min_value= lista_periodos[0], max_value= lista_periodos[-1], value= (lista_periodos[0], lista_periodos[-1]))
        with col_mapa:
        # tab_latino_america, tab_mundo = st.tabs(["Latinoamerica", "Mundial"])
            
            #with tab_latino_america:
            
            #   figura_mapa = grafico_mapa(df_ultima_observacion, "south america")
            #  st.plotly_chart(figura_mapa)

            #with tab_mundo:
                st.subheader('Mapa Emisiones CO2 - Latinoamerica')
                figura_mapa = graficos.grafico_mapa_emisiones(df_ultima_observacion, 'Emisiones_de_CO2', "ISO", "CO2", "Pais")
                st.plotly_chart(figura_mapa,  use_container_width=True)


        with col_grafico:
                st.subheader('Emisiones CO2 - Agrupacion Anual')
                try:
                    figura2 = graficos.grafico_linea_emisiones(df_agrupacion_sum, 'Anio', 'Emisiones_de_CO2', 'Año', 'Emision CO2 (Mill Tn)')
                    st.plotly_chart(figura2,  use_container_width=True)
                except ValueError:
                    st.error("Seleccionar por lo menos 1 (uno) Pais")
            
        #st.sidebar.title('Configuracion Graficos de Barras')          
        
        
        col_top, col_down = st.columns((0.5,0.5))

        with col_top:
            
            st.subheader('Paises con Mayor Emision CO2')
            try:
                opciones_mayor = st.slider('Seleccionar cantidad de Paises Top', 1, 10, 5)
                df_top = df_ultima_observacion.sort_values(by = 'Emisiones_de_CO2' ,ascending= False).head(opciones_mayor)
                figura_top = graficos.grafico_barras_emisiones(df_top, 'Pais', 'Emisiones_de_CO2', 'Pais', 'Emision CO2 (Mill Tn)')
                st.plotly_chart(figura_top,  use_container_width=True)
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")
        
        with col_down:
            st.subheader('Paises con Menor Emision CO2')
            try:
                opciones_menor = st.slider('Seleccionar cantidad de Paises', 1, 10, 5)
                df_down = df_ultima_observacion.sort_values(by = 'Emisiones_de_CO2' ,ascending= True).head(opciones_menor)   
            
                figura_down = graficos.grafico_barras_emisiones(df_down, 'Pais', 'Emisiones_de_CO2', 'Pais', 'Emision CO2 (Mill Tn)')
                st.plotly_chart(figura_down,  use_container_width=True)
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")


if __name__ == '__main__':
    main()
