import pandas as pd

from utils import abbreviations


def clean2019(file_name):
    df2019 = pd.read_csv(file_name)

    df2019 = df2019[:-1]

    df2019.index = df2019['State'].apply(lambda x: abbreviations[x])

    df2019['2019 EVs'] = df2019['EV Registrations 2019'].apply(int)
    df2019['2019 EVPercent'] = df2019['PercentTotalEV 2019'].apply(lambda x: float(x[:-1]) / 100)

    df2019 = df2019.drop(columns=['State', 'EV Registrations 2019', 'PercentTotalEV 2019'])

    return df2019


def clean2021(file_name):
    df2021 = pd.read_csv(file_name)

    df2021 = df2021[:-1]

    df2021.index = df2021['State'].apply(lambda x: abbreviations[x])

    df2021['2021 EVs'] = df2021['EVRegistrations 2021'].apply(lambda x: int(x.replace(',', '')))
    df2021['2021 EVPercent'] = df2021['PercentEVDistribution2021'].apply(lambda x: float(x[:-1]) / 100)

    df2021 = df2021.drop(columns=['State', 'EVRegistrations 2021', 'PercentEVDistribution2021'])

    return df2021


def main(input_filepath, output_filepath):
    df2019 = clean2019(f'{input_filepath}/ev_registrations_2019.csv')
    df2021 = clean2021(f'{input_filepath}/ev_registrations_2021.csv')

    sales = pd.merge(df2019, df2021, on='State')
    sales.to_csv(f'{output_filepath}/state_sales.csv')


if __name__ == '__main__':
    main('../../data/raw', '../../data/interim')
