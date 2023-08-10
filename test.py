import streamlit as st
from streamlit_option_menu import option_menu


if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'


st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state, layout = "wide")
# let default sidebar control button disappear
# go to website inspection, find the control button class
st.markdown("""
<style>
 .css-k4p6xk {display: none;}
 .css-jzqloi {display: none;}
</style>
""", unsafe_allow_html=True)


if st.button('開啟/關閉側邊欄'):
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    st.experimental_rerun()

########################################################################
# when sidebar shows, navigation bar is on the sidebar
if st.session_state.sidebar_state == 'expanded':
    with st.sidebar:
        selected = option_menu(
            menu_title = "menu", 
            options=["Home","other"], 
            icons = ["house-fill", "bar-chart-line-fill"],
            menu_icon = "three-dots-vertical",
            default_index = 0,
            styles={
                    
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
    if selected == "Home":
        st.title(f"{selected}")
    if selected == "other":
        st.title(f"{selected}")

########################################################################
########################################################################
########################################################################
# when sidebar hides, navigation bar is on the main page
elif st.session_state.sidebar_state == 'collapsed': 
    selected2 = option_menu(None, ["Home", "other"], 
    icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "#fafafa"}},
    )
    # selected2
    if selected2 == "Home":
        st.title(f"{selected2}")
    if selected2 == "other":
        st.title(f"{selected2}")


#########################################################
# import streamlit as st
# from streamlit_option_menu import option_menu

# # 1. as sidebar menu
# with st.sidebar:
#     selected = option_menu("Main Menu", ["Home", 'Settings'], 
#         icons=['house', 'gear'], menu_icon="cast", default_index=1)
#     selected

# # 2. horizontal menu
# selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal")
# selected2

# # 3. CSS style definitions
# selected3 = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal",
#     styles={
#         "container": {"padding": "0!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"}, 
#         "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "green"},
#     }
# )

# # 4. Manual Item Selection
# if st.session_state.get('switch_button', False):
#     st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 4
#     manual_select = st.session_state['menu_option']
# else:
#     manual_select = None
    
# selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     orientation="horizontal", manual_select=manual_select, key='menu_4')
# st.button(f"Move to Next {st.session_state.get('menu_option',1)}", key='switch_button')
# selected4

# # 5. Add on_change callback
# def on_change(key):
#     selection = st.session_state[key]
#     st.write(f"Selection changed to {selection}")
    
# selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         on_change=on_change, key='menu_5', orientation="horizontal")
# selected5