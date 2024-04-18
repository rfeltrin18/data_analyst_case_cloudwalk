import pandas as pd
import re
import json
from geobr import read_municipality


def read_csv(path: str,
             sep: str,
             zfill_cols: list = False,
             leave_only_numbers: str = False) -> pd.DataFrame:
    """
    reads csv data based on a given path and standardizes CNPJ columns or removes non-numeric characters
    """

    df = pd.read_csv(path,
                     sep=sep)

    if zfill_cols is not False:

        for col in zfill_cols:
            if col in df.columns:
                max_len = df[col].astype(str).map(len).max()
                df[col] = df[col].astype(str).str.zfill(max_len)
            else:
                print(f"There is no '{col}' column.")

    elif leave_only_numbers is not False:
        df[leave_only_numbers] = df[leave_only_numbers].str.replace('[^0-9]', '', regex=True)
        df[leave_only_numbers] = pd.to_numeric(df[leave_only_numbers], errors='coerce')

    return df


def write_database_dates(df: pd.DataFrame,
                         date_col: str,
                         months: dict):
    """
    parses a date column and adds a new column with dates in 'YYYYMMD' format
    """

    def convert_date(date_str):
        match = re.search(r'(\d{2}) de (\w+) de (\d{4})', date_str)

        if match:
            day, month, year = match.groups()
            month_number = months.get(month, '00')
            return f"{year}{month_number}{day}"

        return None

    if date_col in df.columns:
        df['formatted_opening_date'] = df[date_col].apply(convert_date)
    else:
        raise ValueError(f"There is no '{date_col}' column.")

    return df


def write_associates_and_branches_cols(df: pd.DataFrame,
                                       json_col: str):
    """
    parses a JSON-like column and extracts the number of associates and branches for a given firm
    """

    if json_col not in df.columns:
        raise ValueError(f"There is no '{json_col}' column.")

    def extract_data(json_string):
        try:
            json_data = json.loads(json_string)
            total_associates = json_data.get('total_associates', 0)
            total_branches = json_data.get('total_branches', "0 branch(es)").split(" ")[0]
            return pd.Series([total_associates, int(total_branches)])
        except json.JSONDecodeError:
            return pd.Series([0, 0])

    df[['total_associates', 'total_branches']] = df[json_col].apply(extract_data)

    return df


def create_geodf(df: pd.DataFrame,
                 city_code_col: str,
                 year: int) -> pd.DataFrame:
    """
    parses the column of city codes and gets geospatial data for each one of them
    """
    unique_city_codes = df[city_code_col].unique().tolist()

    def get_city_data(city_codes):
        cities = []

        for code in city_codes:
            try:
                city_gdf = read_municipality(code_muni=code, year=year)
                cities.append(city_gdf)

            except Exception as e:
                print(f"Unable to get data for city code {code}: {e}")

        return pd.concat(cities, ignore_index=True) if cities else None

    cities_data = get_city_data(unique_city_codes)

    return cities_data
