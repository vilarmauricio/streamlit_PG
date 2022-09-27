
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

    df_proyecciones = crear_dataframe('predicciones.csv')
    df = crear_dataframe('emisiones_cod.csv')
    df_compromisos = crear_dataframe('Porcentraje compromiso2.csv')
    df_compromisos.drop('Pais', axis= 1, inplace= True)
    df_compromisos.rename(columns= {'Cod_Pais' : 'ISO'}, inplace= True)

    

    # Calculos
    df_sin_america_del_norte = df[df['Región'] != 'América del Norte']
    df_merge = pd.merge(df_sin_america_del_norte, df_compromisos, how= 'left', on= 'ISO')
    df_merge['reduccion'] = (df_merge['Emisiones_de_CO2']* df_merge['Compromiso30'])/100

    anio_maximo = df_merge.Anio.max()
    anio_minimo = df_merge.Anio.min()
    anio_inicio_kpi = 2015
    sel_fecha_inicio = anio_inicio_kpi -10
    sel_fecha_fin = anio_maximo

    # Datos ultimo registro
    df_ultima_observacion = df_merge[df_merge['Anio'] == anio_maximo]
    suma_emisiones_actual = df_ultima_observacion.Emisiones_de_CO2.sum()

    # Datos Pirmer registro
    df_primer_observacion = df_merge[df_merge['Anio'] == anio_inicio_kpi]
    suma_emisiones_inicial = df_primer_observacion.Emisiones_de_CO2.sum()


    
    st.sidebar.write('Para una correcta visualización, utilizar modo "Light". (Menu derecho-superior/ Settings/ Theme Choose: Light)')
    #listas

    lista_periodos = filtro.lista_anios(df_sin_america_del_norte, 'Anio')
    periodo = st.sidebar.radio("Seleccione Periodo", ('Predeterminado', 'Personalizado'))
    if periodo == 'Predeterminado':
        st.sidebar.write('Periodo predeterminado: ', sel_fecha_inicio, '-', lista_periodos[-1])
    
    elif periodo == 'Personalizado':
        sel_fecha_fin = lista_periodos[-1]
        lista_periodo_min = [x for x in range(lista_periodos[0], sel_fecha_fin+1)]
        sel_fecha_inicio = st.sidebar.selectbox("Seleccionar Fecha Inicio", lista_periodo_min)
        lista_periodo_max = [x for x in range(sel_fecha_inicio, lista_periodos[-1]+1)]
        sel_fecha_fin = st.sidebar.selectbox("Seleccionar Fecha Fin", reversed(lista_periodo_max))
    #st.sidebar.write(sel_fecha_inicio, '-', sel_fecha_fin)
    #fecha_tupla = st.sidebar.slider('Seleccione Periodo',  min_value= lista_periodos[0], max_value= lista_periodos[-1], value= (lista_periodos[0], lista_periodos[-1]))
    #st.sidebar.write(fecha_tupla)
    #st.sidebar.write(fecha_fin)

    # Calculo Emision Objetivo
    df_inicio_medicion = df_merge[df_merge['Anio'] == anio_inicio_kpi]
    suma_emisiones_inicial = df_inicio_medicion.Emisiones_de_CO2.sum()
    suma_reducciones = df_inicio_medicion.reduccion.sum()
    emisiones_objetivo = suma_emisiones_inicial - suma_reducciones
    reduccion_pct = (suma_reducciones/suma_emisiones_inicial)*100 

    # Porcentaje KPi

    kpi_pct= round((suma_emisiones_inicial-suma_emisiones_actual)/(suma_reducciones)*100) #usare este kpi

    #Proyecciones
    df_proyecciones = df_proyecciones[df_proyecciones['dataset'] == 'emisiones_co2']
    valor_proyeccion = df_proyecciones.prediccion.values[0]
    valor_proyeccion_baja = df_proyecciones.inc_baja.values[0]
    valor_proyeccion_alta = df_proyecciones.inc_alta.values[0]

    # Calculos compromisos
    df_inicio_medicion['val20']= df_inicio_medicion['Emisiones_de_CO2']-((df_inicio_medicion['Compromiso20']*df_inicio_medicion['Emisiones_de_CO2'])/100)
    df_inicio_medicion['val30']= df_inicio_medicion['Emisiones_de_CO2']-((df_inicio_medicion['Compromiso30']*df_inicio_medicion['Emisiones_de_CO2'])/100)
    dfcomp = df_inicio_medicion.filter(items= ['Pais','ISO','val20','val30', 'Compromiso20'])
    dfb = pd.merge(dfcomp, df_ultima_observacion, on= 'Pais')  
    dfb['dif'] = dfb['val20'] - dfb['Emisiones_de_CO2']  

    conditionlist = [
        (dfb['Compromiso20_x'] == 0.0),
        (dfb['Emisiones_de_CO2']<dfb['val20']) ,
        (dfb['Emisiones_de_CO2']>dfb['val20'])]
    choicelist = ['Sin Compromiso','Cumplió', 'No cumplió']
    dfb['Compromiso'] = np.select(conditionlist, choicelist, default='Not Specified')

    dfc = dfb.drop(dfb[dfb['Compromiso20_x']==0.0].index)
    cumplen20 = dfc[dfc['Emisiones_de_CO2']<dfc['val20']]
    a = cumplen20.sort_values(by= 'dif', ascending= False).head(5)
    kpi_cumplimiento = (len(cumplen20)*100)/len(dfc)

    # Seleccion paises
    region = st.sidebar.radio("Seleccione Region", ('Latinoamerica', 'Personalizado'))
    lista_paises = filtro.lista_paises(df_sin_america_del_norte, 'pais')
    if region == 'Latinoamerica':
        seleccion_paises =  lista_paises
    #elif region == 'Toda America':
        #seleccion_paises = lista_paises
    elif region == 'Personalizado':
        seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises)

    dfb = dfb[dfb['Pais'].isin(seleccion_paises)]
    # Datos Grafico
    df = df_sin_america_del_norte[(df_sin_america_del_norte['Anio'] >= (sel_fecha_inicio)) & (df['Anio'] <= sel_fecha_fin)]
    df = df[df['Pais'].isin(seleccion_paises)]

    df_agrupacion_sum = df.groupby('Anio', as_index= False).sum()
    df_agrupacion_pais = df.groupby(['Anio','Pais'], as_index= False).mean()
    #df_agrupacion['Anio'] = pd.to_datetime(df_agrupacion['Anio'], format= '%Y')

    df_agrupacion_sum_ultimo_registro = df_agrupacion_sum[df_agrupacion_sum['Anio'] == anio_maximo]
    
    anio_maximo = df.Anio.max()
    anio_minimo = df.Anio.min()
    
    # Datos ultimo registro
    df_ultima_observacion = df[df['Anio'] == anio_maximo]
    #suma_emisiones_actual = df_ultima_observacion.Emisiones_de_CO2.sum()

    # Datos Pirmer registro
    df_primer_observacion = df[df['Anio'] == anio_minimo]
    #suma_emisiones_inicial = df_primer_observacion.Emisiones_de_CO2.sum()
    

    
    
    # Titulo
    col_logo, col_titulo, col_3 = st.columns([1,6,1])
     
    with col_logo:
         st.image('./images/icon_emisiones.png') 
    with col_titulo:
         st.markdown(
          """
         <h1 style="color:white;background-color:#407F46;padding: 2% 2% 2% 2%;border: solid #DCDCDC;border-radius: 10px;">95% de Cumplimiento en el Total de los Compromisos de Emisiones de CO2 en Latinoamérica para el Año 2030</h1>
         """,unsafe_allow_html=True)


    #Contenedor
    with st.container():
        #Columnas
        col1, col2, col3 = st.columns((3,3,3))

        with col1:
            #st.header("Emisiones")
            st.plotly_chart(graficos.indicador_vel_positivo(min_valor= suma_emisiones_inicial,
                                                            max_valor= emisiones_objetivo,
                                                            valor_actual= round(suma_emisiones_actual), 
                                                            valor_objetivo= emisiones_objetivo,
                                                            unidad_medida= 'Mill Tn',
                                                            titulo= "Emisiones CO2 2019",
                                                            color= '#407F46'), use_container_width= True)
            
            
            #st.title(str(kpi_pct) + "%")
            #st.progress(kpi_pct)

        with col2:

            st.header("Objetivo CO2 2030 (Mill Tn)")
            st.title(str(round(emisiones_objetivo)))
            st.header("")
            st.header("Predicción 2030 (Mill Tn)")
            
            st.title('2108  ± 168')
            
        with col3:
            #st.header("Porcentaje de Paises Que Cumplen el Compromiso")
            #st.plotly_chart(graficos.indicador_kpi_acceso(0, 100, round(kpi_cumplimiento), titulo= "Cumplimiento"), use_container_width= True)
            st.plotly_chart(graficos.indicador_vel_positivo(min_valor= 0,
                                                            max_valor= 100,
                                                            valor_actual= round(kpi_cumplimiento), 
                                                            valor_objetivo= 100,
                                                            unidad_medida= '%',
                                                            titulo= "Porc. Cumplimiento Paises",
                                                            color= '#407F46'), use_container_width= True)
            
            
        
        col_mapa, col_grafico = st.columns((2,2))
        #fecha_tupla = st.slider('Seleccione Periodos',  min_value= lista_periodos[0], max_value= lista_periodos[-1], value= (lista_periodos[0], lista_periodos[-1]))
        with col_mapa:
        
                st.subheader('Cantidad Emisiones CO2')
                figura_mapa = graficos.grafico_mapa_emisiones(df_ultima_observacion, 'Emisiones_de_CO2', "ISO", "", "Pais")
                st.plotly_chart(figura_mapa,  use_container_width=True)
                
        with col_grafico:
                st.subheader('Compromisos Cumplidos')
                figura_mapa_com = graficos.grafico_mapa_compromiso(dfb)
                st.plotly_chart(figura_mapa_com,  use_container_width=True)
                #st.dataframe(dfb)
        #st.sidebar.title('Configuracion Graficos de Barras')          
        
        
        col_top, col_down = st.columns((0.5,0.5))

        with col_top:
            
            
            try:
                st.subheader('Emisiones CO2 - Agrupación Anual')
                try:
                    figura2 = graficos.grafico_linea_emisiones(df_agrupacion_sum, 'Anio', 'Emisiones_de_CO2', 'Año', 'Emision CO2 (Mill Tn)')
                    st.plotly_chart(figura2,  use_container_width=True)
                except ValueError:
                    st.error("Seleccionar por lo menos 1 (uno) Pais")
                
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")
        
        with col_down:
            st.subheader('Países con Mayor Emisión CO2')
            try:
                opciones_mayor = st.slider('Seleccionar Cantidad de Paises', 1, 10, 5)
                df_top = df_ultima_observacion.sort_values(by = 'Emisiones_de_CO2' ,ascending= False).head(opciones_mayor)
                figura_top = graficos.grafico_barras_emisiones(df_top, 'Pais', 'Emisiones_de_CO2', 'Pais', 'Emision CO2 (Mill Tn)')
                st.plotly_chart(figura_top,  use_container_width=True)

            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")


if __name__ == '__main__':
    main()
