import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import plost
import plotly.express as px
import datetime
# import mysql.connector
# mysql.connector.connect(
#     host = 
# )

########################################
########## initial settings ##########
########################################
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

st.set_page_config(page_title = "ewant data dashboard",
                page_icon = "🌊",
                layout ='wide', 
                initial_sidebar_state=st.session_state.sidebar_state)
# let default sidebar control button disappear
# go to website inspection, find the control button class
st.markdown("""
<style>
 .css-k4p6xk {display: none;}
 .css-jzqloi {display: none;}
</style>
""", unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# sidebar show/hide control button
if st.button('開啟/關閉側邊欄'):
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    st.experimental_rerun()

########################################
################# data #################
########################################
login_20162022_raw = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/login_2016to2022.csv")
regeister_20142022_raw = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/register_2014to2022.csv")
login_20162022_done = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/login_20162022_done.csv")
register20230717_df = pd.read_csv("https://raw.githubusercontent.com/lnl1119/ewant_registration_datadashboard/main/registerdata20230717.csv")

########################################
########## data preprocessing###########
########################################
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
########################################
############### variable ###############
########################################
today_date = datetime.date.today()
yesterday_date = today_date - datetime.timedelta(days=1)
lastweek_date = today_date - datetime.timedelta(weeks=1)
color_list = ["#ff80ed", "#065535", "#000000", "#008080", "#ff0000", "#ffd700", 
"#ffa500", "#c6e2ff", "#0000ff"]

########################################
############### function ###############
########################################
def register_check_change():
# this runs BEFORE the rest of the script when a change is detected 
# from your checkbox to set selectbox
    if st.session_state.all_option:
        st.session_state.register_year_select = register_year_list
    else:
        st.session_state.register_year_select = []
    return

def register_multi_change():
# this runs BEFORE the rest of the script when a change is detected
# from your selectbox to set checkbox
    if len(st.session_state.register_year_select) == len(register_year_list):
        st.session_state.all_option = True
    else:
        st.session_state.all_option = False
    return

def login_check_change():
    if st.session_state.login_all_option:
        st.session_state.login_year_select = login_year_list
    else:
        st.session_state.login_year_select = []
    return

def login_multi_change():
    if len(st.session_state.login_year_select) == len(login_year_list):
        st.session_state.login_all_option = True
    else:
        st.session_state.login_all_option = False
    return

#######################################
# https://discuss.streamlit.io/t/select-all-checkbox-that-is-linked-to-selectbox-of-options/18521

#######################################


########################################
############## home page ###############
########################################

# when sidebar shows, navigation bar is on the sidebar
if st.session_state.sidebar_state == 'expanded':
    # sidebar navigation menu
    with st.sidebar:
        selected = option_menu(
            menu_title = "menu", 
            options=["Home","other"], 
            icons = ["house-fill", "bar-chart-line-fill"],
            menu_icon = "three-dots-vertical",
            default_index = 0,
            styles={
                    #"container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "22px"},
                    "nav-link": {
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "#36b9cc"},
                },
            
        )

    # if home page being selected
    if selected == "Home":
        st.title(f"{selected}")
        # sidebar
        st.sidebar.subheader('💥每週註冊人數選項')
        register_year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']
        # on the first run add variables to track in state
        if "all_option" not in st.session_state:
            st.session_state.all_option = True
            st.session_state.register_year_select = register_year_list

        register_year_select = st.sidebar.multiselect("Select one or more options:",
                register_year_list,key="register_year_select", on_change = register_multi_change)

        all = st.sidebar.checkbox("Select all", key='all_option',on_change = register_check_change)
        ###############################################################3
        st.sidebar.subheader('💥每日登入人數選項')
        login_year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016']
        # on the first run add variables to track in state
        if "login_all_option" not in st.session_state:
            st.session_state.login_all_option = True
            st.session_state.login_year_select = login_year_list


        login_year_select = st.sidebar.multiselect("Select one or more options:",
                login_year_list,key="login_year_select", on_change=login_multi_change)

        all = st.sidebar.checkbox("Select all", key='login_all_option',on_change= login_check_change)

        ##################################################3

        # Row A
        # https://discuss.streamlit.io/t/select-all-on-a-streamlit-multiselect/9799/2
        # https://discuss.streamlit.io/t/change-metrci-color-font-background-and-style/25309
        # https://discuss.streamlit.io/t/select-all-checkbox-that-is-linked-to-selectbox-of-options/18521
        
        # st.markdown('### 大綱')
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
    
    # if "other" page being selected
    if selected == "other":
        st.title(f"{selected}")
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
            domain_expander = st.expander("點我查看資料")
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
            country_expander = st.expander("點我查看資料")
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

# when sidebar hides, navigation bar is on the main page
elif st.session_state.sidebar_state == 'collapsed': 
    # no sidebar navigation menu
    # selected2 = option_menu(None, ["Home", "other"], 
    # icons=['house', 'cloud-upload'], 
    # menu_icon="cast", default_index=0, orientation="horizontal",
    # styles={
    #             #"container": {"padding": "0!important", "background-color": "#fafafa"},
    #             "icon": {"color": "orange", "font-size": "22px"},
    #             "nav-link": {
    #                 "font-size": "20px",
    #                 "text-align": "left",
    #                 "margin": "0px",
    #                 "--hover-color": "#eee",
    #             },
    #             "nav-link-selected": {"background-color": "#36b9cc"},
    #         },
    # )

    
    selected2 = option_menu(
        menu_title = None, 
        options=["Home","other"], 
        icons = ["house-fill", "bar-chart-line-fill"],
        
        default_index = 0,
        styles={
                "container": {"padding": "0!important", "background-color": "#edecf0"},
                "icon": {"color": "orange", "font-size": "22px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "center",
                    "margin": "6px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#36b9cc"},
            },
        orientation="horizontal",
        navbar_mode = 'pinned',
    )
    #hide_streamlit_markers=False
    # selected2
    if selected2 == "Home":
        st.title(f"{selected2}")
    if selected2 == "other":
        st.title(f"{selected2}")
