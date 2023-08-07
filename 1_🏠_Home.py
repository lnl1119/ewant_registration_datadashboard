import streamlit as st
import pandas as pd
import plost
import datetime

st.set_page_config(page_title= "ewant data dashboard",
                   page_icon = "🌊",
                   layout='wide', 
                   initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('💥每日登入人數選項')
plot_data = st.sidebar.multiselect('Select data', ['2022', '2021', '2020', '2019', '2018', '2017', '2016'])
plot_height = st.sidebar.slider('Specify plot height', 300, 600, 500) # 高度可調整範圍預設為250

# Create a datetime slider with a range of one week
start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(weeks=1)
 
selected_date = st.sidebar.slider(
    "Select a date range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    step=datetime.timedelta(days=1),
)

# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)
# start_date = st.sidebar.date_input('Start date', today)
# end_date = st.sidebar.date_input('End date', tomorrow)
# if start_date > end_date:
#     st.sidebar.error('Error: End date must fall after start date.')
# if start_date < end_date:
#     st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.sidebar.error('Error: End date must fall after start date.')


# st.sidebar.markdown('''
# ---
# Created with ❤️ by [Data Professor](https://youtube.com/dataprofessor/).
# ''')


# Row A
# st.markdown('### Metrics')
# col1, col2, col3 = st.columns(3)
# col1.metric("Temperature", "70 °F", "1.2 °F")
# col2.metric("Wind", "9 mph", "-8%")
# col3.metric("Humidity", "86%", "4%")

# Row B
seattle_weather = pd.read_csv('/Users/leeliang/Desktop/dashboard-v2-master/raw.githubusercontent.com_tvst_plost_master_data_seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('/Users/leeliang/Desktop/dashboard-v2-master/raw.githubusercontent.com_dataprofessor_data_master_stocks_toy.csv')
login_20162022_done = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/login_20162022_done.csv")
login_20162022_raw = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/login_2016to2022.csv")

                     
c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom', 
        use_container_width=True)

# Row C
st.markdown('### ewant平台每日登入人數統計圖')
st.line_chart(login_20162022_raw, x = 'date', y = plot_data, height = plot_height)