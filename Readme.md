# Readme

## Problem: 

Measuring the changes over time in coral reef environments (benthos) within the Pacific Island network. 

## Motivation:

Coral reefs are arguably the most fundamental building blocks for ocean environments, mainly due to the fact that they provide food and shelter for underwater organisms. Due to oceanic pollution and overfishing, coral reefs (they are actually living organisms) are dying from malnutrition which negatively affects humans, as it is a source of food, and protection from shoreline erosion. 

Thus, we want to investigate how the coral reefs change over time to look at its overall health through a myriad of factors, i.e. biomass density of fish populations, rugosity, etc.

## Questions:

1. health of the coral reef: bleaching, rugosity

   rugosity: https://www.researchgate.net/figure/The-tape-chain-rugosity-measurement-is-an-in-situ-method-of-evaluating-terrain_fig4_323932975

   datasets to use:

   > *tbl_benthic_cover*: belaching, disease
   >
   > *tbl_locations*: the locations of the sampling units
   >
   > *tbl_rugosity*: the rugosity of the reef

   tables to be generated

   >time, location vs rugosity
   >
   >time, location vs bleaching

2. Coral reef health conditions: Biomass density of fish, and juvenile colony size variations

    Datasets to use:
    > *tbl_Fish*: Fish density (fish count and area) found at every event.
    >
    > *tbl_Juvenile_Colony*: Juvenile colony density (juvenile individual count and size) found at every event.
    >
    > *tbl_Surface*: Surfaces discovered at every event. Used for linking juvenile colony and surface.  
    >
    > *tbl_Settlement*: Settlements discovered at every event. Used for linking surface and settlement.
    >
    > *tbl_Event*: Discovery events through time. Used for linking settlement and event (hence linking juvenile colony and event), and linking fish and event.

    Tables to generate:
    > time vs fish density 
    >
    > time vs juvenile colony size

## Dataset: 

 Pacific Island Network Benthic Marine and Marine Fish Monitoring Dataset 2006 - 2022

https://irma.nps.gov/DataStore/Reference/Profile/2300415 

The following dataset contains many csv files that contain data on four coral reef parks in the pacific island. Each csv contains unique data on a specific coral reef, such as one about fish data, taxonomic information, rugosity (coral reef structure), some general logistical CSVs on record keeping, as well as unique IDs across all tables for mapping purposes.

Note that the files are too large for GitHub, you'd better to keep the datasets locally.

### Dataset contents
Below is a list of the meanings of different dataset:
* `tbl_Benthic_Cover.csv`: Information about the photo frames surveyed and if there was disease or bleaching detected. This is mainly about bleaching

  ```
  "Benthic_ID","Event_ID","Frame","Analy_Date","FramdIder","TotalPoint","Disease_Bleaching","Severity","Benthic_Certified","Benthic_Certified_by","Benthic_Certified_Date"
  ```

* `tbl_Events.csv`: Sampling events data, including the date the survey was conducted, and rugosity.

  ```
  Event_ID,Location_ID,Protocol_Name,Start_Date,Notes,Rugosity,Entered_by,Entered_Date,Updated_Date,Fish_Certified,Fish_Certified_by,Fish_Certified_Date,QA_notes
  ```

* `tbl_Fish.csv`: Information about fish seen along transect. Species are recorded by number seen per size category.

  ```
  "Fish_ID","Event_ID","Taxon_ID","Number","Min","Max","AvgLgth","Area","Comments"
  ```

* `tbl_Juvenile_Colony.csv`: Contains data on genus identification per plate surface.

  ```
  "Juv_Colony_ID","Surface_ID","Taxon_ID","Genus_code","Ind_Count","Length_mm","Width_mm"
  ```

* `tbl_Locations.csv`: Sampling unit locations which are transects, both fixed and temporary.

  ```
  "Location_ID","Site_ID","Island","Subunit","Loc_Name","Loc_Type","Latitude","Latitude_Dir","Longitude","Longitude_Dir","GCS","Management","Habitat","Compass_bearing","Depth","Cut_Distance","Harbor_Distance","Loc_Notes","Loc_status","Loc_year_established","Loc_Created_Date","Loc_Updated_Date","Loc_Updated_by"
  ```

* `tbl_Points.csv`: Benthic data for each point that was identified within each frame in the software PhotoGrid.

  ```
  "Benthic_ID","Taxon_ID","Point","X","Y","Bleaching","Bleaching_Cat"
  ```

* `tbl_Proof.csv`: Contains information on which records have been proofed, corrected and certified.

  ```
  "Start_Date","Event_ID","Unit_Code","Data_Type","Location_ID","Loc_Name","Loc_Type","Proof_Count","Proofed","Corrected","Certified","Proof_Date","Proof_Reader","Comments"
  ```

* `tbl_Proof_Tracking.csv`: Contains data on benthic records that were proofed for certification, including the percent error.

  ```
  "Event_ID","Location_ID","Points_Reviewed","Points_Corrected","Percent_Error","Proof_Date","Proof_Reader"
  ```

