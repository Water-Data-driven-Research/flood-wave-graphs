import pandas as pd


class StatCalculator:
    """
    This class calculates statistics of aggregated data.
    """
    @staticmethod
    def get_period_stats(df: pd.DataFrame, statistic: str) -> dict:
        """
        We group data by period and return a dictionary with period statistics.
        :param pd.DataFrame df: data to resample
        :param str statistic: statistic to calculate
        :return dict: period statistics
        """
        try:
            yearly = getattr(df.resample('YE'), statistic)()
            quarterly = getattr(df.resample('QE'), statistic)()
        except AttributeError:
            raise ValueError('Invalid statistic')

        yearly.index = yearly.index.to_period('Y')
        quarterly.index = quarterly.index.to_period('Q')

        return {'yearly': yearly, 'quarterly': quarterly}

    @staticmethod
    def get_flood_wave_count(flood_waves: list) -> dict:
        """
        Calculates the number of flood waves from a given list,
        aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :return dict: keys are time interval sizes, values are the respective data
        """
        wave_dates = [wave[0][1] for wave in flood_waves]

        df = pd.DataFrame({
            'date': pd.to_datetime(wave_dates),
            'flood wave count': 1
        }).set_index('date')

        return StatCalculator.get_period_stats(
            df=df,
            statistic='sum'
        )

    @staticmethod
    def get_propagation_time_stat(flood_waves: list, statistic: str = 'mean') -> dict:
        """
        Calculates selected statistic of wave propagation times from a given list,
        aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :return dict: keys are time interval sizes, values are the respective data
        """
        start_dates, propagation_times = zip(*map(
            lambda wave:
            (pd.to_datetime(wave[0][1]),
             (pd.to_datetime(wave[-1][1]) - pd.to_datetime(wave[0][1])).days),
            flood_waves
        ))

        df = pd.DataFrame({
            'date': start_dates,
            f'{statistic} propagation time': propagation_times
        }).set_index('date')

        return StatCalculator.get_period_stats(
            df=df,
            statistic=statistic
        )
