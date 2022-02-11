# WEB-map project

The goal of that project was to create a module which generate the web-map as a HTML-file. The map consists of three different layers. To run the program the user enters a year, coordinates of the location and the dataset where the information contains. The module have to place the markers of ten closets points with film on it. 

## Description

The module has six functions:

1) Argparsing: is used for running the program in terminal with arguments
```python
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
```
2) Reading file: Read the file and return the list, which contains list with name, year and location, like this [name, year, location]

Example:
```bash
[['"#1 Single"', 2006, 'Los Angeles, California, USA'],...
```
3) Calculating coordinates: That function returns set, every element of which is a dictionary with key as coordinates and name as a value

I used geopy.geocoders to find the coordinates of the location:
```python
loc = Nominatim(user_agent = 'app').geocode(element[2])
```
4) Calculation of the distance: Calculate distance between two points, sort it and take only 10 first coordinates, using geodesic
```python
main_list = []
    coord_2 = str(latttitude) + ',' + str(longtitude)
    for key in mass_coords:
        coord_1 = str(key[0]) + "," + str(key[1])
        main_list.append([mass_coords[key], key, geodesic(coord_1, coord_2).kilometers])
    main_list.sort(key = lambda x: x[2])
    return main_list[:10]
```
5) Building of the map:  Function creates a map using folium, with 3 layers: map, markers, cluster we use marker cluster from plugins and and iframe to create a window with text
6) Main: runs all the function
```python
def main():
    year_entered, latttitude, longtitude, file_url = parcer()
    main_mass = readingfile(file_url)
    mass_coords = calculate_coordinates(main_mass, year_entered)
    closest_list = calcutale_distance(mass_coords, latttitude, longtitude)
    build_map(closest_list, latttitude, longtitude)
```

## Conclusion

The module creates a web-map, and give us information about the 10 closest marks to the coordinates of the location that the user enters where the films were filmed. Every mark has their own frame with text about that location.

## The example of running of the program

To run the program user have to enter three arguments into the command line the following, where the firs argument is year, second and third are coordinates of the location and fourth is the path to dataset:

```bash
python3 main.py 2014 55.78 45.77 path_to_dataset
```

Then will be created a new file with the map that can be named like that:

![This is an image](https://user-images.githubusercontent.com/93607175/153660276-30343982-61db-49b2-854d-ae59a1576f46.png)

And opening that file, you open the map and it shows the as it was said the 10 closest locations.

![This is an image](https://user-images.githubusercontent.com/93607175/153669070-0a9d0278-8437-43ba-87a2-29ef3c3dc665.png)

That map already has two layers (markers: red and cluster: green) on the map.
