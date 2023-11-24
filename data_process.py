import pandas as pd

class Data_loader:
    def __init__(self, data_dir = './records-2300415/'):
        self._data_dir = data_dir
        self._location_columns = ["Location_ID","Site_ID","Island","Subunit","Loc_Name","Loc_Type","GCS","Management","Depth","Loc_status"]
        self._df_Locations = self._df_preprocess(pd.read_csv("{}tbl_Locations.csv".format(data_dir)))[self._location_columns]
        self._df_Events = self._df_preprocess(pd.read_csv("{}tbl_Events.csv".format(data_dir)))

    def _df_ID_formatting(self, df:pd.DataFrame):
        """
        format the IDs in the dataframe into the same type format
        """
        for col_name in [name for name in df.columns.values.tolist() if "ID" in name]:
            df[col_name] = df[col_name].astype(str)
        return df

    def _df_date_formatting(self, df:pd.DataFrame, period='M', date_names=None):
        """
        The function converts the date columns in specific dataframe to period format
        eg: Period('2018-3', 'M') # the period in months
        
        Inputs:
        df (pd.Dataframe): the dataframe to be processed
        period (str): the period of time, 'Y': year, 'M': month, 'D': day
        date_names (list): the names of the date list to be changed, if not specified, change
        all the date columns
        Ouput:
        (pd.Dataframe) the update dataframe
        """
        if date_names is None:
            for col_name in [name for name in df.columns.values.tolist() if "Date" in name]:
                df[col_name] = pd.to_datetime(df[col_name])
                df[col_name] = df[col_name].dt.to_period(period)
            return df
        else:
            for col_name in date_names:
                df[col_name] = pd.to_datetime(df[col_name])
                df[col_name] = df[col_name].dt.to_period(period)
            return df

    def _df_preprocess(self, df:pd.DataFrame, period='M'):
        """
        preprocess the dataframes to format its types
        """
        df = self._df_ID_formatting(df)
        df = self._df_date_formatting(df, period=period)
        return df

class Data_loader_coral_reef_health(Data_loader):
    """
    This class is dataloader to investigate the coral reef health
    It focus on two things:
    1. time location vs bleaching
    2. time location vs rugosity (heterogeneity)
    """
    def __init__(self, data_dir='./records-2300415/'):
        self._df_benthic_cover = super()._df_preprocess(pd.read_csv("{}tbl_Benthic_Cover.csv".format(data_dir)))
        self._df_Rugosity = super()._df_preprocess(pd.read_csv("{}tbl_Rugosity.csv".format(data_dir)))
        self._bleaching_columns = ['Event_ID', 'Location_ID', 'Start_Date', 'Rugosity', 'Entered_Date', 'Benthic_ID', 'Frame', 'Disease_Bleaching', 'Severity']
        self._rugosity_columns = ['Event_ID', 'Location_ID', 'Start_Date', 'Rugosity', 'Entered_Date', "Chain_length", "Tape_length"]
        self._location_columns = []
        # rugosity here refers to wehter the df contain such column, disease bleaching is yes or no
        super().__init__(data_dir)
    
    def get_df_time_location_bleaching(self):
        # get time & location vs bleaching
        df_time_loc_bleaching = self._df_Events.merge(self._df_benthic_cover, on='Event_ID', how="inner")[self._bleaching_columns]
        df_time_loc_bleaching = df_time_loc_bleaching.merge(self._df_Locations, on='Location_ID', how='inner')
        return df_time_loc_bleaching
    
    def get_df_time_location_bleaching_severity(self):
        # get time & location vs bleaching with severity
        df = self._df_Events.merge(self._df_benthic_cover, on='Event_ID', how="inner")[self._bleaching_columns]
        df = df[df["Severity"].notna()]
        return df
    
    def get_df_time_loc_rugosity(self):
        df_time_loc_rugosity = self._df_Events.merge(self._df_Rugosity, on='Event_ID', how="inner")[self._rugosity_columns]
        df_time_loc_rugosity["Heterogeneity"] = df_time_loc_rugosity["Chain_length"] / df_time_loc_rugosity["Tape_length"]
        df_time_loc_rugosity = df_time_loc_rugosity.merge(self._df_Locations, on='Location_ID', how='inner')
        return df_time_loc_rugosity

if __name__ == "__main__":
    data_loader = Data_loader_coral_reef_health()
    print(data_loader.get_df_time_loc_rugosity())