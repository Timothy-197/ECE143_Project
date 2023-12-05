import DataProcess.data_process as dp
import matplotlib.pyplot as plt   
from matplotlib.patches import Patch
import statistics as st
import pandas as pd  
import numpy as np
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
    assert stats=='Mean' or stats=='Median' or stats=='Window' or stats=='Scatter' #Did not enter either --> stats=='Mean' or stats=='Median' or stats=='Window' or stats=='Scatter'
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
            elif stats=='Scatter': 
                stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict])
            else: 
                raise NotImplementedError 

            #plot
            fig, (ax1, ax2) =plt.subplots( nrows=2, ncols=1, figsize=(10,8))
            
            ax1.set_title(f'Scatter Plot For Fish {vis} in {island} Since 2009')
            ax1.scatter(sorted_time_axis, sorted_vistype_axis)  
            ax1.set_xlabel('Years') 
            ax1.set_ylabel('Fish Density')

            ax2.set_title(f'{stats} For Fish {vis} in {island} Since 2009') 
            if stats!='Scatter':
                ax2.plot(stats_vistype_time_axis,stats_density)   
            elif stats=='Scatter': 
                ax2.scatter(stats_vistype_time_axis,stats_density) 
                a, b = np.polyfit(np.array(stats_vistype_time_axis), np.array(stats_density), 1)
                plt.plot(np.array(stats_vistype_time_axis), a*np.array(stats_vistype_time_axis)+b)
            else: 
                raise NotImplementedError

            ax2.set_xlabel('Years') 
            ax2.set_ylabel('Fish Density') 

            #plt.savefig(f'datavis/{stats}_{island}_{vis}.jpg')
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
                elif stats=='Scatter': 
                    stats_vistype_time_axis, stats_density=zip(*[(key,st.mean(stats_vistype_dict[key])) for key in stats_vistype_dict])
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

                    if stats != 'Scatter':
                        ax[1,index].plot(data_per_taxon[key]['stats_vistype_time_axis'],data_per_taxon[key]['stats_density']) 
                        ax[1,index].set_xlabel('Years') 
                        ax[1,index].set_ylabel('Fish Density')  
                    elif stats=='Scatter':  
                        ax[1,index].scatter(data_per_taxon[key]['stats_vistype_time_axis'],data_per_taxon[key]['stats_density']) 
                        a, b = np.polyfit(np.array(data_per_taxon[key]['stats_vistype_time_axis']), np.array(data_per_taxon[key]['stats_density']), 1)
                        ax[1,index].plot(np.array(data_per_taxon[key]['stats_vistype_time_axis']), a*np.array(data_per_taxon[key]['stats_vistype_time_axis'])+b) 
                        ax[1,index].set_xlabel('Years') 
                        ax[1,index].set_ylabel('Fish Density')  
                        

                fig.suptitle(f'Scatter Plot and {stats} For {key} {vis} in {island} Since 2009', fontsize=16)
                
                plt.tight_layout()
                plt.show()  

