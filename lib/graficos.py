import pandas as pd
import datetime as dt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


#Configuraciones generales
                 
tamaño_fuente_graficos = 18


def grafico_mapa(df, nombre_columna_color, columna_locacion, region, nombre_escala, nombre_locacion, color_escala, color_text, color_marco, color_fondo,color_titulo):
            fig = px.choropleth(
                    locations= df[columna_locacion], 
                    locationmode="ISO-3", 
                    scope= region,
                    color= df[nombre_columna_color],
                    color_continuous_scale= color_escala,#"balance", #LE CAMBIÉ LA ESCALA DE COLORES DE BALANCE A VIRIDIS
                    #PARA QUE SE VEA MEJOR LA DIFERENCIA ENTRE ESTADOS UNIDOS Y LOS OTROS PAÍSES, SI QUERÉS SIGO BUSCANDO OTRAS
                    # ESCALAS DE COLORES    
                    hover_name= df['Pais'],        
                    labels={ "color": nombre_escala,"locations": nombre_locacion})#PUSE CO2 PORQUE ES CORTO, ESTO TRAE LAS ETIQUETAS CUANDO TE POSAS
                    #PERO TAMBIÉN ES EL TÍTULO DE LA BARRA DE COLORES. LO CORRECTO SERÍA PONER EMISIONES CO2 PERO ERA MUY LARGO

            fig.update_layout(
                    
                    showlegend = False,
                    geo = dict(
                        scope= region,
                        resolution=50,
                        projection_type='miller',
                        showcoastlines=True,
                        showocean=True,
                        showcountries=True,
                        oceancolor='#eaeaea',
                        lakecolor='#eaeaea',
                        coastlinecolor='#dadada',
                        fitbounds="locations",
                        ),
                    font=dict(
                                #family="Courier New, monospace",
                                size=tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                    #width=600,
                    )

            fig.update_layout(
                    #height=500, 
                    margin={"r":0,"t":50,"l":0,"b":0}, #ACÁ EN HEIGHT CAMBIAMOS EL TAMAÑO DEL MAPA.
                    paper_bgcolor=color_marco,
                    plot_bgcolor=color_fondo,
                    title_font_color=color_titulo,
                    font_color=color_text,
                    title_x = 0.5,
            )
            return fig


# Grafico de lineas
def grafico_linea(df, nombre_columna_x, nombre_columna_y, nombre_eje_x, nombre_eje_y, color_text, color_marco, color_fondo, color_titulo, color_dibujo):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                    x= df[nombre_columna_x],
                    y= df[nombre_columna_y],
                    line={'color':color_dibujo}
                    ))

        fig.update_layout(
                        margin=dict(l=20, r=20, t=50, b=20),
                        paper_bgcolor=color_marco,
                        plot_bgcolor=color_fondo,
                        title_font_color=color_titulo,
                        font_color=color_text,
                        #width=600, 
                        #height=500,
                        #title= titulo,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff",
                                ),
                        title_x = 0.5,
                           )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
                    
        return fig
    
    
# Grafico Barras
def grafico_barras(df, nombre_columna_x, nombre_columna_y, nombre_eje_x, nombre_eje_y, color_text, color_marco, color_fondo, color_titulo, color_dibujo):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df[nombre_columna_x], y = df[nombre_columna_y], marker={'color':color_dibujo}))
        fig.update_layout(
                        #title = titulo,
                    paper_bgcolor=color_marco,
                    plot_bgcolor= color_fondo,
                    title_font_color=color_titulo,
                    font_color=color_text,
                    #width=600,
                    #height=500,
                    font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                    title_x = 0.5,
                    )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)', title_text = nombre_eje_x)
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)', title_text = nombre_eje_y)
        return fig



# Graficos  especificos KPI Temperatura
# Colores Graficos
color_fuente_graf_tem = 'rgb(252, 183, 20)'
color_fuente_titulo_graf_tem = 'rgb(252, 183, 20)'
color_fondo_graf_tem = '#EAEAEA'
color_marco_graf_tem = 'rgba(0,0,0,0)'
color_dibujo_graf_tem = '#FDC30C'
color_dibujo_graf_secundario_tem = '#A37C01'
color_dibujo_linea_comparativo =  '#FF5733'
color_escala_mapa_tem = 'solar_r'


