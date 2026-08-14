import networkx as nx
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
        :return dict: keys are frequencies, values are the respective data
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
        :return dict: keys are frequencies, values are the respective data
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
    def get_edge_level_stat(start_dates: list, edge_info: str,
                            stat_data: list, statistic: str = 'mean',
                            is_aggregated: bool = True) -> dict:
        """
        Calculates selected statistic of the selected edge level information
        from a given list, aggregated yearly and quarterly.
        :param list start_dates: ...
        :param str edge_info: edge info to calculate
        :param list stat_data: ...
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :param bool is_aggregated: whether to aggregate by the statistic
        :return dict: keys are frequencies, values are the respective data
        """
        df = pd.DataFrame({
            'date': start_dates,
            f'{statistic} {edge_info}': stat_data
        }).set_index('date')

        if is_aggregated:
            return StatCalculator.get_period_stats(
                df=df,
                statistic=statistic
            )
        else:
            return {"total": df}

    @staticmethod
    def get_propagation_time_stat(flood_waves: list, statistic: str = 'mean',
                                  is_aggregated: bool = True) -> dict:
        """
        Calculates selected statistic of wave propagation times from a given list,
        aggregated yearly and quarterly.
        :param list flood_waves: list of flood waves to analyze
        :param str statistic: the statistic to calculate (mean, median, etc.)
        :param bool is_aggregated: whether to aggregate by the statistic
        :return dict: keys are frequencies, values are the respective data
        """
        start_dates, flood_wave_data = zip(*map(
            lambda wave:
                (pd.to_datetime(wave[0][1]),
                 (pd.to_datetime(wave[-1][1]) - pd.to_datetime(wave[0][1])).days),
            flood_waves
        ))

        return StatCalculator.get_edge_level_stat(
            start_dates=start_dates,
            edge_info='propagation time',
            stat_data=flood_wave_data,
            statistic=statistic,
            is_aggregated=is_aggregated)

    @staticmethod
    def get_slope_stat(fwg: nx.DiGraph,
                       statistic: str = 'mean',
                       is_aggregated: bool = True) -> dict:
        """
        ...
        """
        start_dates, slope_data = zip(*map(
            lambda edge_w_data:
            (pd.to_datetime(edge_w_data[0][1]),
             edge_w_data[2].get("slope")),
            fwg.edges(data=True)
        ))

        return StatCalculator.get_edge_level_stat(
            start_dates=start_dates,
            edge_info='slope',
            stat_data=slope_data,
            statistic=statistic,
            is_aggregated=is_aggregated)
