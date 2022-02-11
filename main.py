"""HTML-map"""
from cmath import pi
import re
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from folium.plugins import MarkerCluster
import argparse


def parcer():
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

# year_entered = 2014
# latttitude = 55.78
# longtitude = 45.77
# file_url = "llist"

# year_entered = 2000
# latttitude = 49.83826
# longtitude = 24.02324
# file_url = "llist"

# python3 main.py 2014 55.78 45.77 "llist" 
# python3 main.py 2000 49.83826 24.02324 "llist" 

def readingfile(file_url):
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
    """  Добавляэ в словник щоб уникнуи повтрыв"""
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
    """ Обчислюэ выдстань мж двома точкамим сортуэ за выдстаню обрызаэ першихм10"""
    main_list = []
    coord_2 = str(latttitude) + ',' + str(longtitude)
    for key in mass_coords:
        coord_1 = str(key[0]) + "," + str(key[1])
        main_list.append([mass_coords[key], key, geodesic(coord_1, coord_2).kilometers])
    main_list.sort(key = lambda x: x[2])
    return main_list[:10]

def build_map(main_list, longtitude, latttitude):
    """будуэ карту з фолыум використовує маркеткаластер з плагінів та групу маркрів ддля того щоб створити 3 шари карти що вимагає умова
    створюєм айфрейм щоб створити віконечко з текстом"""
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
        markers_group.add_child(folium.Marker(location = element[1], popup = folium.Popup(text), icon = folium.Icon(color = "red")))
    
    map.add_child(folium.LayerControl())
    map.save("map.html")

year_entered, latttitude, longtitude, file_url = parcer()
main_mass = readingfile(file_url)
mass_coords = calculate_coordinates(main_mass, year_entered)
closest_list = calcutale_distance(mass_coords, latttitude, longtitude)
build_map(closest_list, latttitude, longtitude)
