import numpy as np
import pandas as pd


def process_data():

    # added

    # newdata = pd.read_csv(
    #     'data/data.csv',
    #     skiprows=1,
    #     names=['index', 'country', 'year', 'fertility', 'population', 'life_expectancy', 'income'],
    # )

    # Make the column names ints not strings for handling

    # # read data

    # data_df = pd.read_csv('data/data.csv')
    # coun_df = pd.read_csv('data/countries.csv')

    # # regions

    # reg_data = coun_df[['country', 'four_regions', 'eight_regions']]
    # reg_data.columns = ['Country', 'Area', 'Group']
    # reg_df = reg_data.set_index('Country')
    # reg_df.to_csv('reg.csv')

    # # pop

    # pop_data = data_df[['country', 'year', 'population']]
    # pop_df = pop_data.pivot(index='country', columns='year', values='population')
    # pop_df.to_csv('pop_data.csv')

    population = pd.read_csv('pop_data.csv', index_col=0)
    regions = pd.read_csv('reg.csv', index_col=0)

    regions_list = list(regions.Group.unique())

    # Turn population into bubble sizes. Use min_size and factor to tweak.
    scale_factor = 200
    population_size = np.sqrt(population / np.pi) / scale_factor
    min_size = 3
    population_size = population_size.where(population_size >= min_size).fillna(min_size)

    # # x : income

    # income_data = data_df[['country', 'year', 'income']]
    # income_df = income_data.pivot(index='country', columns='year', values='income')
    # # income_df.to_csv('2233.csv')
    # # life_expectancy.to_csv('life_exp.csv')
    # # life_exp_df = pd.read_csv('life_exp.csv', index_col='Country')
    # # income_df = income_df.reindex(columns=life_exp_df.columns)
    # income_df.to_csv('income_data.csv')

    # # y : life

    # life_data = data_df[['country', 'year', 'life_expectancy']]
    # life_df = life_data.pivot(index='country', columns='year', values='life_expectancy')
    # life_df.to_csv('life_data.csv')

    # # test

    # test_df = pd.read_csv('life_data.csv', index_col=0)
    # test_df.to_csv('test.csv')

    # read pre

    income_df = pd.read_csv('income_data.csv', index_col=0)
    life_df = pd.read_csv('life_data.csv', index_col=0)

    population_size.to_csv('size_data.csv')

    years = [int(year) for year in range(1800, 2019)]

    return income_df, life_df, population_size, regions, years, regions_list


process_data()
