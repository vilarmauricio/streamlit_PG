import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import lib.graficos as graficos 

st.set_page_config(
     page_title="KPI Acceso",
     page_icon="🌍",
     layout="wide",
     initial_sidebar_state= "collapsed",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("./styles/css_acceso.css")


#@st.cache
def crear_dataframe(nombre_archivo):
    df = pd.read_csv('./'+nombre_archivo)
    return df



def main():

     
   df = crear_dataframe('./dataset/datos_ONU.csv')
    
       
     #lista_paises
   lista_paises_latinoamerica = sorted(df.Pais.unique())
   lista_paises_latinoamerica.remove('Canadá')


     # Seleccion paises
   region = st.sidebar.radio("Seleccione Region", ('Latinoamerica', 'Personalizado'))

   if region == 'Latinoamerica':
        seleccion_paises =  lista_paises_latinoamerica
     #elif region == 'Toda America':
        #seleccion_paises = lista_paises
   elif region == 'Personalizado':
        seleccion_paises = st.sidebar.multiselect('Seleccion Paises', options= lista_paises_latinoamerica)


      
     # Hacemos los calculos
   df = df.drop(df[df['Pais']=='Canadá'].index)
   df['ISO']= df['Pais'].map({'Antigua y Barbuda':'ATG','Argentina':'ARG','Bahamas':'BHS','Barbados':'BRB','Belice':'BLZ',
                           'Bolivia':'BOL','Brasil':'BRA','Chile':'CHL','Colombia':'COL','Costa Rica':'CRI','Cuba':'CUB','Dominica':'DMA',
                           'Ecuador':'ECU','El Salvador':'SLV','Guatemala':'GTM','Guyana':'GUY','Haití':'HTI','Honduras':'HND',
                           'Jamaica':'JAM','México':'MEX','Nicaragua':'NIC','Panamá':'PAN','Paraguay':'PRY','Perú':'PER','República Dominicana':'DOM',
                           'San Cristóbal y Nieves':'KNA','San Vicente y las Granadinas':'VCT','Santa Lucía':'LCA','Surinam':'SUR','Trinidad y Tobago':'TTO',
                           'Uruguay':'URY','Venezuela':'VEN'})


   if region == 'Personalizado' and len(seleccion_paises)>0:
        df = df[df['Pais'].isin(seleccion_paises)]



   df20 = df.filter(items=['Pais','ISO','Anio','proporcion_de_la_poblacion_con_acceso_a_elecricidad', 'proporcion_de_la_poblacion_con_dependencia_primaria_a_energias_limpias'])
   prom = df20.loc[:,'proporcion_de_la_poblacion_con_acceso_a_elecricidad':'proporcion_de_la_poblacion_con_dependencia_primaria_a_energias_limpias']
   df20['promedio'] = prom.mean(axis=1)

   # Tabla grafico linea proporcion latinoamerica
   tabla_g20 = df20.groupby('Anio').mean()
   tabla_g20.reset_index(inplace=True)

   # Tabla grafico de barras top paises mayor proporcion
   df21 = df20[((df20['Anio'])==2019)]
   tabla_g21 = df21.sort_values(by= 'promedio', ascending= False).head(5)
   tabla_g21.reset_index(inplace=True)
   # Grafico de barra colores
   anio_ultimo_registro_df20 = df20.Anio.max()
   anio_primer_registro_df20 = df20.Anio.min()
   df_ultimo = df20[df20['Anio'] == anio_ultimo_registro_df20]
   df_inicio = df20[df20['Anio'] == anio_primer_registro_df20]
   df_ultimo = df_ultimo.sort_values('promedio', ascending= False).head(5)
   lista_paises_top = df_ultimo.Pais.unique()
   df_ultimo2 = df_ultimo[df_ultimo['Pais'].isin(lista_paises_top)]
   df_inicio2 = df_inicio[df_inicio['Pais'].isin(lista_paises_top)]


   # Tabla grafico de lineas top 3 paises mayor proporcion
   lista_pais_mayor_proporcion_acceso = tabla_g21.Pais.unique()
   df22 = df20[df20.Pais.isin(lista_pais_mayor_proporcion_acceso[:3])]
   tabla_g22 = df22
   tabla_g22.reset_index(inplace=True)

   # Tabla grafico de barras top paises menor proporcion
   tabla_g23 = df21.sort_values(by= 'promedio', ascending= True).head(5)
   tabla_g23.reset_index(inplace=True)

   # Tabla grafico de lineas top 3 paises menor proporcion
   lista_pais_menor_proporcion_acceso = tabla_g23.Pais.unique()
   df23 = df20[df20.Pais.isin(lista_pais_menor_proporcion_acceso[:3])]
   tabla_g24 = df23
   tabla_g24.reset_index(inplace=True)

   #kpi y Metrica actual
   anio_ultimo_registro = tabla_g20.Anio.max()
   promedio_ultimo_registro = tabla_g20[tabla_g20['Anio'] == anio_ultimo_registro].promedio.values[0]


   # Titulo
   col_logo, col_titulo = st.columns([1,6])
     
   with col_logo:
         st.image('./images/icon_acceso.png') 
   with col_titulo:
         st.image('./images/titulo_acceso.png')




     # TARJETAS
   col1, col2, col3 = st.columns(3)

   with col1:
            #st.plotly_chart(graficos.indicador_kpi_acceso(0, 100, promedio_ultimo_registro, 'Porcentaje Acceso'), use_container_width= True)
            st.plotly_chart(graficos.indicador_vel_positivo(min_valor= 0,
                                                            max_valor= 100,
                                                            valor_actual= round(promedio_ultimo_registro, 2), 
                                                            valor_objetivo= 95,
                                                            unidad_medida= 'Mill Tn',
                                                            titulo= "Acceso (%)",
                                                            color= "rgb(225,40,72)"), use_container_width= True)
            #st.header("Progreso KPI's")
            #st.title("Calcular KPI")
            #st.progress(round(promedio_ultimo_registro))
            

   with col2:
            st.header("Porcentaje Actual")

            st.title( str(round(promedio_ultimo_registro)) +" %")
            

   with col3:
            st.header("Porcentaje Objetivo")
            st.title("95 %")
            

     # GRAFICOS CENTRALES   
   col_graf_1, col_graf_2 = st.columns(2)

   with col_graf_1:
               st.subheader('Proporción de la población con acceso a los servicios')
               figura_mapa = graficos.grafico_mapa_acceso(df20, 'promedio', 'ISO', "", "Pais")
               st.plotly_chart(figura_mapa, use_container_width= True)


   with col_graf_2:
                #st.subheader('Emisiones CO2 - Agrupacion Anual')
                try:
                    st.subheader('Proporción de la población con acceso a los servicios')
                    figura2 = graficos.grafico_linea_latinoamerica_acceso(tabla_g20, 'Anio', 'promedio', 'Año', 'Promedio')
                    st.plotly_chart(figura2, use_container_width= True)
                except ValueError:
                    st.error("Seleccionar por lo menos 1 (uno) Pais")
            
        #st.sidebar.title('Configuracion Graficos de Barras')          


     # GRAFICOS INFERIORES   
   col_graf_3, col_graf_4 = st.columns(2)

   with col_graf_3:
            
            #try:
               st.subheader('Países con mayor proporción de la población con acceso a los servicios')
               
               figura_top = graficos.grafico_barras_colores_acceso(df_inicio2, df_ultimo2, str(anio_primer_registro_df20), str(anio_ultimo_registro_df20), 'Pais', 'Acceso Promedio (%)')
               # figura_top = graficos.grafico_barra_top_acceso(tabla_g21, 'Pais', 'promedio', 'Pais', 'Promedio')
               #figura_top = graficos.grafico_linea_comparativo_acceso(tabla_g22, 'Anio', 'promedio', 'Pais', 'Anio', 'Promedio')
               st.plotly_chart(figura_top, use_container_width= True)
            #except ValueError:
             #   st.error("Seleccionar por lo menos 1 (uno) Pais")
        
   with col_graf_4:
           
            try:
               st.subheader('Países con menor proporción de la población con acceso a los servicios')           
               figura_down = graficos.grafico_linea_comparativo_acceso(tabla_g24, columna_x= 'Anio', columna_y= 'promedio', color_categ='Pais', nombre_eje_x= 'Anio', nombre_eje_y= 'Promedio')
               st.plotly_chart(figura_down, use_container_width= True)
            except ValueError:
                st.error("Seleccionar por lo menos 1 (uno) Pais")


if __name__ == '__main__':
    main()
