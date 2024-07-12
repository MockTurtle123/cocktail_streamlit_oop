

def convert_cl(cl):
    """ Returns milliliters"""
    return int(cl * 10)


def get_ingr_list(recipe_book):
    ingr_list = []
    for cocktail in recipe_book:
        for item in cocktail['ingredients']:
            try:
                if item['ingredient'] not in ingr_list:
                    ingr_list.append(item['ingredient'])
            except KeyError:
                pass
    return sorted(ingr_list)


def get_name_list(ingredient, recipe_book):
    name_list = []
    if not ingredient:
        for cocktail in recipe_book:
            name_list.append(cocktail['name'])
        return sorted(name_list)
    else:
        found_matches = []
        for cocktail in recipe_book:
            for item in cocktail['ingredients']:
                try:
                    if ingredient in item['ingredient']:
                        found_matches.append(cocktail['name'])
                except KeyError:
                    continue
        return sorted(found_matches)




def display_info(name, recipe_book):
    info = []
    for cocktail in recipe_book:
        if cocktail['name'] == name:
            article = "an" if cocktail['glass'].startswith("o") else "a"
            info.append(f"{cocktail['name']} is typically served in {article} "
                        f"{cocktail['glass']} glass.\n\n"
                        f"Ingredients:\n")
            for item in cocktail["ingredients"]:
                try:
                    info.append(f"{convert_cl(item['amount'])}ml of {item['ingredient']} ({item['label']})\n")
                except KeyError:
                    try:
                        info.append(f"{convert_cl(item['amount'])}ml of {item['ingredient']}\n")
                    except KeyError:
                        pass
            info.append('\n')
            for item in cocktail["ingredients"]:
                try:
                    info.append(item['special'] + '\n')
                except KeyError:
                    pass
            info.append('\n')
            try:
                info.append(f"\nUsually garnished with {cocktail['garnish'].lower()}\n")
            except KeyError:
                pass

            try:
                info.append(f"Preparation:\n")
                info.append(f"{cocktail['preparation']}")
            except KeyError:
                pass

    return info


def search_by_ingredient(ingredient, recipe_book):
    found_matches = []
    for cocktail in recipe_book:
        for item in cocktail['ingredients']:
            try:
                if ingredient in item['ingredient']:
                    found_matches.append(cocktail['name'])
            except KeyError:
                continue
    return sorted(found_matches)
