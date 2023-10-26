import json
import pyproj


# Define the source and target coordinate systems
source_crs = pyproj.CRS("EPSG:28992")  # Dutch RD coordinate system
target_crs = pyproj.CRS("EPSG:4326")   # WGS 84 (latitude and longitude)

# Create a transformer to convert coordinates
transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

# Load the GeoJSON file
with open("C:/Users/924762/Documents/NT/WBD - Breda/polygons_irc.geojson", "r") as file:
    data = json.load(file)

# Function to recursively flatten nested lists of coordinates
def flatten_coordinates(coords):
    for item in coords:
        if isinstance(item, list):
            yield from flatten_coordinates(item)
        else:
            yield item

# Iterate through the features and convert coordinates
num_decimals = 6
for feature in data["features"]:
    coordinates = list(flatten_coordinates(feature["geometry"]["coordinates"]))
    converted_coordinates = [list(transformer.transform(x, y)) for x, y in zip(coordinates[::2], coordinates[1::2])]
    rounded_coordinates = [[round(x, num_decimals), round(y, num_decimals)] for x, y in converted_coordinates]
    feature["geometry"]["coordinates"] = [rounded_coordinates]

# Save the converted and rounded GeoJSON to a new file
with open("converted_and_rounded_geojson_6.geojson", "w") as output_file:
    json.dump(data, output_file, indent=2)

print("Conversion and rounding completed. The converted and rounded GeoJSON file has been saved.")