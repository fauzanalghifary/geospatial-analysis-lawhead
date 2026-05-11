"""Add fields to a shapefile"""

import os
import shutil

import shapefile

source = 'NYC_MUSEUMS_UTM'
target = 'NYC_MUSEUMS_UTM_tmp'

for ext in ('shp', 'shx', 'dbf'):
    path = f'{target}.{ext}'
    if os.path.exists(path):
        os.remove(path)

r = shapefile.Reader(source)
field_names = [field[0] for field in r.fields[1:]]
lat_index = field_names.index('LAT') if 'LAT' in field_names else None
lon_index = field_names.index('LON') if 'LON' in field_names else None

with shapefile.Writer(target, r.shapeType) as w:
    w.fields = list(r.fields)
    if lat_index is None:
        w.field('LAT','F',8,5)
    if lon_index is None:
        w.field('LON','F',8,5)
    for i in range(len(r.shapes())):
        lon, lat = r.shape(i).points[0]
        w.point(lon, lat)
        record = list(r.record(i))
        if lat_index is None:
            record.append(lat)
        else:
            record[lat_index] = lat
        if lon_index is None:
            record.append(lon)
        else:
            record[lon_index] = lon
        w.record(*record)

for ext in ('shp', 'shx', 'dbf'):
    shutil.move(f'{target}.{ext}', f'{source}.{ext}')
