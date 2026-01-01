# config.py

restaurant_list = [
    "ranaacurryhouse",
    "chelveiscurryhouse",
    "pelitanasi",
    "foodieedemo",
    "eltacoexpress1",
    "eltacoexpress2",
]

# Default selected restaurant (ONE TIME)
restaurant = restaurant_list[0]

def set_restaurant(name):
    global restaurant
    if name not in restaurant_list:
        raise ValueError(f"Restaurant '{name}' not found")
    restaurant = name
    print(f"🏪 Active restaurant set to: {restaurant}")
