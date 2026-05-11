# View data in geopandas

import geopandas
import matplotlib.pyplot as plt

census = geopandas.read_file("GIS_CensusTract_poly.shp")

print(census.to_json(default=str))

census.plot()

plt.show()
