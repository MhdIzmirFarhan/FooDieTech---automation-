# config.py

restaurant_list = [
    "ranaacurryhouse",
    "chelveiscurryhouse",
    "thegangacafe",
    "amuthasfishheadcurry",
    "eltacoexpress1",
    "eltacoexpress2",
    "srivasanthavilash",
    "sriannamalaiunavagam",
    "canaicorner",
    "unclemisai",
    "devfrequency",
]

# Default selected restaurant (ONE TIME)
restaurant = restaurant_list[0]

def set_restaurant(name):
    global restaurant
    if name not in restaurant_list:
        raise ValueError(f"Restaurant '{name}' not found")
    restaurant = name
    print(f"🏪 Active restaurant set to: {restaurant}")
