# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import preprocess_income
import preprocess_populations
import preprocess_model_sales
import preprocess_state_sales

import generate_socioeconomic


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('interim_filepath', type=click.Path())
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, interim_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into cleaned data ready to be analyzed
        (saved in ../processed). Intermediary datasets are saved in (../interim).
    """
    logger = logging.getLogger(__name__)

    logger.info('Preprocessing data')
    preprocess_args = (input_filepath, interim_filepath)

    preprocessors = [preprocess_income, preprocess_model_sales, preprocess_populations, preprocess_state_sales]
    for preprocessor in preprocessors:
        preprocessor.main(*preprocess_args)

    logger.info('Generating socioeconomic data')
    generate_socioeconomic.main(input_filepath, interim_filepath, output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