def indicador_kpi_temp(df, columna_dato, valor_referencia):
        fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = df[columna_dato].values[-1],
                                title = {'text': "Proporcion"},
                                delta = {'reference': valor_referencia},
                                domain = {'x': [0, 0.5], 'y': [0, 0.5]},
                                 
                                #width=1000,
                                #height=500,
                                ))

        return fig

transp = 'rgba(0,0,0,0)' 
def grafico_linea_temperatura(df_tabla, df_promedios,nombre_columna_x, nombre_columna_y, nombre_eje_x, nombre_eje_y, color_text, color_marco, color_fondo, color_titulo, color_dibujo, color_dibujo_sec):

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_tabla[nombre_columna_x], y = df_promedios*np.ones(len(df_tabla[nombre_columna_x])), mode='lines', line={'color':color_dibujo_sec, 'dash':'dash', 'width':4}, name = 'Media siglo XX'))
    fig.add_trace(go.Scatter(x = df_tabla[nombre_columna_x], y = 1.5+df_promedios*np.ones(len(df_tabla[nombre_columna_x])), mode='lines', line={'color':color_dibujo_sec, 'dash':'dot', 'width':4}, name = 'Límite: + 1.5ºC'))
    fig.add_trace(go.Scatter(x = df_tabla[nombre_columna_x], y = df_tabla[nombre_columna_y], mode='lines+markers', line={'color':color_dibujo, 'width':4}, name='Temp. ºC'))
    
    fig.update_layout(
        #title = titulo,
        paper_bgcolor=color_marco,
        plot_bgcolor=color_fondo,
        title_font_color=color_titulo,
        font_color=color_text,
        #width=1000,
        #height=500,
        font=dict(
                  #family="Courier New, monospace",
                  size= tamaño_fuente_graficos,
                  #color="#ffffff"
                ),
        title_x = 0.5,
        )
    
    fig.update_xaxes(showline=True, linewidth=3, linecolor='#FFFFFF',gridcolor='rgba(255,255,255,0.5)', title_text = nombre_eje_x)
    fig.update_yaxes(showline=True, linewidth=3, linecolor='#FFFFFF',gridcolor='rgba(255,255,255,0.5)', title_text = nombre_eje_y)
    
    return fig


def grafico_temp_linea_comparativo(df1, df2, df3):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df2['Anio'], y = df2['temperatura'], mode='lines',         line={'color':color_dibujo_linea_comparativo, 'dash':'dot'}, name = 'Cuba'))
        fig.add_trace(go.Scatter(x = df1['Anio'], y = df1['temperatura'], mode='lines+markers', line={'color':color_dibujo_linea_comparativo},               name = 'Bahamas'))
        fig.add_trace(go.Scatter(x = df3['Anio'], y = df3['temperatura'], mode='lines',         line={'color':color_dibujo_linea_comparativo},               name = 'México'))
        fig.update_layout(
                        #title = 'Países con más aumento de temperatura',
                        paper_bgcolor= color_marco_graf_tem,
                        plot_bgcolor= color_fondo_graf_tem,
                        title_font_color= color_fuente_titulo_graf_tem,
                        font_color= color_fuente_graf_tem,
                        #width=1000,
                        #height=500
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)')
        return fig


def grafico_temp_barra(df, columna_x, columna_y):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df[columna_x], y = df[columna_y], marker={'color':color_dibujo_graf_tem}))
        fig.update_layout(
                        #title = 'Top Países con menos aumento de temperatura entre 1901 y 2021',
                        paper_bgcolor= color_marco_graf_tem,
                        plot_bgcolor= color_fondo_graf_tem,
                        title_font_color= color_fuente_titulo_graf_tem,
                        font_color= color_fuente_graf_tem,
                        #width=700,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        
                        )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)')
        return fig



#Graficos Acceso

