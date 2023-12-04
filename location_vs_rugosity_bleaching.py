import data_process as dp
import matplotlib.pyplot as plt 
import statistics as st
import pandas as pd
import folium
import webbrowser
from folium.plugins import MarkerCluster
import base64
from io import BytesIO

data_loader = dp.Data_loader_coral_reef_health()
df_rugosity = data_loader.get_df_time_loc_rugosity()
df_bleaching = data_loader.get_df_time_location_bleaching()


def get_center_point(df):
    """
    Calculates the center point of all islands(To position the visualization of the image at the center and make the entire image more comprehensive.).

    Parameters
    ----------
    df : DataFrame
        The DataFrame containing the latitude and longitude of the islands.

    Returns
    -------
    (float, float)
        The latitude and longitude of the center point.
    """

    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    return center_lat, center_lon

def convert_severity(severity_str):
    """
    Convert the string representation of coral bleaching severity into numerical representation.

    Parameters:
    ----------
    severity_str (str): The string representation of bleaching severity (e.g., '0%', '1-25%').

    Returns:
    -------
    int or None: The corresponding numerical representation. Returns None if the string is not in the predefined mapping.
    """
    class_mapping = {'No Coral': 0, '0%': 1, '1-25%': 2, '26-50%': 3, '51-75%': 4, '76-100%': 5}
    return class_mapping.get(severity_str, None)  # # Returns None if the key is not present in the dictionary.

df_bleaching['Severity_Num'] = df_bleaching['Severity'].apply(convert_severity)


def calculate_island_statistics(df_rugosity, df_bleaching):
    """
    Calculate the median and mean values of Heterogeneity and Bleaching Severity for each island.

    Parameters:
    ----------
    df_rugosity (DataFrame): DataFrame containing the Heterogeneity data.
    df_bleaching (DataFrame): DataFrame containing the Bleaching Severity data.

    Returns:
    -------
    tuple: Two DataFrames containing the statistical data for Heterogeneity and Bleaching Severity, respectively.
    """

    rugosity_stats = df_rugosity.groupby('Island')['Heterogeneity'].agg(['median', 'mean'])
    bleaching_stats = df_bleaching.groupby('Island')['Severity_Num'].agg(['median', 'mean'])
    return rugosity_stats, bleaching_stats


def plot_to_html_img(plot, popup_title, width=500, height=300):
    """
    Convert a Matplotlib plot to an HTML image and wrap it in a popup.

    Parameters:
    ----------
    plot (Matplotlib plot): The plot object to be converted.
    popup_title (str): The title of the popup.
    width (int, optional): The width of the image, defaults to 500 pixels.
    height (int, optional): The height of the image, defaults to 300 pixels.

    Returns:
    -------
    folium.Popup: The popup object containing the image.
    """

    output = BytesIO()
    plot.get_figure().savefig(output, format='png')
    plt.close(plot.get_figure())
    output.seek(0)
    encoded = base64.b64encode(output.getvalue()).decode('utf-8')
    html = f'<h4>{popup_title}</h4>'
    html += f'<img src="data:image/png;base64,{encoded}" style="width:{width}px;height:{height}px;">'
    iframe = folium.IFrame(html, width=width+20, height=height+60)
    return folium.Popup(iframe)


def create_island_map_rugosity_bleaching_overtime(df_rugosity, df_bleaching):
    """
    Create a map displaying the variation trends of Heterogeneity and Bleaching Severity for all islands overtime.

    Parameters:
    ----------
    df_rugosity (DataFrame): DataFrame containing the Heterogeneity data.
    df_bleaching (DataFrame): DataFrame containing the Bleaching Severity data.

    Returns:
    -------
    folium.Map: The created map object.
    """

    # Initialize the map:
    center_lat, center_lon = get_center_point(df_rugosity)
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Iterate over the islands to create plots:
    for island in df_rugosity['Island'].unique():
        island_df_rugosity = df_rugosity[df_rugosity['Island'] == island]
        island_df_bleaching = df_bleaching[df_bleaching['Island'] == island]
        lat, lon = get_center_point(island_df_rugosity)

        # Create combined rugosity and bleaching plot
        fig, ax = plt.subplots()
        island_df_rugosity.groupby(island_df_rugosity['Start_Date'].dt.year)['Heterogeneity'].mean().plot(ax=ax, legend=True)
        island_df_bleaching.groupby(island_df_bleaching['Start_Date'].dt.year)['Severity_Num'].mean().plot(ax=ax, legend=True)
        plt.title(f'{island} - Rugosity and Bleaching Over Time')
        plt.legend(['Rugosity', 'Bleaching'])

        # Convert plot to HTML image and create popup
        popup = plot_to_html_img(ax, f'{island} - Rugosity and Bleaching Over Time', width=500, height=300)
        folium.Marker([lat, lon], popup=popup).add_to(my_map)

    # Save and return map:
    my_map.save('island_map_rugosity_bleaching_overtime.html')
    return my_map


