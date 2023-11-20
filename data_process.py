import pandas as pd
data_dir = "./records-2300415/"


if __name__ == "__main__":
    # get data for the problem is coral reef health
    df_benthic_cover = pd.read_csv("{}tbl_Benthic_Cover.csv".format(data_dir))
    df_benthic_cover['Event_ID'] = df_benthic_cover['Event_ID'].astype(str)
    df_Rugosity = pd.read_csv("{}tbl_Rugosity.csv".format(data_dir))
    df_Rugosity['Event_ID'] = df_Rugosity['Event_ID'].astype(str)
    df_Locations = pd.read_csv("{}tbl_Locations.csv".format(data_dir))
    df_Events = pd.read_csv("{}tbl_Events.csv".format(data_dir))
    df_Events['Event_ID'] = df_Events['Event_ID'].astype(str)
    
    df_time_loc_rugosity = df_Events.merge(df_Rugosity, on='Event_ID', how="inner")
    df_time_loc_bleaching = df_Events.merge(df_benthic_cover, on='Event_ID', how="inner")
    