# Readme

## Problem: 

Measuring the changes over time in coral reef environments (benthos) within the Pacific Island network. 

## Motivation:

Coral reefs are arguably the most fundamental building blocks for ocean environments, mainly due to the fact that they provide food and shelter for underwater organisms. Due to oceanic pollution and overfishing, coral reefs (they are actually living organisms) are dying from malnutrition which negatively affects humans, as it is a source of food, and protection from shoreline erosion. 

Thus, we want to investigate how the coral reefs change over time to look at its overall health through a myriad of factors, i.e. biomass density of fish populations, rugosity, etc.

## Dataset: 

 Pacific Island Network Benthic Marine and Marine Fish Monitoring Dataset 2006 - 2022

https://irma.nps.gov/DataStore/Reference/Profile/2300415 

The following dataset contains many csv files that contain data on four coral reef parks in the pacific island. Each csv contains unique data on a specific coral reef, such as one about fish data, taxonomic information, rugosity (coral reef structure), some general logistical CSVs on record keeping, as well as unique IDs across all tables for mapping purposes.

Note that the files are too large for GitHub, you'd better to keep the datasets locally.

### Dataset contents
Below is a list of the meanings of different dataset:
* `tbl_Benthic_Cover.csv`: Information about the photo frames surveyed and if there was disease or bleaching detected.
* `tbl_Events/csv`: Sampling events data, including the date the survey was conducted, and rugosity.
* `tbl_Fish.csv`: Information about fish seen along transect. Species are recorded by number seen per size category.
* `tbl_Juvenile_Colony.csv`: Contains data on genus identification per plate surface.
* `tbl_Locations.csv`: Sampling unit locations which are transects, both fixed and temporary.
* `tbl_Points.csv`: Benthic data for each point that was identified within each frame in the software PhotoGrid.
* `tbl_Proof.csv`: Contains information on which records have been proofed, corrected and certified.
* `tbl_Proof_Tracking.csv`: Contains data on benthic records that were proofed for certification, including the percent error.
* `tbl_Revision_Log.csv`: Database revision history data.
* `tbl_Rugosity.csv`: Stores rugosity measurement.
* `tbl_Settlement.csv`: Contains data about coral recruitment- mainly on plate and posts being retrieved and deployed.
* `tbl_Sites`: Location aggregations, park units in this case. 
* `tbl_Surfaces.csv`: Stores which surfaces were being analyzed per plate pair.
* `tlu_Contacts.csv`: Contact data for project-related personnel
* `tlu_Taxon.csv`: Contains information for all taxon that may be detected during monitoring.
* `xref_Event_Contacts.csv`: Cross-reference table between events and contacts.


## Solution: 

Specifically, we want to look at the changes in composition in the coral reef benthos. This involves data visualization of rugosity( coral reef structures) throughout the time that this data has been recorded. We also want to observe the change in size for fish species across time, as well as the introduction/removal of fish species in the area to find indications of possible disruptive events in the ecosystem, since the data on fish can be a reflection on the health of the coral reef itself. We can apply statistical methods including but not limited to line charts and histograms to do this.

  Using this data, we can evaluate the overall health in the coral reef benthos. To do this, we will measure the aforementioned relative biomass/density/species shift of all fish in the environment, and the rugosity (coral reef structure). We will combine them with methods including but not limited to weighted sum or exponential weighted average to draw conclusions. 