# Colores Grafico
color_marco_graf_acceso = "#FFFFFF"
color_fondo_graf_acceso = '#EAEAEA'
color_fuente_titulo_graf_acceso = "#E5233D"
color_fuente_graf_acceso = "#E5233D"
color_escala_mapa_acceso = "Reds"

def grafico_linea_latinoamerica_acceso(df_grafico, columna_x, columna_y, nombre_eje_x, nombre_eje_y):
        fig = px.line(df_grafico, 
                       x = columna_x, 
                       y= columna_y, 
                       #title= titulo,
                )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_acceso,
                        plot_bgcolor= color_fondo_graf_acceso,
                        title_font_color= color_fuente_titulo_graf_acceso,
                        font_color= color_fuente_graf_acceso,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        margin={"r":0,"t":50,"l":0,"b":0},
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig


def grafico_barra_top_acceso(df, columna_x, columna_y, titulo, nombre_eje_x, nombre_eje_y):
        fig = px.bar(data_frame= df,
                        x= columna_x,
                        y = columna_y,
                        title= titulo)
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_acceso,
                        plot_bgcolor= color_fondo_graf_acceso,
                        title_font_color= color_fuente_titulo_graf_acceso,
                        font_color= color_fuente_graf_acceso,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        margin={"r":0,"t":50,"l":0,"b":0},
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig


def grafico_linea_comparativo_acceso(df_grafico, columna_x, columna_y, color_categ, nombre_eje_x, nombre_eje_y):
        fig = px.line(df_grafico,
                        x= columna_x, 
                        y= columna_y,
                        color= color_categ,
                        #title= titulo,
                        )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_acceso,
                        plot_bgcolor= color_fondo_graf_acceso,
                        title_font_color= color_fuente_titulo_graf_acceso,
                        font_color= color_fuente_graf_acceso,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        legend=dict(
                                orientation = 'h',
                                yanchor="top",
                                y=1.12,
                                xanchor="left",
                                x=0.01
                        )
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig




def grafico_mapa_acceso(df, nombre_columna_color, columna_locacion, nombre_escala, nombre_locacion ):
        fig = px.choropleth(
                    locations= df[columna_locacion], 
                    locationmode="ISO-3", 
                    scope="world",
                    color= df[nombre_columna_color],
                    color_continuous_scale= color_escala_mapa_acceso,#"balance", #LE CAMBIÉ LA ESCALA DE COLORES DE BALANCE A VIRIDIS
                    #PARA QUE SE VEA MEJOR LA DIFERENCIA ENTRE ESTADOS UNIDOS Y LOS OTROS PAÍSES, SI QUERÉS SIGO BUSCANDO OTRAS
                    # ESCALAS DE COLORES    
                    hover_name= df['Pais'],        
                    labels={ "color": nombre_escala,"locations": nombre_locacion})#PUSE CO2 PORQUE ES CORTO, ESTO TRAE LAS ETIQUETAS CUANDO TE POSAS
                    #PERO TAMBIÉN ES EL TÍTULO DE LA BARRA DE COLORES. LO CORRECTO SERÍA PONER EMISIONES CO2 PERO ERA MUY LARGO

        fig.update_layout(
                #title_text = titulo,
                showlegend = False,
        geo = dict(
                scope='world',
                resolution=110,
                projection_type='miller',
                showcoastlines=True,
                showocean=True,
                showcountries=True,
                oceancolor='#eaeaea',
                lakecolor='#eaeaea',
                coastlinecolor='#dadada',
                fitbounds="locations"),
                )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_acceso,
                        plot_bgcolor= color_fondo_graf_acceso,
                        title_font_color= color_fuente_titulo_graf_acceso,
                        font_color= color_fuente_graf_acceso,
                        #width=600,
                        #height=500, #ACÁ EN HEIGHT CAMBIAMOS EL TAMAÑO DEL MAPA.
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        
                        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig



#Graficos Renovables

# Colores Grafico
color_marco_graf_renovables = "#FFFFFF"
color_fondo_graf_renovables = '#EAEAEA'
color_fuente_titulo_graf_renovables = "rgb(192,142, 46)"
color_fuente_graf_renovables = "rgb(192,142, 46)"
color_escala_mapa_renovables = "BrBg"

