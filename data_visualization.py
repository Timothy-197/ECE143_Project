import DataProcess.data_process as dp
import matplotlib.pyplot as plt 
import statistics as st
import pandas as pd
def get_fish_data_visualization(stats='Mean', vis='Density', taxon=False, window=2):  
    ''' 
    function:def get_biomass_density_visualization(stats): 

    --> gets the scatterplot and statistical operation (mean or median) visulaizations of the biomass density per island. 
    --> gets the scatterplot and statistical operation (mean or median) visulaizations of the juvinile colony size per island. 
    --> gets the scatterplot and statistical operation (mean or median) visulaizations per each taxon if set. 

    example:
    --------
    >>>get_biomass_density_visualization('Mean') 
    (matplot graphs)
    
    param str stats: stats=='Mean' or stats=='Median' or stats=='Window' for the statistical operation to be performed. Default to 'Mean' 
    param str vis: Vis=='Density' or Vis=='Size' for type of visualization to obtain. Default to 'Density'  
    param bool taxon: Shows the statistics among each individual taxon per island when set to True. 
    param int window: Optional. Determine window size for a stats=='Window' operation

    returns: gets the scatterplot and statistical operation (mean or median) visulaizations of the biomass density per island. 
    '''
    assert stats=='Mean' or stats=='Median' or stats=='Window' #Did not enter either --> stats=='Mean' or stats=='Median' or stats=='Window'
    assert vis=='Density' or vis=='Size'    #Did not enter either --> vis=='Density' or vis=='Size'
    assert isinstance(taxon, bool)          #Did not enter --> a boolean value.
    assert isinstance(window,int) and window > 0

    for island in set(dp.Data_Loader_biomass_density_change().get_df_time_fish_density()['Island']): #['Tutuila', 'Hawaii', 'Molokai', 'Guam']
        if taxon==False:
            if vis=='Density':
                #Biomass Density Dataframe overall
                vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_fish_density()   

                #Biomass Density Dataframe; Dates at specific island
                vis_data_frame_dates=vis_data_frame[vis_data_frame['Island']==island]['Start_Date']  

                #Biomass Density Dataframe, Densities at specific island
                vis_data_frame_vistype=vis_data_frame[vis_data_frame['Island']==island]['Density'] 

            elif vis=='Size':  

                #Size Stats only available for island of Molokai
                if island != 'Molokai': 
                    continue

                #Juvinile Colony Dataframe overall
                vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_juvenile_size()   
                
                #Juvinile Colony Dataframe; Dates at specific island
                vis_data_frame_dates=vis_data_frame[vis_data_frame['Island']==island]['Start_Date']  

                #Juvinile Colony Dataframe, Sizes at specific island
                vis_data_frame_vistype=vis_data_frame[vis_data_frame['Island']==island]['Size_mm']   
            
            else: 
                raise NotImplementedError   


            #Create Time axis by adding the year to the (month-1)/12 for sorting purposes
            time_axis=[int(str(date).split('-')[0])+(int(str(date).split('-')[1])-1)/12 for date in vis_data_frame_dates] 

            #Create density axis
            vistype_axis=[float(density) for density in vis_data_frame_vistype] 

            #Create Sorted Axes
            sorted_time_axis, sorted_vistype_axis=zip(*sorted(zip(time_axis,vistype_axis)))  

            #Create new dict for the purpose of condensing the multiple points on a single date
            stats_vistype_dict={}

            for x_y in sorted(zip(time_axis,vistype_axis)): 
                try: 
                    stats_vistype_dict[x_y[0]].append(x_y[1]) 
                except KeyError: 
                    stats_vistype_dict[x_y[0]]=[x_y[1]] 
            ''' 
            #shows the entire median_density_dict line per line.
            for key in median_density_dict: 
                print(f'{key}:{median_density_dict[key]}\n')

            #shows averages are the same
            print(biomass_density[(biomass_density['Island'] == 'Hawaii') & (biomass_density['Entered_Date'] == '2009-1')]['Density'].mean())
            print(st.mean(median_density_dict[2009.0]))
            '''  

            #perform the statistical operation
            if stats=='Mean':
                stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict])
            elif stats=='Median': 
                stats_vistype_time_axis, stats_density=zip(*[(key,st.median(stats_vistype_dict[key])) for key in stats_vistype_dict]) 
            elif stats=='Window': 
                stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict]) 
                stats_density=list(pd.DataFrame(stats_density,index=stats_vistype_time_axis).rolling(window).mean()[0])
                
            else: 
                raise NotImplementedError 

            #plot
            fig, (ax1, ax2) =plt.subplots( nrows=2, ncols=1, figsize=(6,4))
            
            ax1.set_title(f'Scatter Plot For Fish {vis} in {island} Since 2009')
            ax1.scatter(sorted_time_axis, sorted_vistype_axis)  
            ax1.set_xlabel('Years') 
            ax1.set_ylabel('Fish Density')

            ax2.set_title(f'{stats} For Fish {vis} in {island} Since 2009')
            ax2.plot(stats_vistype_time_axis,stats_density) 
            ax2.set_xlabel('Years') 
            ax2.set_ylabel('Fish Density')
            plt.tight_layout()
            plt.show()
        
        elif taxon==True: 
            data_per_taxon={} 
            
            for taxonomy in set(dp.Data_Loader_biomass_density_change().get_df_time_fish_density()['Type']):#{'Invert', 'Algae', 'Fish', 'Coral'}
                
                if vis=='Density':
                    #Biomass Density Dataframe overall
                    vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_fish_density()   

                    #Biomass Density Dataframe; Dates at specific island
                    vis_data_frame_dates=vis_data_frame[(vis_data_frame['Island']==island) & (vis_data_frame['Type']==taxonomy)]['Start_Date']  
                    
                    #Biomass Density Dataframe, Densities at specific island
                    vis_data_frame_vistype=vis_data_frame[(vis_data_frame['Island']==island) & (vis_data_frame['Type']==taxonomy)]['Density'] 
                    
                elif vis=='Size':  

                    #Size Stats only available for island of Molokai
                    if island != 'Molokai' or taxonomy !='Coral': 
                        continue

                    #Juvinile Colony Dataframe overall
                    vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_juvenile_size()   
                    
                    #Juvinile Colony Dataframe; Dates at specific island
                    vis_data_frame_dates=vis_data_frame[(vis_data_frame['Island']==island) & (vis_data_frame['Type']==taxonomy)]['Start_Date']  
                    #Juvinile Colony Dataframe, Sizes at specific island
                    vis_data_frame_vistype=vis_data_frame[(vis_data_frame['Island']==island) & (vis_data_frame['Type']==taxonomy)]['Size_mm']   
                
                else: 
                    raise NotImplementedError  
                #Create Time axis by adding the year to the (month-1)/12 for sorting purposes
                time_axis=[int(str(date).split('-')[0])+(int(str(date).split('-')[1])-1)/12 for date in vis_data_frame_dates] 
                
                #Create density axis
                vistype_axis=[float(density) for density in vis_data_frame_vistype] 
                
                if len(time_axis)==0 or len(vistype_axis)==0: #seems like some taxon types do not have data associated with them. 
                    #this print statement shows this is the case.
                    #print(f"{taxonomy}:{len(vis_data_frame[(vis_data_frame['Island']==island) & (vis_data_frame['Type']==taxonomy)]['Start_Date'])}")
                    continue 

                #Create Sorted Axes
                sorted_time_axis, sorted_vistype_axis=zip(*sorted(zip(time_axis,vistype_axis)))  

                #Create new dict for the purpose of condensing the multiple points on a single date
                stats_vistype_dict={}

                for x_y in sorted(zip(time_axis,vistype_axis)): 
                    try: 
                        stats_vistype_dict[x_y[0]].append(x_y[1]) 
                    except KeyError: 
                        stats_vistype_dict[x_y[0]]=[x_y[1]] 

                if stats=='Mean':
                    stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict])
                elif stats=='Median': 
                    stats_vistype_time_axis, stats_density=zip(*[(key,st.median(stats_vistype_dict[key])) for key in stats_vistype_dict])  
                elif stats=='Window': 
                    stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict]) 
                    stats_density=list(pd.DataFrame(stats_density,index=stats_vistype_time_axis).rolling(window).mean()[0])
                else: 
                    raise NotImplementedError  
                
                data_per_taxon[taxonomy]={'sorted_time_axis':sorted_time_axis,  
                                       'sorted_vistype_axis':sorted_vistype_axis,  
                                       'stats_vistype_time_axis':stats_vistype_time_axis, 
                                       'stats_density':stats_density}  
            
            if len(data_per_taxon) != 0: #mainly for the vis='Size' operation since there is only data for one island.
                fig, ax =plt.subplots( nrows=2, ncols=4, figsize=(10,8))
                
                for index, key in enumerate(data_per_taxon): 
                    ax[0,index].set_title(f'{key}')
                    ax[0,index].scatter(data_per_taxon[key]['sorted_time_axis'], data_per_taxon[key]['sorted_vistype_axis'])  
                    ax[0,index].set_xlabel('Years') 
                    ax[0,index].set_ylabel('Fish Density')

                    ax[1,index].plot(data_per_taxon[key]['stats_vistype_time_axis'],data_per_taxon[key]['stats_density']) 
                    ax[1,index].set_xlabel('Years') 
                    ax[1,index].set_ylabel('Fish Density') 

                fig.suptitle(f'Scatter Plot and {stats} For {key} {vis} in {island} Since 2009', fontsize=16)
                
                plt.tight_layout()
                plt.show()  


