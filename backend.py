import pandas


def convert(cl: int | float) -> int:  # convert cl to ml
    ml = cl * 10
    return int(ml)


def get_name_list(recipe_book: pandas.DataFrame, ingredient: str) -> list[str]:  # get names of cocktails from dataframe
    if ingredient:  # show only cocktails containing specific ingredient
        name_list = []
        for index, recipe in recipe_book.iterrows():
            for item in recipe['ingredients']:
                try:
                    if ingredient in item['ingredient']:
                        name_list.append(recipe['name'])
                except KeyError:
                    continue
    else:  # show all cocktails in the database
        name_list = recipe_book['name'].values

    return sorted(name_list)


def get_ingredients_list(recipe_book: pandas.DataFrame) -> list[str]:  # get ingredients of all cocktails from dataframe
    ingredients_list = []
    for index, recipe in recipe_book.iterrows():
        for item in recipe['ingredients']:
            try:
                if item['ingredient'] not in ingredients_list:
                    ingredients_list.append(item['ingredient'])
            except KeyError:
                pass
    return sorted(ingredients_list)


class Cocktail:
    def __init__(self, name, df):
        self.name = name
        self.row_index = df.index[df['name'] == name].tolist()
        self.ingredient_list = df.iloc[self.row_index]['ingredients'].squeeze()
        self.garnish = df.iloc[self.row_index]['garnish'].squeeze()
        self.glass = df.iloc[self.row_index]['glass'].squeeze()
        self.preparation = df.iloc[self.row_index]['preparation'].squeeze()

    def extract_ingredient_list(self) -> str:  # extract ingredient info from cocktail and format it
        ingredients: str = 'Ingredients:\n\n'
        for item in self.ingredient_list:
            try:
                ingredients += f"- {convert(item['amount'])}ml of {item['ingredient']} ({item['label']})\n\n"
            except KeyError:
                try:
                    ingredients += f"- {convert(item['amount'])}ml of {item['ingredient']}\n\n"
                except KeyError:
                    pass
            try:
                ingredients += f"- {item['special']}\n\n"
            except KeyError:
                pass

        return ingredients

    def extract_garnish(self) -> str:  # extract garnish info from cocktail and format it
        if self.garnish == self.garnish:  # check if value is not NaN
            garnish: str = f"\nUsually garnished with {self.garnish.lower()}\n"
            return garnish
        else:
            return ""

    def extract_glass(self) -> str:  # extract glass info from cocktail and format it
        if self.glass == self.glass:  # check if value is not NaN
            article: str = "an" if self.glass.startswith("o") else "a"
            glass: str = f"{self.name} is typically served in {article} {self.glass} glass.\n\n"
            return glass
        else:
            return ""

    def extract_preparation(self) -> str:  # extract preparation info from cocktail and format it
        if self.preparation == self.preparation:  # check if value is not NaN
            preparation = "Preparation:\n\n" + self.preparation
            return preparation
        else:
            return ""

    def print_recipe(self, glass=True, ingredient_list=True, garnish=True, preparation=True) -> str:
        info_list: list[str] = []

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