def create_combined_eachIslandstats_map_rugosity_bleaching(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats):
    """
    Create a map displaying the variation trends of Heterogeneity and Bleaching Severity for each island.

    Parameters:
    ----------
    df_rugosity (DataFrame): DataFrame containing the Heterogeneity data.
    df_bleaching (DataFrame): DataFrame containing the Bleaching Severity data.
    rugosity_stats (DataFrame): DataFrame containing the statistical information for Heterogeneity.
    bleaching_stats (DataFrame): DataFrame containing the statistical information for Bleaching Severity.

    """

    islands = df_rugosity['Island'].unique()
    
    for island in islands:
        island_rugosity_df = df_rugosity[df_rugosity['Island'] == island]
        island_bleaching_df = df_bleaching[df_bleaching['Island'] == island]
        
        if not island_rugosity_df.empty and not island_bleaching_df.empty:
            avg_lat, avg_lon = get_center_point(island_rugosity_df)

            map = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

            # Add Heterogeneity statistical information.
            rugosity_stat = rugosity_stats.loc[island]
            folium.Marker(
                location=[avg_lat, avg_lon],
                popup=f"{island} - Heterogeneity Median: {rugosity_stat['median']}, Mean: {rugosity_stat['mean']}",
                icon=folium.Icon(color="blue")
            ).add_to(map)

            # Add Bleaching Severity statistical information.
            bleaching_stat = bleaching_stats.loc[island]
            folium.Marker(
                location=[avg_lat + 0.02, avg_lon + 0.02],  # Add a slight offset to differentiate the markers.
                popup=f"{island} - Bleaching Severity Median: {bleaching_stat['median']}, Mean: {bleaching_stat['mean']}",
                icon=folium.Icon(color="red")
            ).add_to(map)

            map.save(f"{island}_combined_eachIslandstats_map_rugosity_bleaching.html")


def create_combined_island_map_rugosity_bleaching_statisctic(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats):
    """
    Create a map displaying the statistical data of Heterogeneity and Bleaching Severity for all islands.

    Parameters:
    ----------
    df_rugosity (DataFrame): DataFrame containing the Heterogeneity data.
    df_bleaching (DataFrame): DataFrame containing the Bleaching data.
    rugosity_stats (DataFrame): DataFrame containing the statistical data for Heterogeneity.
    bleaching_stats (DataFrame): DataFrame containing the statistical data for Bleaching Severity.

    Returns:
    -------
    folium.Map: The created map object.
    """
    
    # # Get the center points of all islands for the initial map position.
    center_lat, center_lon = get_center_point(df_rugosity)

    # Create a map instance
    combined_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Iterate over each island and add statistical information
    for island in df_rugosity['Island'].unique():
        island_rugosity = rugosity_stats.loc[island]
        island_bleaching = bleaching_stats.loc[island]

        # Calculate the center point of the island
        island_lat, island_lon = get_center_point(df_rugosity[df_rugosity['Island'] == island])

        # Add markers for Heterogeneity and Bleaching
        folium.Marker(
            location=[island_lat, island_lon],
            popup=(f"{island} - Heterogeneity\n"
                   f"Median: {island_rugosity['median']}, Mean: {island_rugosity['mean']}\n"
                   f"Bleaching Severity\n"
                   f"Median: {island_bleaching['median']}, Mean: {island_bleaching['mean']}"),
            icon=folium.Icon(color='green')
        ).add_to(combined_map)

    # Save the map as an HTML file
    combined_map.save('combined_island_map_rugosity_bleaching_statisctic.html')

def create_separate_markers_map_rugosity_bleaching(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats):
    """
    Creates a map with separate markers for rugosity and bleaching statistics of each island.

    Parameters:
    - df_rugosity (DataFrame): DataFrame containing rugosity data.
    - df_bleaching (DataFrame): DataFrame containing severity data.
    - rugosity_stats (DataFrame): Statistics of fish rugosity for each island.
    - bleaching_stats (DataFrame): Statistics of bleaching severity size for each island.

    """
    # Obtain the center points of all islands for the initial map position
    center_lat, center_lon = get_center_point(df_rugosity)

    # Create a map instance
    combined_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Iterate over each island and add statistical information
    for island in df_rugosity['Island'].unique():
        island_rugosity = rugosity_stats.loc[island]
        island_bleaching = bleaching_stats.loc[island]

        # Calculate the center point of the island 
        island_lat, island_lon = get_center_point(df_rugosity[df_rugosity['Island'] == island])

        # Add a marker for Heterogeneity
        folium.Marker(
            location=[island_lat, island_lon],
            popup=f"Heterogeneity - Median: {island_rugosity['median']}, Mean: {island_rugosity['mean']}",
            icon=folium.Icon(color='blue')
        ).add_to(combined_map)

        # Add a marker for Bleaching Severity, slightly offset the position for differentiation
        folium.Marker(
            location=[island_lat + 0.02, island_lon + 0.02],
            popup=f"Bleaching Severity - Median: {island_bleaching['median']}, Mean: {island_bleaching['mean']}",
            icon=folium.Icon(color='red')
        ).add_to(combined_map)

    # Save the map as an HTML file 
    combined_map.save('separate_markers_map_rugosity_bleaching.html')

def main():
    rugosity_stats, bleaching_stats = calculate_island_statistics(df_rugosity, df_bleaching)

    create_island_map_rugosity_bleaching_overtime(df_rugosity, df_bleaching) 
    create_combined_eachIslandstats_map_rugosity_bleaching(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats) 
    create_combined_island_map_rugosity_bleaching_statisctic(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats)
    create_separate_markers_map_rugosity_bleaching(df_rugosity, df_bleaching, rugosity_stats, bleaching_stats)
   
   
if __name__ == "__main__":
    main()