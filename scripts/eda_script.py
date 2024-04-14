import matplotlib.pyplot as plt
import geopandas as gpd


def plot_city_data(gdf, variable):
    """
    Plots the geospatial data with a specified variable for each city.

    Parameters:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing city data with geometries.
        variable (str): The name of the column in gdf to visualize.
    """
    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column=variable, ax=ax, legend=True,
             legend_kwds={'label': f"Values of {variable}",
                          'orientation': "horizontal"})
    plt.show()


plot_city_data(gdf, 'code_muni')