import os
from pathlib import Path
import json
import pandas as pd


def get_path():
    cwd = Path(__file__).parents[1]
    return str(cwd)

def read_json(filename):
    cwd = get_path()
    foldername = 'data'
    with open(f'{cwd}/{foldername}/{filename}.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    cwd = get_path()
    foldername = 'data'
    with open(f'{cwd}/{foldername}/{filename}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
def is_json(filename):
    cwd = get_path()
    foldername = 'data'
    return os.path.isfile(f'{cwd}/{foldername}/{filename}.json')

def df_from_json(filename, orient="table"):
    cwd = get_path()
    foldername = 'data'
    df = pd.read_json(f'{cwd}/{foldername}/{filename}.json', orient=orient)
    return df

def df_to_json(df, filename, orient="table"):
    cwd = get_path()
    foldername = 'data'
    df.to_json(f'{cwd}/{foldername}/{filename}.json', orient=orient, indent=4)


if __name__ == "__main__":
    pass