* `tbl_Revision_Log.csv`: Database revision history data.

  ```
  Revision_ID,Revision_Date,Revision_Description,Revision_Comments,Revision_By,Ceritified_Data_Update
  ```

* `tbl_Rugosity.csv`: Stores rugosity measurement.

  ```
  "Event_ID","Chain_length","Tape_length"
  ```

* `tbl_Settlement.csv`: Contains data about coral recruitment- mainly on plate and posts being retrieved and deployed.

  ```
  "Settlement_ID","Event_ID","CRA","Plate_number","Retrieved_Plate_Pair","Duration","Sett_Certified","Sett_Certified_by","Sett_Certified_date"
  ```

* `tbl_Sites`: Location aggregations, park units in this case. 

  ```
  "Site_ID","Unit_Code","Site_Name","Site_Area"
  ```

* `tbl_Surfaces.csv`: Stores which surfaces were being analyzed per plate pair.

  ```
  "Surface_ID","Settlement_ID","Surface","Orientation"
  ```

* `tlu_Contacts.csv`: Contact data for project-related personnel

  ```
  "Contact_ID","Last_Name","First_Name","Middle_Init","Obsr_Code","Organization","Position_Title","Address_Type","Address","Address2","City","State_Code","Zip_Code","Country","Email","Work_Phone","Work_Extension","Contact_Notes","Active"
  ```

* `tlu_Taxon.csv`: Contains information for all taxon that may be detected during monitoring.

  ```
  Taxon_ID,AphiaID,Status,Type,Settlement,Kingdom,Phylum,Class,Order,Family,Genus,Species,Taxon_Name,Synonym,Species_Code,Authority,Reference,Target_Species,Hawaiian_Name,Common_Name,Trophic,Consumer,Endemic,Mobility,a_Variable,b_Variable,Reference_ab_Variable,Congener,TL_TO_SL_FL,Reference_TL_TO_SL_FL,ESA_Status,Comments,Update_Date,Update_By
  ```

* `xref_Event_Contacts.csv`: Cross-reference table between events and contacts.

  ```
  Event_ID,Contact_ID,Contact_Role
  ```

  


## Solution: 

Specifically, we want to look at the changes in composition in the coral reef benthos. This involves data visualization of rugosity( coral reef structures) throughout the time that this data has been recorded. We also want to observe the change in size for fish species across time, as well as the introduction/removal of fish species in the area to find indications of possible disruptive events in the ecosystem, since the data on fish can be a reflection on the health of the coral reef itself. We can apply statistical methods including but not limited to line charts and histograms to do this.

  Using this data, we can evaluate the overall health in the coral reef benthos. To do this, we will measure the aforementioned relative biomass/density/species shift of all fish in the environment, and the rugosity (coral reef structure). We will combine them with methods including but not limited to weighted sum or exponential weighted average to draw conclusions. 

### Step 0: Download dataset

You need to first download the dataset to get everything work. Since the dataset is too large for a github repository, you should download it yourself and put the file in the root directory.

### Step 1: Data Cleaning

In this step, we organize the data into several pandas dataframes. Each set of dataframes corresponds to a QUESTION we are study.

#### Question 1: Change over the coral reef health

You need dataframes containing the following information:

1. time & location vs coral reef rugosity (heterogeneity)
2. time & location vs coral reef bleaching 

To use the dataframes, you need to use the class `Data_loader_coral_reef_health`

```python
# get dataframe of time & location vs coral reef rugosity (heterogeneity):
data_loader = Data_loader_coral_reef_health()
df_heterogeneity = data_loader.get_df_time_loc_rugosity()
```

```python
# get dataframe of 1. time & location vs coral reef bleaching 
data_loader = Data_loader_coral_reef_health()
df_bleaching = data_loader.get_df_time_location_bleaching()
# if you want to investigate the bleaching with severity, you can:
df_bleaching_severity = data_loader.get_df_time_location_bleaching_severity()
```

#### Question 2: Change of the coral reef biological conditions 

Dataframes necessary for analysis include the following information:

1. time vs fish density
2. time vs juvenile colony size

You can use `Data_Loader_biomass_density_change` for loading the cleaned and merged biomass density and juvenile colony size datasets.


```python
# get general density/size data loader
data_loader_biomass = Data_Loader_biomass_density_change()
# get time vs fish density data
data_fish_density = data_loader_biomass.get_df_time_fish_density()
```

```python
# get general density/size data loader
data_loader_biomass = Data_Loader_biomass_density_change()
# get time vs juvenile size data
data_juvenile_size = data_loader_biomass.get_df_time_juvenile_size()
```

## Running: 

Run using the following command to view the cleaned data:

```python
python data_process.py
```

Place the required .csv files (indicated in the **Questions** section) under the *records-2300415* directory. Then you can run successfully.
