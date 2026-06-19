import pandas as pd


def first(series):
    clean = series.dropna()
    return clean.iloc[0] if not clean.empty else None


def last(series):
    clean = series.dropna()
    return clean.iloc[-1] if not clean.empty else None


def avg(series):
    return series.fillna(0).mean()


def sum_value(series):
    return series.sum()


def min_value(series):
    return series.min()


def max_value(series):
    return series.max()

def window_duration(dataframe):

    start_time = dataframe["Timestamp"].min()

    end_time = dataframe["Timestamp"].max()

    return (
        end_time - start_time
    ).total_seconds()


def window_start(dataframe):

    return dataframe[
        "Timestamp"
    ].min()


def window_end(dataframe):

    return dataframe[
        "Timestamp"
    ].max()