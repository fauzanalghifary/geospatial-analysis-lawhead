from google.transit import gtfs_realtime_pb2
from urllib.request import Request, urlopen
import folium
import time


def get_bus():
    """Returns the most recent latitude and
    longitude of the selected bus line using
    the GTFS Real-Time Washington Metropolitan Area 
    Transit Authority API to grab the first available
    public bus in the feed.
    """
    bus_lat = False
    bus_lon = False
    feed = gtfs_realtime_pb2.FeedMessage()
    req = Request('https://api.wmata.com/gtfs/bus-gtfsrt-vehiclepositions.pb')
    req.add_header('api_key', 'd4d713a59a9f477fab8c1e9fbadbd467')
    response = urlopen(req)
    feed.ParseFromString(response.read())
    bus = feed.entity[0]
    bus_lat = bus.vehicle.position.latitude
    bus_lon = bus.vehicle.position.longitude
    return(bus_lat, bus_lon)


def bus_map(mapimg):
    """Plots a nextbus location on an interactive map."""
    # Fetch the latest bus location
    lat, lon = get_bus()
    print(f"Located bus at {lon}, {lat}")
    if not lat:
        return False
    m = folium.Map(location=[lat, lon], tiles="OpenStreetMap", zoom_start=18)
    folium.Marker([lat, lon], tooltip="Bus location").add_to(m)
    m.save("{}.html".format(mapimg))
    return True

# Name of map image to save as PNG
nextimg = "bus_map"

# Number of updates we want to make
requests = 3

# How often we want to update (seconds)
freq = 5

# Map the bus location every few seconds
for i in range(requests):
    success = bus_map(nextimg)
    if not success:
        print("No data available.")
        continue
    print(f"Saved map {i} at {time.asctime()}")
    time.sleep(freq)
