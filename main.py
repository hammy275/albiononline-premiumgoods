import requests
import json


def get_city_by_id(item_id):
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
    r = requests.get(url)
    return json.loads(r.text)


def get_item_data(items, locations):
    items = list(items)
    for i in range(len(items)):
        items[i] = ",".join(items[i])
    items = ",".join(items)
    url = "https://albion-online-data.com/api/v2/stats/prices/{}?locations={}".format(
        items, ",".join(locations)
    )
    return get_request(url)

def gen_treasure_names(name):
    names = []
    for i in range(3):
        names.append("TREASURE_{}_RARITY{}".format(name.upper(), str(i+1)))
    return names


def get_input(question, answers, default=None):
    answer = None
    while not answer or answer not in answers:
        answer = input(question).lower()
        if answer == "" and default:
            answer = default
    return answer


def get_lowest_price(price_dict):
    lowest_price = 999999
    lowest_city_from = None
    item = None
    for i in range(len(price_dict)):
        if price_dict[list(price_dict.keys())[i]][0] < lowest_price and price_dict[list(price_dict.keys())[i]][0] > 10:
            lowest_price = price_dict[list(price_dict.keys())[i]][0]
            lowest_city_from = price_dict[list(price_dict.keys())[i]][1]
            item = list(price_dict.keys())[i]
    return (item, lowest_price, lowest_city_from)



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
            if key["buy_price_max"] < lowest_price and key["buy_price_max"] > 10:
                lowest_price = key["buy_price_max"]
                lowest_price_city = key["city"]
        if key["item_id"].endswith("1"):
            t4_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
        elif key["item_id"].endswith("2"):
            t5_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
        else:
            t6_price_pairs[key["item_id"]] = (lowest_price, lowest_price_city)
    t4_lowest = get_lowest_price(t4_price_pairs)
    print("Lowest for T4 is from {} to {} at approximately {} silver per item".format(t4_lowest[2], get_city_by_id(t4_lowest[0]), t4_lowest[1]))
    t5_lowest = get_lowest_price(t5_price_pairs)
    print("Lowest for T5 is from {} to {} at approximately {} silver per item".format(t5_lowest[2], get_city_by_id(t5_lowest[0]), t5_lowest[1]))
    t6_lowest = get_lowest_price(t6_price_pairs)
    print("Lowest for T6 is from {} to {} at approximately {} silver per item".format(t6_lowest[2], get_city_by_id(t6_lowest[0]), t6_lowest[1]))


if __name__ == '__main__':
    main()