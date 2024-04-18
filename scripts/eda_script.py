import geopandas as gpd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import Literal


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


def join_dfs(df_1: pd.DataFrame,
             df_2: pd.DataFrame,
             how: Literal["left", "right", "inner", "outer", "cross"],
             left_on: str,
             right_on: str = False) -> pd.DataFrame:
    """
    joins tables which might or might not have the key named the same in both ones
    """

    if right_on is not False:
        df = pd.merge(df_1,
                      df_2,
                      left_on=left_on,
                      right_on=right_on,
                      how=how)

    else:
        df = pd.merge(df_1,
                      df_2,
                      on=left_on,
                      how=how)

    return df


def pivot_data(df: pd.DataFrame,
               index_columns: list[str],
               values_and_operations: dict[str: str]):
    """
    creates a pivot table with certain indexes, values and operations
    """
    pivot_df = pd.pivot_table(df,
                              values=list(values_and_operations.keys()),
                              index=index_columns,
                              aggfunc=values_and_operations)

    return pivot_df


def plot_city_data(gdf: gpd.GeoDataFrame,
                   variable: str) -> tuple[Figure, Axes]:
    """
    creates a map plot for a certain variable
    """

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column=variable, ax=ax, legend=True,
             legend_kwds={'label': f"Values of {variable}",
                          'orientation': "horizontal"})
    plt.close(fig)

    return fig, ax


def plot_correlation_matrix(df: pd.DataFrame,
                            method: Literal["pearson", "spearman", "kendall"]) -> tuple[Figure, Axes]:
    """
    creates a correlation plot for certain variables
    """

    corr = df.corr(method=method)

    fig, ax = plt.subplots(figsize=(10, 8))

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(corr, annot=True, cmap=cmap, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

    ax.set_title(f'Correlation Matrix ({method} method)')

    plt.close(fig)

    return fig, ax


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
