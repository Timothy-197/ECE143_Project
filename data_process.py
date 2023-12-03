import pandas as pd
import plotly.express as px

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
        df_time_loc_bleaching = self._df_Events.merge(self._df_benthic_cover, on='Event_ID', how="inner")[self._bleaching_columns]
        df_time_loc_bleaching = df_time_loc_bleaching.merge(self._df_Locations, on='Location_ID', how='inner')
        df = df_time_loc_bleaching[df_time_loc_bleaching["Severity"].notna()]
        return df
    
    def get_df_time_loc_rugosity(self):
        df_time_loc_rugosity = self._df_Events.merge(self._df_Rugosity, on='Event_ID', how="inner")[self._rugosity_columns]
        df_time_loc_rugosity["Heterogeneity"] = df_time_loc_rugosity["Chain_length"] / df_time_loc_rugosity["Tape_length"]
        df_time_loc_rugosity = df_time_loc_rugosity.merge(self._df_Locations, on='Location_ID', how='inner')
        return df_time_loc_rugosity

class Data_Loader_biomass_density_change(Data_loader):
    """
    This class is dataloader to measure biomass density change and species size change at the coral reef over time
    It focus on two things:
    1. time vs fish density
    2. time vs juvenile colony size
    """
    def __init__(self, data_dir='./records-2300415/'):
        self._df_Fish = super()._df_preprocess(pd.read_csv("{}tbl_Fish.csv".format(data_dir)))
        self._df_Juvenile_Colony = self._df_preprocess_juvenile_colony(pd.read_csv("{}tbl_Juvenile_Colony.csv".format(data_dir)))
        self._df_Settlement = super()._df_preprocess(pd.read_csv("{}tbl_Settlement.csv".format(data_dir)))
        self._df_Surfaces = super()._df_preprocess(pd.read_csv("{}tbl_Surfaces.csv".format(data_dir)))
        self._df_Taxons = super()._df_preprocess(pd.read_csv("{}tlu_Taxon.csv".format(data_dir)))
        self._fish_density_columns = ['Fish_ID', 'Event_ID', 'Taxon_ID', 'Location_ID', 'Start_Date', 'Entered_Date', 'Number', 'Area']
        self._juvenile_surface_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Taxon_ID", "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._juvenile_settlement_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._time_juvenile_size_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._time_juvenile_size_taxon_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", "Taxon_Name", "Type", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        # self._time_juvenile_size_loc_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", "Loc_Name", "Taxon_Name", "Type", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        # self._juvenile_density_columns = ['Event_ID', 'Location_ID', 'Start_Date', 'Rugosity', 'Entered_Date', "Chain_length", "Tape_length"]
        
        super().__init__(data_dir)

    def _df_preprocess_juvenile_colony(self, df_juvenile_colony: pd.DataFrame):
        """
        Pre-process juvenile colony table by elimicating rows with incomplete information
        """
        df_juvenile_colony = super()._df_preprocess(df_juvenile_colony)
        df_juvenile_colony = df_juvenile_colony[df_juvenile_colony["Ind_Count"].notna()]
        return df_juvenile_colony

    def get_df_time_fish_density(self):
        """
        Get dataframe containing event time (in month) and fish groups' density
        """
        # get fish density variations over time
        df_time_fish_density = self._df_Fish.merge(self._df_Events, on='Event_ID', how="inner")[self._fish_density_columns]
        # Compute fish density per group of fish (number per unit area)
        df_time_fish_density["Density"] = df_time_fish_density["Number"] / df_time_fish_density["Area"]
        # Possible analysis TODO: Group density by months (either given Taxons or not) or 
        #                         Taxons (given months) using average, and plot the density change 
        #                         trend w.r.t. time/Taxon.
        return df_time_fish_density
    
    def get_df_time_juvenile_size(self):
        """
        Get dataframe containing event time (in month) and the sizes of the juvenile colonies discovered
        """
        # get juvenile species size variations over time
        df_juvenile_surface = self._df_Juvenile_Colony.merge(self._df_Surfaces, on='Surface_ID', how="inner")[self._juvenile_surface_columns]
        df_juvenile_settlement = df_juvenile_surface.merge(self._df_Settlement, on='Settlement_ID', how="inner")[self._juvenile_settlement_columns]
        df_time_juvenile_size = df_juvenile_settlement.merge(self._df_Events, on='Event_ID', how="inner")[self._time_juvenile_size_columns]
        df_time_juvenile_size_taxon  = df_time_juvenile_size.merge(self._df_Taxons, on='Taxon_ID', how="inner")[self._time_juvenile_size_taxon_columns]
        df_time_juvenile_size_taxon = df_time_juvenile_size_taxon[df_time_juvenile_size_taxon["Taxon_Name"].notna()]
        df_time_juvenile_size_taxon["Size_mm"] = df_time_juvenile_size_taxon["Length_mm"]*df_time_juvenile_size_taxon["Width_mm"]
        # Possible analysis TODO: Group Size by Taxon using average, and measure the species size change 
        #                         across time given a Taxon.
        return df_time_juvenile_size_taxon



if __name__ == "__main__":
    data_loader = Data_loader_coral_reef_health()
    data_loader_biomass = Data_Loader_biomass_density_change()
    df_time_loc_rugosity = data_loader.get_df_time_loc_rugosity()
    df_time_loc_bleaching = data_loader.get_df_time_location_bleaching_severity()
    # df_time_loc_bleaching = df_time_loc_bleaching.drop(axis=0)
    # df_time_loc_bleaching['Loc_Name'] = df_time_loc_bleaching['Loc_Name'].astype(int)
    # loc_data = df_time_loc_bleaching['Loc_Name']
    print(data_loader_biomass.get_df_time_fish_density())
    print(data_loader_biomass.get_df_time_juvenile_size())
    
    import matplotlib.pyplot as plt
    import pandas as pd

    # Assuming df_time_loc_rugosity is your DataFrame
    # Convert Period to numerical representation using the 'ordinal' attribute
    df_time_loc_bleaching['Start_Date_Num'] = df_time_loc_bleaching['Start_Date'].dt.to_timestamp().apply(lambda x: x.toordinal())
    # df_het_10 = df_time_loc_bleaching[df_time_loc_bleaching['Location_ID'] == '{005A1863-5D44-4E62-B251-C5E650E31EAF}']
    df_het_10 = df_time_loc_bleaching
    df_het_10 = df_het_10[df_het_10['Disease_Bleaching'] == 'Yes']
    class_mapping = {'No Coral':0, '0%' : 1, '1-25%': 2, '26-50%': 3, '51-75%': 4, '76-100%': 5}
    df_het_10['sev_numeric'] = df_het_10['Severity'].map(class_mapping) 
    df_het_10['sev_numeric_avg'] = df_het_10['sev_numeric'].rolling(window=3).mean()
    # df_het_10['db_avg'] = df_het_10['Disease_Bleaching'].rolling(window=5).mean()
    # Plot using the numerical representation of 'Entered_Date'
    
    # df_temp = df_het_10[['Entered_Date_Num', 'sev_numeric_avg']].groupby('Entered_Date_Num').median()
    df_temp = df_het_10[['Start_Date_Num', 'Disease_Bleaching']].groupby('Start_Date_Num').count()
    df_temp['db_avg'] = df_temp['Disease_Bleaching'].rolling(window=3).mean()
    plt.scatter(df_temp.index, df_temp['db_avg'])

    # You can customize the plot further if needed
    plt.xlabel('Start Date')
    plt.ylabel('Heterogeneity')
    plt.title('Heterogeneity over Time')

    plt.show()
    
    
    
    