def grafico_linea_latinoamerica_renovables(df_grafico, columna_x, columna_y, nombre_eje_x, nombre_eje_y):
        fig = px.line(df_grafico, 
                       x = columna_x, 
                       y= columna_y, 
                       #title= titulo,
                )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_renovables,
                        plot_bgcolor= color_fondo_graf_renovables,
                        title_font_color= color_fuente_titulo_graf_renovables,
                        font_color= color_fuente_graf_renovables,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        margin={"r":0,"t":50,"l":0,"b":0},
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig


def grafico_barra_top_renovables(df, columna_x, columna_y, titulo, nombre_eje_x, nombre_eje_y):
        fig = px.bar(data_frame= df,
                        x= columna_x,
                        y = columna_y,
                        title= titulo)
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_renovables,
                        plot_bgcolor= color_fondo_graf_renovables,
                        title_font_color= color_fuente_titulo_graf_renovables,
                        font_color= color_fuente_graf_renovables,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        margin={"r":0,"t":50,"l":0,"b":0},
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig


def grafico_linea_comparativo_renovables(df_grafico, columna_x, columna_y, color_categ, nombre_eje_x, nombre_eje_y):
        fig = px.line(df_grafico,
                        x= columna_x, 
                        y= columna_y,
                        color= color_categ,
                        #title= titulo,
                        )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_renovables,
                        plot_bgcolor= color_fondo_graf_renovables,
                        title_font_color= color_fuente_titulo_graf_renovables,
                        font_color= color_fuente_graf_renovables,
                        #width=600,
                        #height=500,
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        legend=dict(
                        orientation = 'h',
                        yanchor="top",
                        y=1.12,
                        xanchor="left",
                        x=0.01
                        )
        )
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_y)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.5)',
                            title_text= nombre_eje_x)
        return fig




def grafico_mapa_renovables(df, nombre_columna_color, columna_locacion, nombre_escala, nombre_locacion ):
        fig = px.choropleth(
                    locations= df[columna_locacion], 
                    locationmode="ISO-3", 
                    scope="world",
                    color= df[nombre_columna_color],
                    color_continuous_scale= color_escala_mapa_renovables,#"balance", #LE CAMBIÉ LA ESCALA DE COLORES DE BALANCE A VIRIDIS
                    #PARA QUE SE VEA MEJOR LA DIFERENCIA ENTRE ESTADOS UNIDOS Y LOS OTROS PAÍSES, SI QUERÉS SIGO BUSCANDO OTRAS
                    # ESCALAS DE COLORES    
                    hover_name= df['Pais'],        
                    labels={ "color": nombre_escala,"locations": nombre_locacion})#PUSE CO2 PORQUE ES CORTO, ESTO TRAE LAS ETIQUETAS CUANDO TE POSAS
                    #PERO TAMBIÉN ES EL TÍTULO DE LA BARRA DE COLORES. LO CORRECTO SERÍA PONER EMISIONES CO2 PERO ERA MUY LARGO

        fig.update_layout(
                        #title_text = titulo,
                        showlegend = False,
                geo = dict(
                        scope='world',
                        resolution=110,
                        projection_type='miller',
                        showcoastlines=True,
                        showocean=True,
                        showcountries=True,
                        oceancolor='#eaeaea',
                        lakecolor='#eaeaea',
                        coastlinecolor='#dadada',
                        fitbounds="locations"),
                )
        fig.update_layout(
                        paper_bgcolor= color_marco_graf_renovables,
                        plot_bgcolor= color_fondo_graf_renovables,
                        title_font_color= color_fuente_titulo_graf_renovables,
                        font_color= color_fuente_graf_renovables,
                        #width=600,
                        #height=500, #ACÁ EN HEIGHT CAMBIAMOS EL TAMAÑO DEL MAPA.
                        font=dict(
                                #family="Courier New, monospace",
                                size= tamaño_fuente_graficos,
                                #color="#ffffff"
                                ),
                        title_x = 0.5,
                        
                        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig