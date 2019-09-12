# INSTRUCTIONS :
# We have a list of campers. Each camper has a location (latitude and longitude).
# We also have a list of searches.
# Each search also have a location (latitude and longitude).
# To filter the campers, we must use a bounding box that is 2 degrees square in total (ie,
# +/-0.1 from each coordinate)
# ################################################### LEVEL 2 ##########################################################
# Results are ordered by price, from cheapest to more expensive.
# If no dates are provided, the price is the price_per_day. The
# weekly_discount is applied for rentals of 7 days or more
import json


def make_square(lat, lon):
    """ Create the square (location limits
    :param lat = current latitude of user
    :param lon = current longitude of user"""
    square = [lat-0.1, lon-0.1, lat+0.1, lon+0.1]
    return square


def date_in_nm(date):
    """ convert the given date (format aaaa-mm-dd) to a number in format aaaammdd
    :param date"""
    date = date.replace("-", "")
    date = int(date)
    return date


def find_nb_days(start, end):
    """ return the amount of days between start and end dates
    :param start = start date
    :param end = en date"""
    # convert dates in numbers
    start = date_in_nm(start)
    end = date_in_nm(end)
    nb_days = end - start + 1
    return nb_days


def find_price(period, price_per_day, discount):
    """ find rental price for specific camper and specific time
    :param period = delta between the end date and the start date
    :param price_per_day
    :param discount = discount to apply only if period > 7 days
    :return price_to_pay = price including discount"""
    if period == 0:
        price_to_pay = price_per_day
    else:
        if period < 7:
            discount = 0
        price_to_pay = price_per_day * period
        price_to_pay = price_to_pay - (price_to_pay * discount)
    return price_to_pay


def find_campers(period, square, campers):
    """ find campers in the json string
    :param period = delta between the end date and the start date
    :param square = [minimal latitude, minimal longitude, maximal latitude, maximal longitude]
    :param campers"""
    res = []
    for i in campers["campers"]:
        if (i["latitude"] > square[0]) \
            and (i["latitude"] < square[2]) \
            and (i["longitude"] > square[1]) \
                and (i["longitude"] < square[3]):
            if "weekly_discount" not in i:
                price = find_price(period, i["price_per_day"], 0)
            else:
                price = find_price(period, i["price_per_day"], i["weekly_discount"])
            res.append({"camper_id": i["id"], "price": price})
    res = sorted(res, key=lambda k: k['price'], reverse=False)
    return res


def search_in_json():
    """ find in the json files """
    # open file and save items to search in a var
    items_to_search = {}
    with open("data/searches.json", "r") as json_search_file:
        items_to_search = json.load(json_search_file)
    json_search_file.close()

    # open file and save campers in a var
    campers = {}
    with open("data/campers.json", "r") as json_campers_file:
        campers = json.load(json_campers_file)
    json_campers_file.close()

    # find corresponding campers for each searched item
    results = {"results": []}
    for i in items_to_search['searches']:
        square = make_square(i["latitude"], i["longitude"])
        if "start_date" not in i \
                or "end_date" not in i:
            period = 0
        else:
            period = find_nb_days(i["start_date"], i["end_date"])
        res = find_campers(period, square, campers)
        results["results"].append({"search_id": i["id"], "search_results": res})

    # save result in new var
    with open("data/results.json", "w") as json_results_file:
        json.dump(results, json_results_file)
    json_results_file.close()
    # write in a new file
    return 0


search_in_json()
