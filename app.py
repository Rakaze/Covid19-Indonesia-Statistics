import pandas as pd
from plotly import graph_objs as go
import streamlit as st

url_case = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
vax_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/Indonesia.csv"
url_a = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


st.set_page_config(page_title='Indonesia Covid-19 Statistic', layout="wide", page_icon=':bar_chart:')
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
footer{
    visibility:hidden;
}

"""
st.write('''

# Covid-19 Indonesia Dashboard :bar_chart:

Menampilkan data Covid-19 di Indonesia

''')

st.write("Made with :heart: by Raka Luthfi")
st.write("Data from: BNPB, JHU CSSE and Our World in Data")
st.write("Tech: Python, Streamlit, Pandas and Plotly")
st.write('---')

@st.cache(allow_output_mutation=True)
def get_cov_data():
  case_id = pd.read_csv(url_case)
  death = pd.read_csv(url_death)
  vax = pd.read_csv(vax_url)
  vax_daily = pd.read_csv('vax_daily.csv')
  provinsi = pd.read_csv('cov_provinsi.csv')
  prov = pd.read_csv('provinsi.csv')
  harian = pd.read_csv('covid_id.csv')
  all = pd.read_csv(url_a)
  return case_id, death, vax, provinsi, all, harian, prov, vax_daily

case_id, death, vax, provinsi, all, harian, prov, vax_daily = get_cov_data()

kasus_indo = case_id[case_id['Country/Region']=="Indonesia"].T.iloc[-1,0]
meninggal = death[death['Country/Region']=="Indonesia"].T.iloc[-1,0]
sembuh_all = provinsi.loc[provinsi['Provinsi']=='Total', 'Total Sembuh'].iloc[0]
af = all[all['iso_code']=='IDN']
harian['Tanggal'] = pd.to_datetime(harian['Tanggal']).dt.strftime('%Y-%m-%d')
harian['Sembuh (Indonesia)'] = harian['Sembuh (Indonesia)'].replace(',','', regex=True).apply(pd.to_numeric)
harian['Sembuh Harian (Indonesia)'] = harian['Sembuh Harian (Indonesia)'].replace(',','', regex=True).apply(pd.to_numeric)
harian['Meninggal (Indonesia)'] = harian['Meninggal (Indonesia)'].replace(',','', regex=True).apply(pd.to_numeric)
harian['Meninggal Harian (Indonesia)'] = harian['Meninggal Harian (Indonesia)'].replace(',','', regex=True).apply(pd.to_numeric)

st.subheader("Kasus Covid-19")

option = st.selectbox(
     'Pilih data wilayah',
     ('Nasional', 'ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG','KEPULAUAN BANGKA BELITUNG', 'KEPULAUAN RIAU', 'DKI JAKARTA', 'JAWA BARAT', 'JAWA TENGAH', 'DAERAH ISTIMEWA YOGYAKARTA', 'JAWA TIMUR', 'BANTEN', 'BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 'KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN','KALIMANTAN TIMUR', 'KALIMANTAN UTARA', 'SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 'SULAWESI TENGGARA', 'GORONTALO', 'SULAWESI BARAT', 'MALUKU', 'MALUKU UTARA', 'PAPUA', 'PAPUA BARAT'))

st.write('Memilih data:', option)

if option=='Nasional':
  tot_kasus, tot_sembuh, tot_meninggal = st.columns(3)
  tot_kasus.metric("Total Kasus di " + str(option) , format(kasus_indo, ',d'))
  tot_sembuh.metric("Total Sembuh di " + str(option), format(sembuh_all, ',d'))
  tot_meninggal.metric("Total Meninggal di " + str(option), format(meninggal, ',d'))
else:
  tot_kasus, tot_sembuh, tot_meninggal = st.columns(3)
  lokasi_total = prov[prov["Location"]==option]['KASUS'].sum()
  lokasi_sembuh = prov[prov["Location"]==option]['SEMBUH'].sum()
  lokasi_meninggal = prov[prov["Location"]==option]['MENINGGAL'].sum()
  tot_kasus.metric("Total Kasus di " + str(option) , format(lokasi_total, ',d'))
  tot_sembuh.metric("Total Sembuh di " + str(option), format(lokasi_sembuh, ',d'))
  tot_meninggal.metric("Total Meninggal di " + str(option), format(lokasi_meninggal, ',d'))


st.sidebar.subheader('Pilih Data')
opsi1 = st.sidebar.checkbox("Total Kasus")
opsi2 = st.sidebar.checkbox("Kasus Harian")
opsi3 = st.sidebar.checkbox("Total Sembuh")
opsi4 = st.sidebar.checkbox("Sembuh Harian")
opsi5 = st.sidebar.checkbox("Total Meninggal")
opsi6 = st.sidebar.checkbox("Meninggal Harian")

fig = go.Figure()
if option=='Nasional':
    if (opsi1 or opsi2 or opsi3 or opsi4 or opsi5 or opsi6) is False:
          fig.add_trace(go.Scatter(x=af['date'], y=af['new_cases'], name='Total Kasus'))
          fig.add_trace(go.Scatter(x=harian['Tanggal'], y=harian['Sembuh Harian (Indonesia)'], name='Sembuh Harian'))
    else:
      if opsi1:
          fig.add_trace(go.Scatter(x=af['date'], y=af['total_cases'], name='Total Kasus'))
      if opsi2:
          fig.add_trace(go.Scatter(x=af['date'], y=af['new_cases'], name='Kasus Harian'))
      if opsi3:
          fig.add_trace(go.Scatter(x=harian['Tanggal'], y=harian['Sembuh (Indonesia)'], name='Kasus Sembuh'))
      if opsi4:
          fig.add_trace(go.Scatter(x=harian['Tanggal'], y=harian['Sembuh Harian (Indonesia)'], name='Sembuh Harian')) 
      if opsi5:
          fig.add_trace(go.Scatter(x=harian['Tanggal'], y=harian['Meninggal (Indonesia)'], name='Kasus Meninggal')) 
      if opsi6:
          fig.add_trace(go.Scatter(x=harian['Tanggal'], y=harian['Meninggal Harian (Indonesia)'], name='Meninggal Harian')) 

else:
    if (opsi1 or opsi2 or opsi3 or opsi4 or opsi5 or opsi6) is False:
          lokasi_total = prov[prov["Location"]==option]['KASUS']
          lokasi_sembuh = prov[prov["Location"]==option]['SEMBUH']
          lokasi_meninggal = prov[prov["Location"]==option]['MENINGGAL']
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['KASUS'], name='Kasus Harian'))
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['SEMBUH'], name='Sembuh Harian'))
    else:
      if opsi1:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['AKUMULASI_KASUS'], name='Total Kasus'))
      if opsi2:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['KASUS'], name='Kasus Harian'))
      if opsi3:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['AKUMULASI_SEMBUH'], name='Kasus Sembuh'))
      if opsi4:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['SEMBUH'], name='Sembuh Harian')) 
      if opsi5:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['AKUMULASI_MENINGGAL'], name='Kasus Meninggal')) 
      if opsi6:
          fig.add_trace(go.Scatter(x=prov['Date'], y=prov[prov["Location"]==option]['MENINGGAL'], name='Meninggal Harian')) 

fig.layout.update(title_text=str(option) + ' Covid-19', 
                      xaxis_rangeslider_visible=True, 
                      hovermode='x',
                      legend_orientation='v')
st.plotly_chart(fig, use_container_width=True)
st.write('---')

st.subheader("Jumlah Penerima Vaksinasi")

vax_1 = vax['people_vaccinated'].iloc[-1]
vax_2 = vax['people_fully_vaccinated'].iloc[-1]
vax_col1, vax_col2 = st.columns(2)
vax_col1.metric("Vaksinasi ke-1", format(vax_1, ',d'))
vax_col2.metric("Vaksinasi ke-2", format(vax_2, ',d'))

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
opsi_vax = st.radio("", ('Vaksinasi ke-1', 'Vaksinasi ke-2'))
vax_select = st.selectbox('', ('Kumulatif', 'Harian'))
fig_vax = go.Figure()
if opsi_vax == 'Vaksinasi ke-1':
    if vax_select == 'Kumulatif':
      fig_vax.add_trace(go.Scatter(x=vax_daily['Date'], y=vax_daily['jumlah_jumlah_vaksinasi_1_kum'], name='Kumulatif Vaksinasi ke-1'))
      fig_vax.layout.update(title_text='Kumulatif Vaksinasi ke-1', 
                       xaxis_rangeslider_visible=False, 
                       hovermode='x',
                       legend_orientation='v')
      st.plotly_chart(fig_vax, use_container_width=True)
    else:
      fig_vax.add_trace(go.Bar(x=vax_daily['Date'], y=vax_daily['jumlah_vaksinasi_1'].apply(pd.to_numeric), name='Harian Vaksinasi ke-1'))
      fig_vax.layout.update(title_text='Harian Vaksinasi ke-1', 
                       xaxis_rangeslider_visible=True, 
                       hovermode='x',
                       legend_orientation='v')
      st.plotly_chart(fig_vax, use_container_width=True)
else:
    if vax_select == 'Kumulatif':
      fig_vax.add_trace(go.Scatter(x=vax_daily['Date'], y=vax_daily['jumlah_jumlah_vaksinasi_2_kum'], name='Kumulatif Vaksinasi ke-2'))
      fig_vax.layout.update(title_text='Kumulatif Vaksinasi ke-2', 
                       xaxis_rangeslider_visible=False, 
                       hovermode='x',
                       legend_orientation='v')
      st.plotly_chart(fig_vax, use_container_width=True)
    else:
      fig_vax.add_trace(go.Bar(x=vax_daily['Date'], y=vax_daily['jumlah_vaksinasi_2'].apply(pd.to_numeric), name='Harian Vaksinasi ke-2'))
      fig_vax.layout.update(title_text='Harian Vaksinasi ke-2', 
                       xaxis_rangeslider_visible=True, 
                       hovermode='x',
                       legend_orientation='v')
      st.plotly_chart(fig_vax, use_container_width=True)
st.markdown(hide_menu, unsafe_allow_html=True)