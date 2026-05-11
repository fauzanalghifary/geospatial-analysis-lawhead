import osmnx as ox
G = ox.graph_from_place('Bay St. Louis, Mississippi, USA', network_type='drive')
stats = ox.basic_stats(G)
print(stats["street_length_avg"])
