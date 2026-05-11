import fiona
import os
from shapely.geometry import mapping, shape, LineString
from shapely.ops import nearest_points

# Did a quick manual check to see what the layer names are.
# You could do this programmatically by checking the geometry
# type.
#>>>fiona.listlayers("city.gpkg")
#   ['buildings', 'roads', 'layer_styles']

# Sample data: https://github.com/GeospatialPython/Learn/raw/master/city.gpkg

layers = fiona.listlayers("city.gpkg")
buildings_layer = next(layer for layer in layers if "buildings" in layer)
roads_layer = next(layer for layer in layers if "roads" in layer)

# Now we open the buildings layer and then the roads layer
with fiona.open("city.gpkg", layer=roads_layer) as roads:
    # Grab the roads metadata file as a template for our results output
    meta = roads.meta
    road_geometries = []
    for road in roads:
        road_geometry = shape(road["geometry"])
        if road_geometry.geom_type == "MultiLineString":
            road_geometries.extend(road_geometry.geoms)
        else:
            road_geometries.append(road_geometry)

with fiona.open("city.gpkg", layer=buildings_layer) as buildings:
    # The list of lines containing our result
    face_lines = []
    # Now we loop through each building to begin our algorithm
    for building in buildings:
        # Covert the building geometry to a Shapely feature
        building_shape = shape(building["geometry"])
        if building_shape.geom_type == "MultiPolygon":
            building_geometry = building_shape.geoms
        else:
            building_geometry = [building_shape]
        # Create the variables that monitor our loop checks until
        # we have the right answer.
        # The road closest to the building edge facing it.
        closest_road = None
        # The distance to the closest road to the building.
        closest_road_distance = None
        # The midpoint of the closest building edge to the road.
        closest_edge_midpoint = None
        # The buildings are multipolygons so we have to extract their
        # exterior rings.
        building_exterior_coords = []
        for poly in building_geometry:
            building_exterior_coords.extend(poly.exterior.coords)
        building_edges = LineString(building_exterior_coords)
        # Break the exterior ring feature back into points for 
        # edge detection
        edge_points = list(building_edges.coords)
        # Loop through the edges            
        for i,j in zip(edge_points, edge_points[1:]):
            # Compare edge midpoints to each road to see which is
            # the closest.  This takes awhile.
            current_edge = LineString((i,j))
            current_edge_midpoint = current_edge.interpolate(0.5, normalized = True)
            for road_geometry in road_geometries:
                current_road_distance = current_edge_midpoint.distance(road_geometry)
                if closest_road:
                    if current_road_distance < closest_road_distance:
                        closest_road_distance = current_road_distance
                        closest_road = road_geometry
                        closest_edge_midpoint = current_edge_midpoint
                else:
                    closest_road = road_geometry
                    closest_road_distance = current_road_distance
                    closest_edge_midpoint = current_edge_midpoint
        # Now that we found the closest edge midpoint to each road,
        # draw a line between the midpoint and the closest line
        # on the road.
        midpoint_to_road = nearest_points(closest_edge_midpoint, closest_road) 
        face_lines.append(LineString(midpoint_to_road))          

# Now write out our result to a new geopackage!                        
meta["schema"]["geometry"] = "LineString"
meta["schema"]["properties"] = {"id": "int"}

if os.path.exists("faces.gpkg"):
    os.remove("faces.gpkg")
            
with fiona.open("faces.gpkg", "w", **meta) as faces:
    i = 0
    for face_line in face_lines:
        faces.write({
            "geometry": mapping(face_line),
            "properties": {"id": i}
        })
        i += 1
        
    
                    
