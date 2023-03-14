# Paketleri içeri aktaralım. 
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Sayfayı geniş formatta kullanma
st.set_page_config(layout="wide")

# Veri setini içeri aktarma
gapminder = pd.read_csv('gapminder.csv')

# Bir satırlık alanı kolonlara ayırma
row0_1, row0_2 = st.columns(2)
# İlk kolon
with row0_1:
    st.image('https://storage.googleapis.com/kaggle-datasets-images/373567/726490/b870208e6f91c6a6c940f8a4df111c87/dataset-cover.png?t=2019-10-22-19-47-34')

# Başlık ekleme
st.markdown('### Yıllar içinde Yaşam Beklentisi ve Gayrisafi Yurt İçi Hasıla Değişimleri')

# Bir satırlık alanı kolonlara ayırma
row1_1, row1_2 = st.columns(2)
# İlk kolon
with row1_1:
    ulkeler = st.multiselect('Karşılaştırmak istediğiniz ülkeleri seçiniz:', list(gapminder["country"].unique()), default = ['Germany', 'Turkey', 'Argentina']) 

# Bir satırlık alanı kolonlara ayırma
row2_1, row2_2 = st.columns(2)
# İlk kolondaki grafik
with row2_1:
    fig = px.line(data_frame = gapminder[gapminder['country'].isin(ulkeler)], 
                x = 'year', y = 'lifeExp', color = 'country')
    fig.update_layout(title = dict(text='Yıla Göre Yaşam Beklentisi Değişimi', x = 0.05, font = dict(size = 18)),
                    legend_title = 'Ülke')
    fig.update_xaxes(title = dict(text = 'Yıl', font = dict(size = 16)))
    fig.update_yaxes(title = dict(text = 'Yaşam Beklentisi', font = dict(size = 16)))
    fig.update_traces(dict(line = {'width':3}))
    st.plotly_chart(fig, use_container_width = True)

# İkinci kolondaki grafik
with row2_2:
    fig = px.line(data_frame = gapminder[gapminder['country'].isin(ulkeler)], 
                x = 'year', y = 'gdpPercap', color = 'country')
    fig.update_layout(title = dict(text='Yıla Göre Gayrisafi Yurt İçi Hasıla Değişimi', x = 0.05, font = dict(size = 18)),
                    legend_title = 'Ülke')
    fig.update_xaxes(title = dict(text = 'Yıl', font = dict(size = 16)))
    fig.update_yaxes(title = dict(text = 'Kişi Başı Gayrisafi Yurt İçi Hasıla', font = dict(size = 16)))
    fig.update_traces(dict(line = {'width':3}))
    st.plotly_chart(fig, use_container_width = True)

# Başlık ekleme
st.markdown('### Gayrisafi Yurt İçi Hasıla ve Yaşam Beklentisi İlişkisi')

# Bir satırlık alanı kolonlara ayırma
row3_1, row3_2 = st.columns(2)
# İlk kolon
with row3_1:
    yil = st.selectbox('İncelemek istediğiniz yılı seçiniz:', list(gapminder["year"].unique()), index = 11, key = 1.1) 

fig = px.scatter(gapminder[gapminder['year'] == yil], x = 'gdpPercap', y = 'lifeExp', hover_data = ['country'],
                color = 'continent', opacity = 0.6, size = 'pop', size_max = 60, log_x = True)
fig.update_layout(title = dict(text = 'Gayrisafi Yurt İçi Hasıla ve Yaşam Beklentisi İlişkisi', 
                font = dict(size = 18)), legend_title = 'Kıta', xaxis = dict(tickmode = 'array', 
                tickvals = [500, 1000, 5000, 10000, 50000, 100000], ticktext = [500, 1000, 5000, 10000, 50000, 100000]))
fig.update_xaxes(title = dict(text='Kişi Başı Gayrisafi Yurt İçi Hasıla', font = dict(size = 16)))
fig.update_yaxes(title = dict(text='Yaşam Beklentisi', font = dict(size = 16)))
st.plotly_chart(fig, use_container_width = True)

# Başlık ekleme
st.markdown('### Yaşam Beklentisinde Dünya Ortalamasına Göre Ülkelerin Durumları')

