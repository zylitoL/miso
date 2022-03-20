import pandas as pd

from utils import abbreviations


def clean_p1(file_name):
    df1 = pd.read_csv(file_name)
    df1 = df1.drop(df1.index[0])
    df1 = df1.rename({'Area Name': 'State'}, axis=1)
    df1.index = df1['State']
    df1 = df1.drop(columns=['State'])
    df1 = df1.loc[abbreviations.keys()]

    return df1


def clean_p2(file_name):
    df2 = pd.read_csv(file_name)
    df2 = df2.drop(df2.index[0])
    df2 = df2.drop(columns=['Estimates Base (4/1/2010)'])
    df2 = df2.rename({'Area': 'State'}, axis=1)
    df2.index = df2['State']
    df2 = df2.drop(columns=['State'])
    df2 = df2.loc[abbreviations.keys()]

    return df2


def main(input_filepath, output_filepath):
    df1 = clean_p1(f'{input_filepath}/population_p1.csv')
    df2 = clean_p2(f'{input_filepath}/population_p2.csv')

    population = pd.merge(df1, df2, on='State')
    population = population.applymap(lambda x: int(x.replace(",", "")))

    population.to_csv(f'{output_filepath}/populations.csv')


if __name__ == '__main__':
    main('../../data/raw', '../../data/interim')
