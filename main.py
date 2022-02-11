"""HTML-map"""
import re
import argparse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from folium.plugins import MarkerCluster

def parcer():
    """
    Function for arparsing with 4 arguments
    """
    parser = argparse.ArgumentParser(description="Map")

    parser.add_argument("year_enetered", help='year enetered')
    parser.add_argument("latttitude", help='latttitude')
    parser.add_argument("longtitude", help='longtitude')
    parser.add_argument("file", help='file')

    args = parser.parse_args()
    year_entered = int(args.year_enetered)
    latttitude = float(args.latttitude)
    longtitude = float(args.longtitude)
    file_url = args.file
    return year_entered, latttitude, longtitude, file_url

def readingfile(file_url):
    """
    Read the file and return the list, which contains list with\
name, year and location, like this [name, year, location]
    >>> readingfile("locations.list") #doctest: +ELLIPSIS
    [['"#1 Single"', 2006, 'Los Angeles, California, USA'],...
    """
    list_for_lines = []
    with open(file_url, 'r', encoding = 'utf-8') as new_file:
        for i, line in enumerate(new_file):
            if not(0 <= i <= 13):
                line = line.rstrip()
                line = line.replace("\t", "")
                list_for_lines.append(line)

    thelistwithoufig = []
    for line in list_for_lines:
        if re.search(r"\{([^}]+)\}", line):
            replaced = "".join(re.findall(r"\{([^}]+)\}", line))
            line = line.replace(replaced, "")
            line = line.replace("{}", "")
            thelistwithoufig.append(line)
        else:
            thelistwithoufig.append(line)
    thelistwithoufiggand = []
    for line in thelistwithoufig:
        if line.endswith("(studio)"):
            line = line.replace("(studio)", "")
            if line.count("(") < 2:
                thelistwithoufiggand.append(line)
        elif line.endswith("(location)"):
            line = line.replace("(location)", "")
            if line.count("(") < 2:
                thelistwithoufiggand.append(line)
        elif "(TV)" in line:
            line = line.replace("(TV)", "")
            if line.count("(") < 2:
                thelistwithoufiggand.append(line)
        elif line.count("(") == 1:
            thelistwithoufiggand.append(line)

    namee= []
    yeaaarr = []
    for line in thelistwithoufiggand:
        if line.startswith('"'):
            name = re.findall(r'"[^"]*"', line)
            namee.append("".join(name))
        else:
            partitioned_string = line.partition('(')
            before_first = partitioned_string[0][:-1]
            namee.append(before_first)
        year = re.findall(r'^.*?\([^\d]*(\d+)[^\d]*\).*$', line)
        yeaaarr.append("".join(year))
    location = []
    for line in thelistwithoufiggand:
        newline = line.split(")")
        location.append(newline[1])

    zipall = list(zip(namee, yeaaarr, location))
    final_list = []
    final_list_num = []

    for line in zipall:
        if not(line[0] == "" or line[1] == "" or line[2] == ""):
            final_list_num.append(int(line[1]))
            final_list.append(line)

    list_of_lists_fi = [list(elem) for elem in final_list]
    for num in range(len(final_list)):
        list_of_lists_fi[num][1] = final_list_num[num]
    return list_of_lists_fi

def calculate_coordinates(main_mass, year_entered):
    """
    That function returns set, every element of which is a dictionary\
with key as coordiantes and name as a value
    >>> calculate_coordinates(main_mass[:5], 2014)
    {(30.2711286, -97.7436995): ['"#ATown"']}
    """
    return_list = {}
    for element in main_mass:
        if element[1] != year_entered:
            continue
        loc = Nominatim(user_agent = 'app').geocode(element[2])
        try:
            while loc == None:
                element[2] = element[2][element[2].find(",") + 1:]
                loc = Nominatim(user_agent = 'app').geocode(element[2])
        except IndexError:
            continue
        coords = (loc.latitude, loc.longitude)
        if coords not in return_list.keys():
            return_list[coords] = {element[0]}
        else:
            return_list[coords].add(element[0])
    for key in return_list:
        return_list[key] = list(return_list[key])
    return return_list

def calcutale_distance(mass_coords, longtitude, latttitude):
    """
    Calculate distance between two points, sort it\
and take only 10 first coordiantes.
    >>> calcutale_distance({(30.2711286, -97.7436995): ['"#ATown"']}, 45.77, 55.78)
    [[['"#ATown"'], (30.2711286, -97.7436995), 9861.626433190442]]
    """
    main_list = []
    coord_2 = str(latttitude) + ',' + str(longtitude)
    for key in mass_coords:
        coord_1 = str(key[0]) + "," + str(key[1])
        main_list.append([mass_coords[key], key, geodesic(coord_1, coord_2).kilometers])
    main_list.sort(key = lambda x: x[2])
    return main_list[:10]

def build_map(main_list, longtitude, latttitude):
    """
    Fucntion creates a map using folium, with 3 layers: map, markers, cluster\
we use marketcluster from plugins and and iframe to create a window woth text
    """
    map = folium.Map(location = [latttitude, longtitude], zoom_start = 3, control_scale = True)

    all_loc = [elem[1] for elem in main_list]

    markers_group = folium.FeatureGroup(name = "Markers", show = False)
    cluster = MarkerCluster(all_loc, name = "Cluster")
    map.add_child(markers_group)
    map.add_child(cluster)

    for element in main_list:
        text = element[0][0]
        for i in range(1, len(element[0])):
            text += ', ' + element[0][i]
        text = folium.IFrame(text, width = 200, height = 100)
        markers_group.add_child(folium.Marker(location = element[1], \
            popup = folium.Popup(text), icon = folium.Icon(color = "red")))

    map.add_child(folium.LayerControl())
    map.save("map.html")

def main():
    year_entered, latttitude, longtitude, file_url = parcer()
    main_mass = readingfile(file_url)
    mass_coords = calculate_coordinates(main_mass, year_entered)
    closest_list = calcutale_distance(mass_coords, latttitude, longtitude)
    build_map(closest_list, latttitude, longtitude)

if __name__ == '__main__':
    main()
