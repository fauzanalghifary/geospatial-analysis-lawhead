"""Convert a shapefile from lat/lon to UTM"""
import shapefile
import utm
r = shapefile.Reader("NYC_MUSEUMS_GEO")
with shapefile.Writer("NYC_MUSEUMS_UTM", shapeType=1) as w:
    w.fields = list(r.fields)
    for rec in r.records():
        w.record(*list(rec))
    for s in r.iterShapes():
        lon, lat = s.points[0]
        y, x, zone, band = utm.from_latlon(lat, lon)
        w.point(x, y)

# Add a prj file for EPSG:26918 / NAD 1983 UTM Zone 18N.
prj = (
    'PROJCS["NAD_1983_UTM_Zone_18N",'
    'GEOGCS["GCS_North_American_1983",'
    'DATUM["D_North_American_1983",'
    'SPHEROID["GRS_1980",6378137.0,298.257222101]],'
    'PRIMEM["Greenwich",0.0],'
    'UNIT["Degree",0.0174532925199433]],'
    'PROJECTION["Transverse_Mercator"],'
    'PARAMETER["False_Easting",500000.0],'
    'PARAMETER["False_Northing",0.0],'
    'PARAMETER["Central_Meridian",-75.0],'
    'PARAMETER["Scale_Factor",0.9996],'
    'PARAMETER["Latitude_Of_Origin",0.0],'
    'UNIT["Meter",1.0]]'
)
with open('NYC_MUSEUMS_UTM.prj', 'w') as f:
    f.write(prj)