'''
print(dp.Data_Loader_biomass_density_change().get_df_time_fish_density().columns)
print(dp.Data_Loader_biomass_density_change().get_df_time_juvenile_size().columns) 
print(dp.Data_loader_coral_reef_health().get_df_time_loc_rugosity().columns)

print(set(dp.Data_Loader_biomass_density_change().get_df_time_fish_density()['Island']))
print(set(dp.Data_loader_coral_reef_health().get_df_time_loc_rugosity()['Site_ID']))
'''
'''
coral_reef_rugosity=dp.Data_loader_coral_reef_health().get_df_time_loc_rugosity()  
site_id='{B2472B30-77EA-4247-9FF8-B93033138632}'
coral_reef_rugosity_loc_1=coral_reef_rugosity[coral_reef_rugosity['Site_ID']==site_id]['Heterogeneity']
coral_reef_rugosity_loc_1_dates=coral_reef_rugosity[coral_reef_rugosity['Site_ID']==site_id]['Entered_Date']

time_axis=[int(str(date).split('-')[0])+int(str(date).split('-')[1])/12 for date in coral_reef_rugosity_loc_1_dates ] 

rugosity_axis=[float(heterogeneity) for heterogeneity in coral_reef_rugosity_loc_1] 

sorted_time_axis, sorted_rugosity_axis=zip(*sorted(zip(time_axis,rugosity_axis))) 

plt.scatter(sorted_time_axis, sorted_rugosity_axis) 

plt.show()
'''
if __name__ == "__main__": 
    #get_fish_data_visualization(stats='Window', vis='Density', taxon=True, window=2)
    get_fish_data_visualization(stats='Mean', vis='Density', taxon=True, window=2)
   
    


