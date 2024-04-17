import geopandas as gpd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd


def compare_branches(df: pd.DataFrame,
                     branches_col: str) -> str:
    """
    checks whether the sum of branches from the JSON-like column equals to the number of rows
    """

    branches = ('the column sum', df[branches_col].sum())

    rows = ('number of rows', len(df.index))

    delta = abs(branches[1] - rows[1])

    larger = branches[0] if branches[1] > rows[1] else rows[0]

    if branches == rows:
        verdict = f'They are the same: {rows} branches.'
    else:
        verdict = f'They are not the same: {larger} has {delta} more branches.'

    return verdict


def calculate_branch_ratio(df: pd.DataFrame,
                           cnpj_root_col: str,
                           cnpj_col: str,
                           branches_col: str) -> pd.DataFrame:
    """
    calculates the percentage of branches of a CNPJ root
    """

    root_df = df.groupby(cnpj_root_col).agg({cnpj_col: pd.Series.nunique,
                                             branches_col: 'first'
                                             })

    root_df['branch_ratio'] = (root_df[cnpj_col] / root_df[branches_col]) * 100

    return root_df


def slice_date(df: pd.DataFrame,
               date_col: str) -> pd.DataFrame:
    """
    takes a YYYYMMDD column and extracts the separate date dimensions in columns
    """

    date_dims = {'year': (0, 4),
                 'month': (4, 2),
                 'day': (6, 2)}

    def extract_date_dims(date_str: str,
                          date_dim: str) -> str:
        start, length = date_dims[date_dim][0], date_dims[date_dim][1]

        return date_str[start: start + length]

    for dim in date_dims.keys():
        df[dim] = df[date_col].apply(lambda x: extract_date_dims(x, dim))

    return df


def plot_city_data(gdf: gpd.GeoDataFrame, variable: str) -> tuple[Figure, Axes]:
    """
    Plots the geospatial data with a specified variable for each city and returns the plot objects.

    Parameters:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing city data with geometries.
        variable (str): The name of the column in gdf to visualize.

    Returns:
        tuple[Figure, Axes]: A tuple containing the Figure and Axes objects for the plot.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column=variable, ax=ax, legend=True,
             legend_kwds={'label': f"Values of {variable}",
                          'orientation': "horizontal"})

    return fig, ax
