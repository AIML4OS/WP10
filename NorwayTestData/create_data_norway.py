# This file contains python code to collect and process Norwegian data to use in testing text classification methods.
# It collects information from the BRreg API on legal business units.

# If not already installed install Staistics Norway package for collecting classification names from API
# ! pip install ssb-klass-python

import csv
from datetime import datetime, date
import gzip
from klass import get_classification 
import os
import pandas as pd
import requests
import s3fs
from sklearn.model_selection import train_test_split

def download_csv_format(file_name: str, path: str = f'{os.environ["WORKSPACE_DIR"]}/temp') -> None|str:
    """
    Downloads a compressed CSV file from the Brønnøysund Register Centre's API and saves it locally.

    The function retrieves the dataset of registered entities in Norway from the official API,
    saves it as a `.csv.gz` file in the specified directory, and estimates the number of entities
    by counting the lines in the decompressed file.

    Parameters:
    ----------
    file_name : str
        The name to use for the saved CSV file (without extension).
    path : str, optional
        The directory where the file should be saved. Defaults to "temp".

    Returns:
    -------
    str or None
        The full path to the saved file if successful, or None if the download fails.

    Notes:
    -----
    - The function creates the target directory if it does not exist.
    - The download uses a custom User-Agent and a 5-minute timeout.
    - The file is saved in compressed `.gz` format and decompressed for line counting.
    """
    print(f"Downloading dataset in CSV format to {path} folder...")
    
    os.makedirs(path, exist_ok=True)
        
    csv_url = "https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv"

    try:
        headers = {
            'User-Agent': 'Python-CSV-Download/1.0'
        }

        response = requests.get(csv_url, headers=headers, stream=True, timeout=300)
        response.raise_for_status()

        # Save compressed file
        file_path = f"{path}/{file_name}.csv.gz"

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Compressed CSV file saved as: {file_path}")

        # Decompress and count lines
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            line_count = sum(1 for line in f) - 1  # Subtract header

        print(f"Estimated entities in CSV: {line_count:,}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading CSV: {e}")
        return None

def process_csv(csv_filename: str, min_nace_count: int = 0) -> pd.DataFrame:
    """
    Read and organise csv file of companies
    """

    df = pd.read_csv(csv_filename, compression='gzip', low_memory=False, dtype = "object")

    # Take out those that have closed down
    mask_not_konkurs = df.konkurs == "false"
    df = df.loc[mask_not_konkurs,:].copy()

    # Select only those in enterprise register
    mask_in_reg = df.registrertIForetaksregisteret == "true"
    df = df.loc[mask_in_reg,:].copy()

    # Select only those with a valid nace
    mask_nace = df["naeringskode1.kode"].notna()
    df = df.loc[mask_nace,:].copy()

    # Change to 4-digit European Nace
    df["naeringskode1.kode"] = df["naeringskode1.kode"].str.slice(stop=-1)

    # Filter out too small nace groups - default is no filtering
    tab = df.groupby("naeringskode1.kode").organisasjonsnummer.count()
    small_nace = tab[(tab < min_nace_count)].index.to_list()
    print(f'Number of small Nace gorups removed: {len(small_nace)}')
    mask = df["naeringskode1.kode"].isin(small_nace)
    print(f'Number of units removed due to small Nace groups: {mask.sum()}')
    df = df.loc[~mask,: ]

    # Rename variables
    rename_dict = {
        "navn":"company_name",
        "maalform":"language",
        "organisasjonsnummer":"orgnr",
        "organisasjonsform.kode":"orgform",
        'naeringskode1.kode':"nace_21_code",
        'naeringskode1.beskrivelse':"nace_21_name_nb",
        'hjemmeside':"website",
        'stiftelsesdato':'date_of_incorporation',
        'antallAnsatte':"number_of_employees",
        'institusjonellSektorkode.kode':"sector_code",
        'institusjonellSektorkode.beskrivelse':"sector_name_nb",
        "aktivitet":"company_activity",
        'vedtektsfestetFormaal':"company_purpose",
        }
    df.rename(rename_dict, axis=1, inplace=True)

    # Change variable types
    df["number_of_employees"]=df.number_of_employees.astype("Int64")
    
    # Add standard names
    df["nace_21_name_en"] = get_name(df.nace_21_code, 6, 4)
    df["sector_name_en"] = get_name(df.sector_code, 39, 3)
    df["orgform_name_en"] = get_name(df.orgform, 35, 1)
    df["orgform_name_nb"] = get_name(df.orgform, 35, 1, language = "nb")

    # Order columns
    column_order = ["orgnr", "company_name", "company_activity", "company_purpose", "language",
                    "number_of_employees", "orgform", "orgform_name_nb", "orgform_name_en", "date_of_incorporation", "website",
                    "sector_code", "sector_name_nb", "sector_name_en",
                    "nace_21_code", "nace_21_name_nb", "nace_21_name_en"
                    ]

    return df[column_order]


