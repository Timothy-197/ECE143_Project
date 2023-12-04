# file: biomass_analysis.py
import data_process as dp
import matplotlib.pyplot as plt 
import statistics as st
import pandas as pd
import folium
import webbrowser
from folium.plugins import MarkerCluster
import base64
from io import BytesIO

data_loader = dp.Data_Loader_biomass_density_change()
df_density = data_loader.get_df_time_fish_density()
df_size = data_loader.get_df_time_juvenile_size()



def get_center_point(df):
    """
    Calculates the center point of all islands.

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

def calculate_island_statistics(df_density, df_size):
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
    density_stats = df_density.groupby('Island')['Density'].agg(['median', 'mean'])
    size_stats = df_size.groupby('Island')['Size_mm'].agg(['median', 'mean'])
    return density_stats, size_stats

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

def create_island_map_density_size_overtime(df_density, df_size):
    """
    Create a map displaying the variation trends of Fish Density and Juvenile Size for all islands overtime.

    Parameters:
    ----------
    df_densit (DataFrame): DataFrame containing the Heterogeneity data.
    df_size (DataFrame): DataFrame containing the Bleaching Severity data.

    Returns:
    -------
    folium.Map: The created map object.
    """
    # Initialize the map:
    center_lat, center_lon = get_center_point(df_density)
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Iterate over the islands to create plots:
    for island in df_density['Island'].unique():
        island_df_density = df_density[df_density['Island'] == island]
        island_df_size = df_size[df_size['Island'] == island]
        lat, lon = get_center_point(island_df_density)

        # Create combined rugosity and bleaching plot
        fig, ax = plt.subplots()
        island_df_density.groupby(island_df_density['Start_Date'].dt.year)['Density'].mean().plot(ax=ax, legend=True)
        island_df_size.groupby(island_df_size['Start_Date'].dt.year)['Size_mm'].mean().plot(ax=ax, legend=True)
        plt.title(f'{island} - Density and Size Over Time')
        plt.legend(['Density', 'Size'])

        # Convert plot to HTML image and create popup
        popup = plot_to_html_img(ax, f'{island} - Density and Size Over Time', width=500, height=300)
        folium.Marker([lat, lon], popup=popup).add_to(my_map)

    # Save and return map:
    my_map.save('island_map_density_size_overtime.html')
    return my_map


def create_separate_markers_map_density_size(df_density, df_size, density_stats, size_stats):
    """
    Creates a map with separate markers for density and size statistics of each island.

    Parameters:
    ----------
    - df_density (DataFrame): DataFrame containing fish density data.
    - df_size (DataFrame): DataFrame containing juvenile size data.
    - density_stats (DataFrame): Statistics of fish density for each island.
    - size_stats (DataFrame): Statistics of juvenile size for each island.
    """

    # Obtain the center points of all islands for the initial map position
    center_lat, center_lon = get_center_point(df_density)
    combined_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Iterate over each island and add statistical information
    for island in df_density['Island'].unique():
        island_density = density_stats.loc[island]
        
       # Calculate the center point of the island 
        island_lat, island_lon = get_center_point(df_density[df_density['Island'] == island])
        
        # Add a marker for Density
        folium.Marker(
            location=[island_lat, island_lon],
            popup=f"Density - Median: {island_density['median']}, Mean: {island_density['mean']}",
            icon=folium.Icon(color='blue')
        ).add_to(combined_map)
        
        
        if island in size_stats.index:
            island_size = size_stats.loc[island]
            folium.Marker(
                location=[island_lat + 0.02, island_lon + 0.02],  # 小幅偏移以区分标记
                popup=f"Size - Median: {island_size['median']}, Mean: {island_size['mean']}",
                icon=folium.Icon(color='green')
            ).add_to(combined_map)

    combined_map.save('separate_markers_map_density_size.html')




def main():
    density_stats, size_stats = calculate_island_statistics(df_density, df_size)
    
    create_island_map_density_size_overtime(df_density, df_size)
    create_separate_markers_map_density_size(df_density, df_size, density_stats, size_stats)

   
if __name__ == "__main__":
    main()


