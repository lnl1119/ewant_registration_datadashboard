import streamlit as st
import pandas as pd
import plost
import plotly.express as px
import datetime

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
register20230717_df = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/registerdata20230717.csv")


# data preprocessing for register
## email domain
email_list = register20230717_df["email"].values
domain_name_list = [i[i.index('@') + 1 : ] for i in email_list]
domain_list = ["edu.tw", "gmail", "qq", "yahoo", "hotmail"]
each_domain_count_list = [len([i for i in domain_name_list if d in i]) for d in domain_list]
data = {'domain': domain_list + ["other"],
        'count': each_domain_count_list + [len(domain_name_list) - sum(each_domain_count_list)]}
domain_count_df = pd.DataFrame(data)


## country
register20230717_df['country'] = register20230717_df['country'].replace(['""'], '未填')
country_count_df = pd.DataFrame(register20230717_df['country'].value_counts())
country_count_df.reset_index(inplace=True)
country_count_df.columns = ["country", "count"]
country_dict = {
    'TW' : '台灣', 'MY' : '馬來西亞', 'CN' : '中國大陸', 'VN' : '越南', 'PY' : '巴拉圭', 
    'HK' : '香港', 'ID' : '印尼', 'JP' : '日本', 'TH' : '泰國', 'MO' : '澳門',
    'US' : '美國', 'AL' : '阿爾巴尼亞', 'PK' : '巴基斯坦', 'AU' : '澳大利亞', 'AE' : '阿拉伯聯合大公國', 
    'GM' : '甘比亞', 'CA' : '加拿大', 'KR' : '韓國', 'DE' : '德國', 'PH' : '菲律賓', 
    'IE' : '愛爾蘭','CY' : '塞普路斯', 'GB' : '英國', 'FR' : '法國', 'LU' : '盧森堡', 
    'TF' : '法屬南部屬地', 'PM' : '聖匹及密啟倫群島', 'SV' : '薩爾瓦多', 'MS' : '蒙瑟拉特島', 'BH' : '巴林', 
    'AF' : '阿富汗', 'SD' : '蘇丹'}
country_count_df.replace({"country": country_dict},inplace=True)

##########################################                     
# plot pie chart
c1, c2 = st.columns(2)
with c1:
    st.markdown('### 📩註冊者:blue[信箱]分佈')
    domain_max_type = domain_count_df['domain'][domain_count_df['count'] == domain_count_df['count'].max()].values[0]
    st.write(f"最多註冊者信箱網域為： :blue[{domain_max_type}]")
    email_pie_chart = px.pie(domain_count_df, values='count', names='domain')# , title = "註冊者信箱分佈"
    email_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(email_pie_chart)
    
    

    # st.dataframe resources
    # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    # https://docs.kanaries.net/tutorials/Streamlit/streamlit-dataframe
    domain_expander = st.expander("點我看資料")
    domain_expander.dataframe(
        domain_count_df,
        column_config={
            "domain": "網域",
            "count": "數量",
        },
        hide_index=True,
        use_container_width = True,
        height = 250
    )
    
with c2:
    st.markdown('### 🇹🇼註冊者:blue[國家]分佈')
    country_max_type = country_count_df['country'][country_count_df['count'] == country_count_df['count'].max()].values[0]
    st.write(f"最多註冊者國家為： :blue[{country_max_type}]")
    country_pie_chart = px.pie(country_count_df, values='count', names='country')
    country_pie_chart.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(country_pie_chart)
    country_expander = st.expander("點我看資料")
    #country_expander.table(country_count_df.head(30))
    country_expander.dataframe(
        country_count_df,
        column_config={
            "country": "國家",
            "count": "數量",
        },
        hide_index=True,
        use_container_width = True,
        height = 250
    )

##########################################
st.divider()
##########################################
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