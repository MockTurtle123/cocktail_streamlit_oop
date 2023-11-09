import streamlit as st
import json
import functions


with open('recipes.json', 'r', encoding='utf-8') as file:
    contents = file.read()

recipes = json.loads(contents)

#ingr_list = []

ingr_list = functions.get_ingr_list(recipes)

# page layout
st.set_page_config(layout='wide')

st.header('Cocktail Database')

col1, col2 = st.columns([0.5, 1.5])
with col1:
    ingr_filter = st.selectbox("Search by ingredient", ingr_list, None)
    ingr_selection = ingr_filter
    name_select = st.selectbox('Available recipes:',
                               functions.get_name_list(ingr_selection,recipes))

with col2:
    info = functions.display_info(name_select, recipes)
    info_str = '\n'.join(info)
    c = st.container()
    #for row in info:
      #  c.info(row)
    c.info(info_str)