def get_taxon_piechart(vis='Density'): 
    ''' 
        Function: get_taxon_piechart(vis='Density'):  

        --> Gets the top 10 most common genus accross all islands at once, individually and alltogether. 

        example:
        --------
        >>>get_taxon_piechart():
        (matplot graphs)
         
        param str vis: vis=='Density' or vis=='Size' for type of visualization to obtain. Default to 'Density'  

        returns: Gets the top 10 most common genus accross all islands at once, individually and alltogether. 
    ''' 
    for island in set(dp.Data_Loader_biomass_density_change().get_df_time_fish_density()['Island']): #['Tutuila', 'Hawaii', 'Molokai', 'Guam']
        if vis=='Density':
            #Biomass Density Dataframe overall
            vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_fish_density()   

            #Biomass Density Dataframe, Densities at specific island
            vis_data_frame_vistype=vis_data_frame[vis_data_frame['Island']==island]['Taxon_Name']  
            

        elif vis=='Size':  

            #Size Stats only available for island of Molokai
            if island != 'Molokai': 
                continue

            #Juvinile Colony Dataframe overall
            vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_juvenile_size()   

            #Juvinile Colony Dataframe, Sizes at specific island
            vis_data_frame_vistype=vis_data_frame[vis_data_frame['Island']==island]['Taxon_Name']   
            
        else: 
            raise NotImplementedError 
        fish_df_raw=pd.DataFrame({'fish':[name.split()[0] for name in vis_data_frame_vistype]}).value_counts() 
        fish_df_raw=pd.DataFrame({'fish':fish_df_raw.index, 'counts':fish_df_raw.values}) 
        fish_df=pd.DataFrame({'fish':fish_df_raw['fish'].apply(lambda x: x[0]),'counts':100*(fish_df_raw['counts']/fish_df_raw['counts'].sum())}).head(5) 
        
        fish_df_2=pd.DataFrame({'fish':['Other'],'counts':[100-fish_df['counts'].sum()]})  
        print(fish_df_2)
        fish_df=pd.concat([fish_df,fish_df_2]) 
        
        fig, ax = plt.subplots() 
        explode=[0 for i in range(len(fish_df))] 
        explode[0]=0.3 

        ax.pie(fish_df['counts'], labels=fish_df['fish'], autopct='%1.1f%%',explode=explode) 
        ax.set_title(f'Frequency of Genus on {island}')
        
        #plt.savefig(f'piecharts/{island}.jpg')
        plt.tight_layout()
        plt.show()

    fish_df_raw=pd.DataFrame({'fish':[name.split()[0] for name in vis_data_frame['Taxon_Name']]}).value_counts() 
    fish_df_raw=pd.DataFrame({'fish':fish_df_raw.index, 'counts':fish_df_raw.values}) 
    fish_df=pd.DataFrame({'fish':fish_df_raw['fish'].apply(lambda x: x[0]),'counts':100*(fish_df_raw['counts']/fish_df_raw['counts'].sum())}).head(5) 
    
    fish_df_2=pd.DataFrame({'fish':['Other'],'counts':[100-fish_df['counts'].sum()]})  
    print(fish_df_2)
    fish_df=pd.concat([fish_df,fish_df_2]) 
    
    fig, ax = plt.subplots() 
    explode=[0 for i in range(len(fish_df))] 
    explode[0]=0.3 

    ax.pie(fish_df['counts'], labels=fish_df['fish'], autopct='%1.1f%%',explode=explode) 
    ax.set_title(f'Frequency of Genus Overall')
    
    #plt.savefig(f'piecharts/all_islands.jpg')
    plt.tight_layout()
    plt.show()    

