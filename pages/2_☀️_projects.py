import streamlit as st
import pandas as pd
import plost
import plotly.express as px
import datetime

# data
login_20162022_raw = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/login_2016to2022.csv")
regeister_20142022_raw = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/register_2014to2022.csv")
login_20162022_done = pd.read_csv("/Users/leeliang/Desktop/dashboard_registration/login_20162022_done.csv")
# variable
today_date = datetime.date.today()
yesterday_date = today_date - datetime.timedelta(days=1)
lastweek_date = today_date - datetime.timedelta(weeks=1)
color_list = ["#ff80ed", "#065535", "#000000", "#008080", "#ff0000", "#ffd700", 
"#ffa500", "#c6e2ff", "#0000ff"]

# function

#######################################
# https://discuss.streamlit.io/t/select-all-checkbox-that-is-linked-to-selectbox-of-options/18521

#######################################

#######################################

# main 
st.set_page_config(page_title= "ewant data dashboard",
                   page_icon = "🌊",
                   layout='wide', 
                   initial_sidebar_state='expanded') 

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# sidebar
st.sidebar.subheader('💥每週註冊人數選項')
register_year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']
# on the first run add variables to track in state
if "all_option" not in st.session_state:
    st.session_state.all_option = True
    st.session_state.register_year_select = register_year_list

def check_change():
# this runs BEFORE the rest of the script when a change is detected 
# from your checkbox to set selectbox
    if st.session_state.all_option:
        st.session_state.register_year_select = register_year_list
    else:
        st.session_state.register_year_select = []
    return

def multi_change():
# this runs BEFORE the rest of the script when a change is detected
# from your selectbox to set checkbox
    if len(st.session_state.register_year_select) == len(register_year_list):
        st.session_state.all_option = True
    else:
        st.session_state.all_option = False
    return

register_year_select = st.sidebar.multiselect("Select one or more options:",
         register_year_list,key="register_year_select", on_change=multi_change)

all = st.sidebar.checkbox("Select all", key='all_option',on_change= check_change)
###############################################################3
st.sidebar.subheader('💥每日登入人數選項')
login_year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016']
# on the first run add variables to track in state
if "login_all_option" not in st.session_state:
    st.session_state.login_all_option = True
    st.session_state.login_year_select = login_year_list

def login_check_change():
# this runs BEFORE the rest of the script when a change is detected 
# from your checkbox to set selectbox
    if st.session_state.login_all_option:
        st.session_state.login_year_select = login_year_list
    else:
        st.session_state.login_year_select = []
    return

def login_multi_change():
# this runs BEFORE the rest of the script when a change is detected
# from your selectbox to set checkbox
    if len(st.session_state.login_year_select) == len(login_year_list):
        st.session_state.login_all_option = True
    else:
        st.session_state.login_all_option = False
    return

login_year_select = st.sidebar.multiselect("Select one or more options:",
         login_year_list,key="login_year_select", on_change=login_multi_change)

all = st.sidebar.checkbox("Select all", key='login_all_option',on_change= login_check_change)

##################################################3

# Row A
# https://discuss.streamlit.io/t/select-all-on-a-streamlit-multiselect/9799/2
# https://discuss.streamlit.io/t/change-metric-color-font-background-and-style/25309
# https://discuss.streamlit.io/t/select-all-checkbox-that-is-linked-to-selectbox-of-options/18521
st.markdown('### 大綱')

total_registration_count = 477275
lastweek_registration_count = 476849
increasefromlastweek_total_registration_count = total_registration_count - lastweek_registration_count
thisyear_registration_count = 39664

Acol1, Acol2, Acol3, Acol4 = st.columns(4)
Acol1.metric("總註冊人數", "{:,}".format(total_registration_count)+"人", str(increasefromlastweek_total_registration_count)+"人")
Acol2.metric("上週註冊人數", "{:,}".format(lastweek_registration_count)+"人", "-8%")
Acol3.metric("本年度註冊人數", "{:,}".format(thisyear_registration_count)+"人", "4%")
Acol4.metric("近期增加人數原因：", "SOS")
# col1.metric("累積至昨日"+str(today_date), "70 °F", "1.2 °F")
# col2.metric("昨日"+str(yesterday_date), "9 mph", "-8%")
# col3.metric("上週"+str(lastweek_date), "86%", "4%")

st.divider()

# Row B
Btab1, Btab2, Btab3 = st.tabs(["📈折線圖", "🔼面積圖", "熱圖"])
with Btab1:
    st.markdown('### ewant平台每週註冊人數統計圖')
    st.line_chart(regeister_20142022_raw, x = 'week', y = register_year_select, height = 500) # , height = register_plot_height
with Btab2:    
    st.markdown('### ewant平台每週註冊人數統計圖')
    st.area_chart(regeister_20142022_raw, x = 'week', y = register_year_select, height = 500)
with Btab3:
    st.markdown('### ewant平台每週註冊人數統計圖')
    plost.time_hist(
    data=login_20162022_done,
    date='date',
    x_unit='week',
    y_unit='day',
    color='value',
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
    #st.line_chart(regeister_20142022_raw, x = 'week', y = register_year_select, height = 500)


# Row C
Ctab1, Ctab2 = st.tabs(["📈折線圖", "🔼面積圖"])
with Ctab1:
    st.markdown('### ewant平台每日登入人數統計圖')
    st.line_chart(login_20162022_raw, x = 'date', y = login_year_select, height = 500)# , height = login_plot_height
with Ctab2:    
    st.markdown('### ewant平台每日登入人數統計圖')
    st.area_chart(login_20162022_raw, x = 'date', y = login_year_select, height = 500)# , height = login_plot_height



