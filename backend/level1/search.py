# INSTRUCTIONS :
# We have a list of campers. Each camper has a location (latitude and longitude).
# We also have a list of searches.
# Each search also have a location (latitude and longitude).
# To filter the campers, we must use a bounding box that is 2 degrees square in total (ie,
# +/-0.1 from each coordinate)
import json


def make_square(lat, lon):
    """ Create the square (location limits
    :param lat = current latitude of user
    :param lon = current longitude of user"""
    square = [lat-0.1, lon-0.1, lat+0.1, lon+0.1]
    return square


def find_campers(square, campers):
    """ find campers in the json string
    param: square = [minimal latitude, minimal longitude, maximal latitude, maximal longitude]"""
    res = []
    for i in campers["campers"]:
        if (i["latitude"] > square[0]) \
            and (i["latitude"] < square[2]) \
            and (i["longitude"] > square[1]) \
                and (i["longitude"] < square[3]):
            res.append({"camper_id": i["id"]})
    return res


def search_in_json():
    """ find in the json files
    param: square = [minimal latitude, minimal longitude, maximal latitude, maximal longitude]"""
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
        res = find_campers(square, campers)
        results["results"].append({"search_id": i["id"], "search_results": res})
    # save result in new var
    with open("data/results.json", "w") as json_results_file:
        json.dump(results, json_results_file)
    json_results_file.close()
    # write in a new file
    return 0


search_in_json()
