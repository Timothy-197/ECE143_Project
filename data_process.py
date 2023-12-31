import pandas as pd

class Data_loader:
    def __init__(self, data_dir = './records-2300415/'):
        self._data_dir = data_dir
        self._location_columns = ["Location_ID","Latitude", "Latitude_Dir", "Longitude", "Longitude_Dir", "Site_ID","Island","Subunit","Loc_Name","Loc_Type","GCS","Management","Depth","Loc_status"]
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
        self._bleaching_columns = ['Event_ID', 'Location_ID', "Latitude", "Latitude_Dir", "Longitude", "Longitude_Dir", 'Start_Date', 'Rugosity', 'Entered_Date', 'Benthic_ID', 'Frame', 'Disease_Bleaching', 'Severity']
        self._rugosity_columns = ['Event_ID', 'Location_ID', "Latitude", "Latitude_Dir", "Longitude", "Longitude_Dir", 'Start_Date', 'Rugosity', 'Entered_Date', "Chain_length", "Tape_length"]
        self._location_columns = []
        # rugosity here refers to wehter the df contain such column, disease bleaching is yes or no
        super().__init__(data_dir)
    
    def get_df_time_location_bleaching(self):
        # get time & location vs bleaching
        df_time_loc_bleaching = self._df_Events.merge(self._df_benthic_cover, on='Event_ID', how="inner")
        df_time_loc_bleaching = df_time_loc_bleaching.merge(self._df_Locations, on='Location_ID', how='inner')[self._bleaching_columns]
        df_time_loc_bleaching = df_time_loc_bleaching[df_time_loc_bleaching["Latitude"].notna()]
        return df_time_loc_bleaching
    
    def get_df_time_location_bleaching_severity(self):
        # get time & location vs bleaching with severity
        df = self._df_Events.merge(self._df_benthic_cover, on='Event_ID', how="inner")
        df = df.merge(self._df_Locations, on='Location_ID', how='inner')[self._bleaching_columns]
        df = df[df["Severity"].notna()]
        df = df[df["Latitude"].notna()]
        return df
    
    def get_df_time_loc_rugosity(self):
        df_time_loc_rugosity = self._df_Events.merge(self._df_Rugosity, on='Event_ID', how="inner")
        df_time_loc_rugosity["Heterogeneity"] = df_time_loc_rugosity["Chain_length"] / df_time_loc_rugosity["Tape_length"]
        df_time_loc_rugosity = df_time_loc_rugosity.merge(self._df_Locations, on='Location_ID', how='inner')[self._rugosity_columns]
        df_time_loc_rugosity = df_time_loc_rugosity[df_time_loc_rugosity["Latitude"].notna()]
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
        self._fish_density_taxon_columns = ['Fish_ID', 'Event_ID', 'Taxon_ID', "Taxon_Name", "Type", 'Location_ID', 'Start_Date', 'Entered_Date', 'Number', 'Area']
        self._fish_density_taxon_loc_columns = ['Fish_ID', 'Event_ID', 'Taxon_ID', "Taxon_Name", "Type", 'Location_ID', "Latitude", "Latitude_Dir", "Longitude", "Longitude_Dir", 'Island', 'Subunit', 'Loc_Name', 'Start_Date', 'Entered_Date', 'Number', 'Area', 'Density']
        self._juvenile_surface_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Taxon_ID", "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._juvenile_settlement_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._time_juvenile_size_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._time_juvenile_size_taxon_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", "Taxon_Name", "Type", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
        self._time_juvenile_size_taxon_loc_columns = ["Juv_Colony_ID", "Surface_ID", "Settlement_ID", "Event_ID", "Taxon_ID", "Location_ID", "Latitude", "Latitude_Dir", "Longitude", "Longitude_Dir", 'Island', 'Subunit', 'Loc_Name', "Taxon_Name", "Type", 'Start_Date', 'Entered_Date', "Genus_code", "Ind_Count", "Length_mm", "Width_mm"]
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
        df_time_fish_density_taxon = df_time_fish_density.merge(self._df_Taxons, on='Taxon_ID', how="inner")[self._fish_density_taxon_columns]
        # clean out fish groups with unknown taxon name
        df_time_fish_density_taxon = df_time_fish_density_taxon[df_time_fish_density_taxon["Taxon_Name"].notna()]
        # compute fish density given per group of fish (number per unit area)
        df_time_fish_density_taxon["Density"] = df_time_fish_density_taxon["Number"] / df_time_fish_density_taxon["Area"]
        df_time_fish_density_taxon_loc = df_time_fish_density_taxon.merge(self._df_Locations, on='Location_ID', how="inner")[self._fish_density_taxon_loc_columns]
        df_time_fish_density_taxon_loc = df_time_fish_density_taxon_loc[df_time_fish_density_taxon_loc["Island"].notna()]
        df_time_fish_density_taxon_loc = df_time_fish_density_taxon_loc[df_time_fish_density_taxon_loc["Latitude"].notna()]
        # Possible analysis TODO: Group density by months (either given Taxons or not) or 
        #                         Taxons (given months) using average, and plot the density change 
        #                         trend w.r.t. time/Taxon.
        return df_time_fish_density_taxon_loc
    
    def get_df_time_juvenile_size(self):
        """
        Get dataframe containing event time (in month) and the sizes of the juvenile colonies discovered
        """
        # get juvenile species size variations over time
        df_juvenile_surface = self._df_Juvenile_Colony.merge(self._df_Surfaces, on='Surface_ID', how="inner")[self._juvenile_surface_columns]
        df_juvenile_settlement = df_juvenile_surface.merge(self._df_Settlement, on='Settlement_ID', how="inner")[self._juvenile_settlement_columns]
        df_time_juvenile_size = df_juvenile_settlement.merge(self._df_Events, on='Event_ID', how="inner")[self._time_juvenile_size_columns]
        df_time_juvenile_size_taxon  = df_time_juvenile_size.merge(self._df_Taxons, on='Taxon_ID', how="inner")[self._time_juvenile_size_taxon_columns]
        df_time_juvenile_size_taxon_loc = df_time_juvenile_size_taxon.merge(self._df_Locations, on='Location_ID', how="inner")[self._time_juvenile_size_taxon_loc_columns]
        # clean out juveniles with unknown location information
        df_time_juvenile_size_taxon_loc = df_time_juvenile_size_taxon_loc[df_time_juvenile_size_taxon_loc["Island"].notna()]
        # clean out juveniles with unknown taxon name
        df_time_juvenile_size_taxon_loc = df_time_juvenile_size_taxon_loc[df_time_juvenile_size_taxon_loc["Taxon_Name"].notna()]
        df_time_juvenile_size_taxon_loc = df_time_juvenile_size_taxon_loc[df_time_juvenile_size_taxon_loc["Latitude"].notna()]
        # compute sizes of juvenile individuals
        df_time_juvenile_size_taxon_loc["Size_mm"] = df_time_juvenile_size_taxon_loc["Length_mm"]*df_time_juvenile_size_taxon_loc["Width_mm"]
        # Possible analysis TODO: Group Size by Taxon using average, and measure the species size change 
        #                         across time given a Taxon.
        return df_time_juvenile_size_taxon_loc



if __name__ == "__main__":
    data_loader = Data_loader_coral_reef_health()
    data_loader_biomass = Data_Loader_biomass_density_change()
    print(data_loader.get_df_time_loc_rugosity().columns.values, len(data_loader.get_df_time_loc_rugosity()))
    print(data_loader.get_df_time_location_bleaching().columns.values, len(data_loader.get_df_time_location_bleaching()))
    print(data_loader_biomass.get_df_time_fish_density().columns.values, len(data_loader_biomass.get_df_time_fish_density()))
    print(data_loader_biomass.get_df_time_juvenile_size().columns.values, len(data_loader_biomass.get_df_time_juvenile_size()))
    data_loader.get_df_time_loc_rugosity().to_csv("time_rugosity.csv")
    data_loader.get_df_time_location_bleaching().to_csv("time_bleaching.csv")
    data_loader_biomass.get_df_time_fish_density().to_csv("time_fish_density.csv")
    data_loader_biomass.get_df_time_juvenile_size().to_csv("time_juvenile_size.csv")
    df_ju = data_loader_biomass.get_df_time_juvenile_size().groupby(["Island"])