def get_taxon_over_time(vis='Density'): 
    ''' 
        Function: get_taxon_over_time(vis='Density'):  

        --> gets the top 10 most common genus per year per island in percents. 

        example:
        --------
        >>>get_taxon_over_time(vis='Density') 
        (matplot graphs)
         
        param str vis: Vis=='Density' or Vis=='Size' for type of visualization to obtain. Default to 'Density'  

        returns: gets the top 10 most common genus per year per island in percents. 
    '''

    for island in set(dp.Data_Loader_biomass_density_change().get_df_time_fish_density()['Island']): #['Tutuila', 'Hawaii', 'Molokai', 'Guam']
        
        if vis=='Density':
            #Biomass Density Dataframe overall
            vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_fish_density()   

            #Biomass Density Dataframe; Dates at specific island
            vis_data_frame_dates=vis_data_frame[(vis_data_frame['Island']==island)]['Start_Date']  
            
            #Biomass Density Dataframe, Densities at specific island
            vis_data_frame_vistype=vis_data_frame[(vis_data_frame['Island']==island)]['Taxon_Name']            
            
             
        elif vis=='Size':  

            #Size Stats only available for island of Molokai
            if island != 'Molokai': 
                continue

            #Juvinile Colony Dataframe overall
            vis_data_frame=dp.Data_Loader_biomass_density_change().get_df_time_juvenile_size()   
            
            #Juvinile Colony Dataframe; Dates at specific island
            vis_data_frame_dates=vis_data_frame[(vis_data_frame['Island']==island)]['Start_Date']  
            #Juvinile Colony Dataframe, Sizes at specific island
            vis_data_frame_vistype=vis_data_frame[(vis_data_frame['Island']==island)]['Taxon_Name']   
            
        
        else: 
            raise NotImplementedError  
        
        

        time_axis=[int(str(date).split('-')[0]) for date in vis_data_frame_dates]  
        
        #creates a dict where the keys are the year, and the values are arrays that contain the genus that was recorded that year.
        taxon_breakdown_per_date_names={}
        for date_fish in zip(time_axis,list(vis_data_frame_vistype)): 
            try: 
                taxon_breakdown_per_date_names[date_fish[0]].append(date_fish[1].split()[0]) 
            except KeyError: 
                taxon_breakdown_per_date_names[date_fish[0]]=[date_fish[1].split()[0]]  

        #creates a dict where the keys are the year and the values are dicts, where the keys are the genus, and the values are percentage of times it appears.
        taxon_breakdown_per_date_numbers={}
        for key in taxon_breakdown_per_date_names: 
            breakdown_per_taxon={} 
            for taxon_name in vis_data_frame_vistype.unique():  
                if taxon_name.split()[0] in taxon_breakdown_per_date_names[key]:
                    breakdown_per_taxon[taxon_name.split()[0]]=(((pd.Series(taxon_breakdown_per_date_names[key])==taxon_name.split()[0]).sum()/len(taxon_breakdown_per_date_names[key]))*100) 
                else: 
                    breakdown_per_taxon[taxon_name.split()[0]]=0
            taxon_breakdown_per_date_numbers[key]=breakdown_per_taxon    
        
          
        #undicts the taxon_breakdown_per_date_numbers and separate sthem into lists of date, genus, and percents.
        taxon_breakdown_per_date_list=sorted([(key, 
                                        list(taxon_breakdown_per_date_numbers[key].keys()),  
                                        list(taxon_breakdown_per_date_numbers[key].values())) for key in taxon_breakdown_per_date_numbers])
            
        fig, ax = plt.subplots(figsize=(10,10))
        ax.set_title('Animated Fish Quantities per Date')
        ax.set_ylabel('Fish Types')
        ax.set_xlabel('Quantity')
        
        #for loop that generates the animation for top 10 most common genus per year.
        for i in range(len(taxon_breakdown_per_date_list)):
            #print(f'{taxon_breakdown_per_date_list[i][0]} : {max(zip(taxon_breakdown_per_date_list[i][2],taxon_breakdown_per_date_list[i][1]))} ')
            #'''
            ax.set_title(f'10 Most Common Genus on {island} \n {(int(taxon_breakdown_per_date_list[i][0]))}')
            ax.set_ylabel('Fish Genus')
           
            

            # Plot the animated histogram 
            fish_df=pd.DataFrame({'fish':taxon_breakdown_per_date_list[i][1],'quantity':taxon_breakdown_per_date_list[i][2]}).sort_values(by='quantity')
            
            fish_mode=str(pd.Series([name.split()[0] for name in vis_data_frame['Taxon_Name']]).mode()[0])  
            non_highlight_color='#768493' 
            highlight_color='#1f77b4'

            fish_df['colors']=fish_df['fish'].apply(lambda x: highlight_color if str(x) == fish_mode else non_highlight_color)  
            bars=plt.barh(fish_df.tail(10)['fish'],fish_df.tail(10)['quantity'],height=0.8,color=fish_df.tail(10)['colors'])  
            
            ax.spines[['right','bottom','top']].set_visible(False) 
            ax.xaxis.set_visible(False) 
            ax.bar_label(bars, padding=-45, color='white',fontsize=10,label_type='edge',fmt='%.1f%%',fontweight='bold')
            #plt.tight_layout
            plt.xlim(0, 30) 
            plt.legend(handles=[Patch(facecolor="#1f77b4", label="Most Frequently Appearing Genus Since 2009")],loc='lower right')
            plt.yticks(fontsize=10)  # Set a smaller font size for y-axis labels
            plt.subplots_adjust(left=0.2)  # Adjust the left margin
            plt.draw()  
            #plt.savefig(f'taxon_time/Taxon_{island}_frame_{i}.jpg') USE THIS TO SAVE EACH FIGURE
            plt.pause(0.3) 
            ax.cla()
            #'''
        plt.close()
        
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
    get_fish_data_visualization(stats='Mean', vis='Density', taxon=False, window=4) 
    get_fish_data_visualization(stats='Window', vis='Density', taxon=False, window=4) 
    get_fish_data_visualization(stats='Scatter', vis='Density', taxon=False, window=4) 
    get_fish_data_visualization(stats='Median', vis='Density', taxon=False, window=4)  
    get_fish_data_visualization(stats='Mean', vis='Size', taxon=False, window=4) 
    get_fish_data_visualization(stats='Window', vis='Size', taxon=False, window=4) 
    get_fish_data_visualization(stats='Scatter', vis='Size', taxon=False, window=4) 
    get_fish_data_visualization(stats='Median', vis='Size', taxon=False, window=4)  
    get_taxon_over_time(vis='Density') 
    get_taxon_piechart(vis='Density')
   
    


