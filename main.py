#!/usr/bin/python3
import requests
import json


def print_info():
    """Prints some Useful Info."""
    print("Luxury Good Sell Values:")
    print("\n\nNon-Premium:\nT4: 940 silver\nT5: 4,700 silver\nT6: 23,500 silver")
    print("\nPremium:\nT4: 970 silver\nT5: 4,850 silver\nT6: 24,250 silver\n")
    print("Lowest price luxury goods:")


def get_city_by_id(item_id):
    """Get City by Item ID.

    Given the item ID of a luxury good, return which city it needs to be brought to.

    Args:
        item_id (str): Item ID

    Returns:
        str: City name the item should be brought to.

    """
    ids_to_city = {
        "RITUAL": "Caerleon",
        "KNOWLEDGE": "Martlock",
        "SILVERWARE": "Lymhurst",
        "DECORATIVE": "Fort Sterling",
        "TRIBAL": "Bridgewatch",
        "CEREMONIAL": "Thetford"
    }
    for n in ids_to_city.keys():
        if n in item_id:
            return ids_to_city[n]


def get_request(url):
    """Simple GET Request.

    Args:
        url (str): URL with parameters to GET request to.

    Returns:
        dict: Dictionary form of a JSON response.

    """
    r = requests.get(url)
    return json.loads(r.text)


def get_item_data(items, locations):
    """Get Item Data.

    Given a list of items and locations, get the market info for them.

    Args:
        items (str[] or str[][]): List of items to get prices for.
        locations (str[]): Locations to get item pricing info from.

    Returns:
        dict: The dictionary response from albion-online-data.com

    """
    items = list(items)
    if type(items) is list:
        for i in range(len(items)):
            items[i] = ",".join(items[i])
    items = ",".join(items)
    url = "https://albion-online-data.com/api/v2/stats/prices/{}?locations={}".format(
        items, ",".join(locations)
    )
    return get_request(url)


def gen_treasure_names(name):
    """Get List of Treasure IDs by Type.

    Args:
        name (str): The name of the treasure (CEREMONIAL, KNOWLEDGE, etc.)

    Returns:
        str[]: The list of luxury goods IDs.

    """
    names = []
    for i in range(3):
        names.append("TREASURE_{}_RARITY{}".format(name.upper(), str(i+1)))
    return names


def get_input(question, answers, default=None):
    """Get User Input.

    Args:
        question (str): Question to ask user (passed directly to input())
        answers (str[]): List of possible answers. Must be all lowercase.
        default (str, optional): If specified, the answer to have if none is supplied. Defaults to None.

    Returns:
        str: The answer from the user.

    """
    answer = None
    while not answer or answer not in answers:
        answer = input(question).lower()
        if answer == "" and default:
            answer = default
    return answer


def get_lowest_price(price_dict):
    """Get Lowest Price.

    Get the lowest price for a given premium good from all of the lowest prices of that tier's premium good.

    Args:
        price_dict (dict): See usage in code for format of dict.

    Returns:
        tuple: The item id, the lowest price, and the city with that lowest price.

    """
    lowest_price = 999999
    lowest_city_from = None
    item = None
    for i in range(len(price_dict)):
        if price_dict[list(price_dict.keys())[i]][0] < lowest_price and price_dict[list(price_dict.keys())[i]][0] > 10:
            lowest_price = price_dict[list(price_dict.keys())[i]][0]
            lowest_city_from = price_dict[list(price_dict.keys())[i]][1]
            item = list(price_dict.keys())[i]
    return (item, lowest_price, lowest_city_from)


def is_neighbor(a, b):
    """Check if City Neighbors Another.

    Args:
        a (str): City A
        b (str): City B

    Returns:
        bool: Whether or not cities A and B neighbor each other.

    """
    if "Caerleon" in [a, b]:
        return True
    cities = ["Lymhurst", "Bridgewatch", "Martlock", "Thetford", "Fort Sterling"]
    start = cities.index(a)
    check_a = start - 1
    check_b = start + 1
    if check_a < 0:
        check_a = len(cities) - 1
    if check_b >= len(cities):
        check_b = 0
    return b in [cities[check_a], cities[check_b]]



def main():
    premium_goods_dict = {
        "Caerleon": gen_treasure_names("RITUAL"),
        "Martlock": gen_treasure_names("KNOWLEDGE"),
        "Lymhurst": gen_treasure_names("SILVERWARE"),
        "Fort Sterling": gen_treasure_names("DECORATIVE"),
        "Bridgewatch": gen_treasure_names("TRIBAL"),
        "Thetford": gen_treasure_names("CEREMONIAL")
    }
    use_caerleon = get_input("Check Caerleon? [y/N] ", ['y', 'n'], 'n')
    if use_caerleon != "y":
        del premium_goods_dict["Caerleon"]
    neighbor = get_input("Only check routes between neighbors? [y/N] ", ['y', 'n'], 'n')
    use_neighbors = neighbor == 'y'
    item_data = get_item_data(premium_goods_dict.values(), premium_goods_dict.keys())
    city_count = len(premium_goods_dict)
    item_count = len(premium_goods_dict.values()) * 3
    t4_price_pairs = {}
    t5_price_pairs = {}
    t6_price_pairs = {}
    for i in range(item_count):
        lowest_price = 999999
        lowest_price_city = None
        for c in range(city_count):
            key = item_data[i * city_count + c]
            if use_neighbors and not is_neighbor(key["city"], get_city_by_id(key["item_id"])):
                continue
            if key["buy_price_max"] < lowest_price and key["buy_price_max"] > 10:
                lowest_price = key["buy_price_max"]
                lowest_price_city = key["city"]
        if key["item_id"].endswith("1"):
            t4_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
        elif key["item_id"].endswith("2"):
            t5_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
        else:
            t6_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
    print_info()
    t4_lowest = get_lowest_price(t4_price_pairs)
    print("Lowest for T4 is from {} to {} at approximately {} silver per item".format(t4_lowest[2], get_city_by_id(t4_lowest[0]), t4_lowest[1]))
    t5_lowest = get_lowest_price(t5_price_pairs)
    print("Lowest for T5 is from {} to {} at approximately {} silver per item".format(t5_lowest[2], get_city_by_id(t5_lowest[0]), t5_lowest[1]))
    t6_lowest = get_lowest_price(t6_price_pairs)
    print("Lowest for T6 is from {} to {} at approximately {} silver per item".format(t6_lowest[2], get_city_by_id(t6_lowest[0]), t6_lowest[1]))


if __name__ == '__main__':
    main()
