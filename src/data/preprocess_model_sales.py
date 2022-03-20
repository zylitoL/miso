import csv

import pandas as pd


def process_model_rows(s):
    # determine left and right "boundaries" of non-sales
    left = -1
    right = len(s)
    for i in range(len(s)):  # normally we would use enumerate, but enumerating in reverse doesn't exist
        x = s[i]
        if x != '-':
            left = i
            break

    for i in range(len(s) - 1, -1, -1):
        x = s[i]
        if x != '-':
            right = i
            break

    # if a '-' entry is between the left and right cutoffs, we assume missing data
    s = [
        float(x.replace(',', '')) if x != '-'
        else (0 if i < left or i > right else None)
        for i, x in enumerate(s)
    ]

    return s


def clean_hev(file_name):
    vehicle_data = []

    with open(file_name, 'r') as fin:
        sale_data = csv.reader(fin)
        *header, _ = next(sale_data)  # skip header row, but keep information, except total

        for row in sale_data:
            vehicle, *data, _ = row  # we need information about the vehicle and the yearly data, and can skip the total
            vehicle_data.append([vehicle, *process_model_rows(data)])

    df = pd.DataFrame(vehicle_data, columns=header)
    df.index = df['Vehicle']
    df['Type'] = 'HEV'
    df = df.drop('Total')
    df = df.drop(columns=['Vehicle'])

    return df


def clean_pev(file_name):
    vehicle_data = []

    with open(file_name, 'r') as fin:
        sale_data = csv.reader(fin)
        *header, _ = next(sale_data)  # skip header row, but keep information, except total

        for row in sale_data:
            vehicle, ev_type, *data, _ = row  # need information about the vehicle and the yearly data only
            vehicle_data.append([vehicle, ev_type, *process_model_rows(data)])

    df = pd.DataFrame(vehicle_data, columns=header)
    df.index = df['Vehicle']
    df = df.drop('Total')
    df = df.drop(columns=['Vehicle'])

    return df


def main(input_filepath, output_filepath):
    hev_df = clean_hev(f'{input_filepath}/hev_sales.csv')
    pev_df = clean_pev(f'{input_filepath}/pev_sales.csv')

    model_df = pd.concat([hev_df, pev_df])
    model_df = model_df[['Type'] + [str(x) for x in range(1999, 2019 + 1)]]

    model_df.to_csv(f'{output_filepath}/model_sales.csv')


if __name__ == '__main__':
    main('../../data/raw', '../../data/interim')