def get_name(series: pd.Series, klass_nr: int, level: int, language: str = "en", date_str: str = date.today().strftime("%Y-%m-%d")):
    """
    Maps a pandas Series of classification codes to their textual names from a specified classification.

    Parameters:
    ----------
    series : pandas.Series
        A Series containing classification codes to be described.
    klass_nr : str or int
        The classification number used to fetch metadata from the classification system.
    level : int
        The hierarchical level of the classification to select names from.
    language : str, optional
        Language code for the names (default is "en" for English).
    date_str : str, optional
        The reference date for the classification version in "YYYY-MM-DD" format (default is today).

    Returns:
    -------
    pandas.Series
        A Series with the same index as `series`, containing the mapped textual names.
    """
    class_obj = get_classification(klass_nr)
    class_codes = class_obj.get_codes(date_str, language = language, select_level=level)
    series_codes = series.map(class_codes.to_dict())
    return(series_codes)

def train_test_split_single(df, stratify_col, train_size, random_state, min_count):
    """
    Split a DataFrame into train and test sets with approximate stratification,
    while ensuring that classes with very few observations are handled.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to split.
    stratify_col : str
        Column name used for stratification (categorical labels).
    train_size : float
        Desired proportion of the dataset to include in the training set (0 < train_size < 1).
    random_state : int
        Random seed for reproducibility.
    min_count : int
        Minimum number of samples required for a class to be split. Groups with <= min_count 
        are placed in the training data. 

    Returns
    -------
    train : pandas.DataFrame
        Training subset of the original DataFrame.
    test : pandas.DataFrame
        Test subset of the original DataFrame.

    """
    # Check if all small Nace groups are included and add count 1 groups to training.
    # This will result in training data size > train_size but for big data with few small groups ~train_size ok.
    if min_count == 0:
        vc = df[stratify_col].value_counts()
        single_mask = df[stratify_col].map(vc) == 1
        df_rest = df[~single_mask]
        df_single = df[single_mask]

        # Split data and add in small gorups
        train, test = train_test_split(df_rest, stratify = df_rest[stratify_col], train_size = train_size, random_state = random_state)
        train = pd.concat([df_single, train], axis=0)
    else:
        train, test = train_test_split(df, stratify = df[stratify_col], train_size = train_size, random_state = random_state)
    
    # Resex index
    train = train.reset_index(drop=True)
    test  = test.reset_index(drop=True)

    return train, test


if __name__ == "__main__":
    # Download the whole data as a csv first. This is to avoid the 10000 API query limit
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"brreg_entities_{timestamp}"
    csv_filename = download_csv_format(filename)

    # Process data
    min_count = 0
    df_clean = process_csv(csv_filename, min_nace_count = min_count)

    # Create test,train split
    train, test = train_test_split_single(df_clean, stratify_col = "nace_21_code", 
                                          train_size = 0.8, random_state = 42, min_count = min_count)
    
    print(f'Number of units in train data: {train.shape[0]}')
    print(f'Number of units in test data: {test.shape[0]}')
    print(f'Number of Nace groups in test data: {len(test.groupby("nace_21_code").count())}')
    print(f'Number of Nace groups in train data: {len(train.groupby("nace_21_code").count())}')

    # Save data to WP10 bucket
    filename_test = f"s3://projet-aiml4os-wp10/NorwayData/test_norwaydata_{timestamp[:10]}.parquet"
    filename_train = f"s3://projet-aiml4os-wp10/NorwayData/train_norwaydata_{timestamp[:10]}.parquet"
    test.to_parquet(filename_test) 
    train.to_parquet(filename_train)