# Bir satırlık alanı kolonlara ayırma
row4_1, row4_2 = st.columns(2)
# İlk kolon
with row4_1:
    yil = st.selectbox('İncelemek istediğiniz yılı seçiniz:', list(gapminder["year"].unique()), index = 11, key = 1.2) 

# Veri manipülasyonu
df = gapminder[gapminder['year'] == yil]
df['lifeExp_status'] = ['Dünya ortalamasından düşük' if x < df.lifeExp.mean()  else 'Dünya ortalamasından yüksek' for x in df['lifeExp']]

# Bir satırlık alanı kolonlara ayırma
row5_1, row5_2 = st.columns(2)
# İlk kolondaki grafik
with row5_1:
    df_stack_bar = df.groupby('continent')['lifeExp_status'].value_counts(normalize = True).to_frame().rename(columns = {'lifeExp_status':'ratio'}).reset_index()
    fig = px.bar(data_frame = df_stack_bar, x = 'continent', y = 'ratio', color = 'lifeExp_status')
    fig.update_xaxes(title = dict(text = 'Kıta', font = dict(size = 16)))
    fig.update_yaxes(title = dict(text = 'Ülke Oranı', font = dict(size = 16)))
    fig.update_layout(title = dict(text='Dünyadaki Ortalama Yaşam Beklentisine Göre Ülkelerin Dağılımı', x = 0.05, font = dict(size = 17)),
                    legend = dict(orientation = "h", yanchor = "bottom", y = 1.01, xanchor = "right", x = 1),
                    legend_title = dict(text = 'Yaşam Beklentisi', font = dict(size = 15)), margin = dict(l=0, r=20, t=100, b=0))
    st.plotly_chart(fig, use_container_width = True)

# İkinci kolondaki grafik
with row5_2:
    fig = px.box(data_frame = df, x = 'continent', y = 'gdpPercap', color = 'lifeExp_status')
    fig.update_xaxes(title = dict(text = 'Kıta', font = dict(size = 16)))
    fig.update_yaxes(title = dict(text = 'Kişi Başı Gayrisafi Yurt İçi Hasıla', font = dict(size = 16)))
    fig.update_layout(title = dict(text='Dünyadaki Ortalama Yaşam Beklentisine Göre Ülkelerin GSYH Dağılımı', x = 0.05, font = dict(size = 17)),
                    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
                    legend_title = dict(text = 'Yaşam Beklentisi', font = dict(size = 15)), margin=dict(l=80, r=0, t=100, b=0))
    st.plotly_chart(fig, use_container_width = True)

# Başlık ekleme
st.markdown('### Yıla Göre Harita')

# Bir satırlık alanı kolonlara ayırma
row6_1, row6_2 = st.columns(2)

# İlk kolon
with row6_1:
    degisken = st.selectbox('İncelemek istediğiniz değişkeni seçiniz:', ['Yaşam Beklentisi', 'Nüfus', 'Gayrisafi Yurt İçi Hasıla'], index = 0) 
# İkinci kolon
with row6_2:
    yil = st.selectbox('İncelemek istediğiniz yılı seçiniz:', list(gapminder["year"].unique()), index = 11, key = 1.3) 

# Veri manipülasyonu
degisken_dict = {'Yaşam Beklentisi':'lifeExp', 'Nüfus':'pop', 'Gayrisafi Yurt İçi Hasıla':'gdpPercap'}

# Bir satırlık alanı kolonlara ayırma
row7_1, row7_2, row7_3 = st.columns([0.75,2,1])
# İlk kolondaki grafik
with row7_2:
    m = folium.Map(location=(30, 10), zoom_start=1, height = '80%')

    choropleth = folium.Choropleth(
            geo_data=("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"),
            data = gapminder[gapminder.year == yil][['country', degisken_dict[degisken]]],
            columns = ['country', degisken_dict[degisken]],
            key_on = 'feature.properties.name',
            fill_color='Reds',
            line_opacity = 0.2,
            fill_opacity = 0.8,
            legend_name='Yaşam Beklentisi',
            highlight = True,
            nan_fill_color="white"
            ).add_to(m)

    folium.LayerControl().add_to(m)

    choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'], labels=True, aliases= ['Ülke'])
            )

    folium_static(m, width=700)

