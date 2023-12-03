#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:13:41 2023

@author: manavchordia
"""

import data_process as dp
import matplotlib.pyplot as plt 
import statistics as st
import pandas as pd

data_loader = dp.Data_loader_coral_reef_health()

def vis_rugosity(parameter = 'loc'):
    """
    Generates visualisations about rudosity of coral reefs vs time and location
    

    Parameters
    ----------
    parameter : string, optional
        what type of visualisation loc or time

    Returns
    -------
    None.

    """

    df_time_loc_rugosity = data_loader.get_df_time_loc_rugosity()
    
    if parameter == 'loc':
        
        fig, axes = plt.subplots(3, 2, figsize=(10, 10))  # Adjust rows/cols as needed
        
        grouped_loc = df_time_loc_rugosity.groupby("Island")
    
        for i, (island, data) in enumerate(grouped_loc):
            ax = axes.flatten()[i]
            data["Heterogeneity"].plot.hist(ax=ax, label=island)
            ax.set_title(f"Island: {island}")
            ax.set_xlabel("Heterogeneity")
            ax.set_ylabel("Count")
                
        fig.suptitle("Heterogeneity Distribution by Site ID")
        plt.tight_layout()
        plt.show()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

        # Island histogram
        for island in df_time_loc_rugosity['Island'].unique():
            island_data = df_time_loc_rugosity[df_time_loc_rugosity['Island'] == island]['Heterogeneity']
            ax1.hist(island_data, label=island, alpha=0.6)

        # Heterogeneity distribution
        ax2.hist(df_time_loc_rugosity['Heterogeneity'], label='Overall')

        ax1.set_xlabel('Heterogeneity')
        ax1.set_ylabel('Count')
        ax1.set_title('Island-wise Heterogeneity distribution')
        ax2.set_xlabel('Heterogeneity')
        ax2.set_ylabel('Count')
        ax2.set_title('Overall Heterogeneity distribution')

        ax1.legend()
        plt.tight_layout()
        plt.show()
        
    if parameter == 'time':
        df_time_loc_rugosity['Start_Date_Num'] = df_time_loc_rugosity['Start_Date'].dt.to_timestamp()
        
        for i in df_time_loc_rugosity['Island'].unique():
        
            df_time_loc_rugosity_temp = df_time_loc_rugosity[df_time_loc_rugosity['Island'] == i]
            df_temp = df_time_loc_rugosity_temp[['Start_Date_Num', 'Heterogeneity']].groupby('Start_Date_Num').mean()
            df_temp['het_avg'] = df_temp['Heterogeneity'].rolling(window=3).mean()
            plt.plot(df_temp.index, df_temp['het_avg'], label=i)
    
            plt.xlabel('Start Date')
            plt.ylabel('Heterogeneity')
            plt.title('Heterogeneity over Time')

        plt.legend()
        plt.show()
        
def vis_bleach(type = "loc"):
    """
    Generates visualisations about bleaching of coral reefs vs time and location

    Parameters
    ----------
    p
    type : string, optional
        DESCRIPTION. The default is "count".

    Returns
    -------
    df_het_10 : TYPE
        DESCRIPTION.

    """
    
    df_time_loc_bleaching = data_loader.get_df_time_location_bleaching_severity()
    df_time_loc_bleaching['Start_Date_Num'] = df_time_loc_bleaching['Start_Date'].dt.to_timestamp()
    # df_het_10 = df_time_loc_bleaching[df_time_loc_bleaching['Location_ID'] == '{005A1863-5D44-4E62-B251-C5E650E31EAF}']
    df_het_10 = df_time_loc_bleaching
    df_het_10 = df_het_10[df_het_10['Disease_Bleaching'] == 'Yes']
    class_mapping = {'No Coral':0, '0%' : 1, '1-25%': 2, '26-50%': 3, '51-75%': 4, '76-100%': 5}
    df_het_10['sev_numeric'] = df_het_10['Severity'].map(class_mapping) 
    # df_het_10['sev_numeric_avg'] = df_het_10['sev_numeric'].rolling(window=3).mean()
    # df_het_10['db_avg'] = df_het_10['Disease_Bleaching'].rolling(window=5).mean()
    # Plot using the numerical representation of 'Entered_Date'
    
    if type == 'loc':
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # Adjust rows/cols as needed
        
        grouped_loc = df_het_10.groupby("Island")
    
        for i, (island, data) in enumerate(grouped_loc):
            ax = axes.flatten()[i]
            data["sev_numeric"].plot.hist(ax=ax, label=island)
            ax.set_title(f"Island: {island}")
            ax.set_xlabel("Heterogeneity")
            ax.set_ylabel("Count")
                
        fig.suptitle("Heterogeneity Distribution by Site ID")
        plt.tight_layout()
        plt.show()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

        # Island histogram
        for island in df_het_10['Island'].unique():
            island_data = df_het_10[df_het_10['Island'] == island]['sev_numeric']
            ax1.hist(island_data, label=island, alpha=0.6)

        # Heterogeneity distribution
        ax2.hist(df_het_10['sev_numeric'], label='Overall')

        # Set labels and title
        ax1.set_xlabel('Heterogeneity')
        ax1.set_ylabel('Count')
        ax1.set_title('Island-wise Heterogeneity distribution')
        ax2.set_xlabel('Heterogeneity')
        ax2.set_ylabel('Count')
        ax2.set_title('Overall Heterogeneity distribution')

        ax1.legend()
        plt.tight_layout()
        plt.show()
    
    
    if type == 'severity':
        
        df_temp = df_het_10[['Start_Date_Num', 'sev_numeric']].groupby('Start_Date_Num').mean()
        df_temp['sev_avg'] = df_temp['sev_numeric'].rolling(window=4).mean()
    
        plt.scatter(df_temp.index, df_temp['sev_avg'])
    
        # You can customize the plot further if needed
        plt.xlabel('Start Date')
        plt.ylabel('Bleaching Severity')
        plt.title('Avg bleaching severity over time')
        
        plt.show()
    
    if type == 'count':
    # df_temp = df_het_10[['Entered_Date_Num', 'sev_numeric_avg']].groupby('Entered_Date_Num').median()
        df_temp = df_het_10[['Start_Date_Num', 'Disease_Bleaching']].groupby('Start_Date_Num').count()
        df_temp['db_avg'] = df_temp['Disease_Bleaching'].rolling(window=3).mean()
        plt.scatter(df_temp.index, df_temp['db_avg'])
    
        # You can customize the plot further if needed
        plt.xlabel('Start Date')
        plt.ylabel('Count of Disease Bleaching')
        plt.title('Avg bleaching case count over time')

        plt.show()

    return df_temp
        
df = vis_rugosity('loc')
    
    

