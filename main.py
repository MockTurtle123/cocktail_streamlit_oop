import pandas
import streamlit as st
import backend

df = pandas.read_json('recipes.json')  # load recipe book


# page layout
st.set_page_config(layout='wide')

st.header('Cocktail Database')

col1, col2 = st.columns([0.5, 1.5])
with col1:
    ingredient_filter = st.selectbox("Search by ingredient", backend.get_ingredients_list(df), None)
    name_select = st.selectbox('Available recipes:',
                               backend.get_name_list(df, ingredient_filter), None)

    cocktail = backend.Cocktail(name_select, df)

with col2:
    if name_select:
        info = cocktail.print_recipe()
        c = st.container()
        c.info(info)