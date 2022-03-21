import pandas as pd


def main(input_filepath, output_filepath):
    load_df = pd.read_csv(f'{input_filepath}/miso_load.csv')
    load_df['Market Day'] = pd.to_datetime(load_df['Market Day'])
    load_df['Market Day'] += load_df['HourEnding'].astype('timedelta64[h]')
    load_df = load_df.drop(columns=['HourEnding'])

    dfs = []
    regions = load_df['Region'].unique()
    for region in regions:
        df = load_df[load_df['Region'] == region]
        df.index = df['Market Day']
        df = df.resample('1A').sum()
        df['Region'] = region
        dfs.append(df)

    load_df = pd.concat(dfs)
    load_df = load_df.reset_index()
    load_df['Year'] = pd.DatetimeIndex(load_df['Market Day']).year
    load_df = load_df.set_index(['Year', 'Region'])
    load_df = load_df.drop(columns=['Market Day'])
    load_df.head()

    load_df.to_csv(f'{output_filepath}/miso_load.csv')


if __name__ == '__main__':
    main('../../data/raw', '../../data/processed')
