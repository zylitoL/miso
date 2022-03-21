from functools import reduce

import pandas as pd

from utils import abbreviations, states

FIELD_NAMES = ['Gasoline Price', 'Median Income', 'Population', 'Renewable Energy Use', 'Total Energy Use',
               'Transportation Energy Use']
DIRECTORIES = ['raw', 'interim', 'interim', 'raw', 'raw', 'raw']
FILE_NAMES = ['gasoline_price.csv', 'income.csv', 'populations.csv', 'renewable_energy_use.csv', 'total_energy_use.csv',
              'transportation_energy_use.csv']


def main(raw_filepath, interim_filepath, output_filepath):
    prefix = {'raw': raw_filepath, 'interim': interim_filepath}

    dfs = []
    for field_name, directory, file_name in zip(FIELD_NAMES, DIRECTORIES, FILE_NAMES):
        df = pd.read_csv(f'{prefix[directory]}/{file_name}')
        df = df[df['State'] != 'US']
        df['State'] = df['State'].apply(lambda x: x if x in states else abbreviations[x])
        df = df.melt(id_vars=['State'], var_name='Year', value_name=field_name)
        dfs.append(df)

    socioeconomic_df = reduce(lambda x, y: pd.merge(x, y, on=['State', 'Year']), dfs)
    socioeconomic_df = socioeconomic_df.set_index(['State', 'Year'])
    socioeconomic_df.to_csv(f'{output_filepath}/socioeconomic.csv')


if __name__ == '__main__':
    main('../../data/raw', '../../data/interim', '../../data/processed')
