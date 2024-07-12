import pandas
import streamlit as st

df = pandas.read_json('recipes.json')


def convert(cl: int) -> int:
    ml = cl * 10
    return int(ml)


def get_name_list(recipe_book, ingredient: str) -> list[str]:
    if not ingredient:
        name_list = recipe_book['name'].values
        return sorted(name_list)
    else:
        found_matches = []
        for index, recipe in recipe_book.iterrows():
            for item in recipe['ingredients']:
                try:
                    if ingredient in item['ingredient']:
                        found_matches.append(recipe['name'])
                except KeyError:
                    continue
        return sorted(found_matches)


def get_ingredients_list(recipe_book) -> list[str]:
    ingr_list = []
    for index, recipe in recipe_book.iterrows():
        for item in recipe['ingredients']:
            try:
                if item['ingredient'] not in ingr_list:
                    ingr_list.append(item['ingredient'])
            except KeyError:
                pass
    return sorted(ingr_list)


class Cocktail:
    def __init__(self, name):
        self.name = name
        self.row_index = df.index[df['name'] == name].tolist()
        self.ingredient_list = df.iloc[self.row_index]['ingredients'].squeeze()
        self.garnish = df.iloc[self.row_index]['garnish'].squeeze()
        self.glass = df.iloc[self.row_index]['glass'].squeeze()
        self.preparation = df.iloc[self.row_index]['preparation'].squeeze()

    def extract_ingredient_list(self) -> str:
        ingredients: str = "Ingredients:\n"
        for item in self.ingredient_list:
            try:
                ingredients += f"{convert(item['amount'])}ml of {item['ingredient']} ({item['label']})\n"
            except KeyError:
                try:
                    ingredients += f"{convert(item['amount'])}ml of {item['ingredient']}\n"
                except KeyError:
                    pass
        ingredients += '\n'
        return ingredients

    def extract_garnish(self) -> str:
        if self.garnish:
            garnish: str = f"\nUsually garnished with {self.garnish.lower()}\n"
            return garnish
        else:
            pass

    def extract_glass(self) -> str:
        if self.glass:
            article: str = "an" if self.glass.startswith("o") else "a"
            glass: str = f"{self.name} is typically served in {article} {self.glass} glass.\n\n"
            return glass
        else:
            pass

    def extract_preparation(self) -> str:
        if self.preparation:
            preparation = "Preparation:\n\n" + self.preparation
            return preparation
        else:
            pass

    def print_recipe(self, glass=True, ingredient_list=True, garnish=True, preparation=True) -> str:
        info_list = []

        if glass:
            info_list.append(self.extract_glass())

        if ingredient_list:
            info_list.append(self.extract_ingredient_list())

        if garnish:
            info_list.append(self.extract_garnish())

        if preparation:
            info_list.append(self.extract_preparation())

        info_str: str = '\n'.join(info_list)
        return info_str


# page layout
st.set_page_config(layout='wide')

st.header('Cocktail Database')

col1, col2 = st.columns([0.5, 1.5])
with col1:
    ingr_filter = st.selectbox("Search by ingredient", get_ingredients_list(df), None)
    name_select = st.selectbox('Available recipes:',
                               get_name_list(df, ingr_filter), None)
    cocktail = Cocktail(name_select)

with col2:
    if name_select:
        info = cocktail.print_recipe()
        c = st.container()
        c.info(info)