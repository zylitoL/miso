import pandas as pd


def main(input_filepath, output_filepath):
    df = pd.read_csv(f'{input_filepath}/median_income.csv')
    # Keep only median income columns
    temp_header = df.columns + ' ' + df.iloc[0]
    df.columns = temp_header

    seen = set()
    new_columns = []
    for column in df.columns:
        if 'Standard error' in column:
            continue
        year = column.split(" ")[0]
        if year in seen:
            continue
        else:
            new_columns.append(column)
            seen.add(year)

    df = df[new_columns]

    # Reformat
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.rename({'State State': 'State'}, axis=1)
    df.index = df['State']
    df = df.drop(columns=['State'])
    df.columns = df.columns[::-1]

    df.columns = [col.split(" ")[0] for col in df.columns]
    df = df.applymap(lambda x: int(x.replace(",", "")))

    df.to_csv(f"{output_filepath}/income.csv")


if __name__ == '__main__':
    main('../../data/raw', '../../data/interim')
