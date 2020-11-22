#%%
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


df = pd.read_csv("full_top_2000_audio_features.csv", header=0, index_col=[0])


def data_dict_generator():
    #Initialize empty dict
    data_dict = {}
    for i in range(1999, 2019):
        #Subset dataframe; for example only take rows where pos1999 is not 0 (So song is in top 2000 of 1999)
        sub_df = df[df[f'pos{i}'] != 0]
        #Calculate means, add as dictionary.
        data_dict[f'pos{i}'] = {'acousticness' : sub_df['acousticness'].mean(),
                                'danceability':sub_df['danceability'].mean(),
                                'duration_ms':sub_df['duration_ms'].mean(),
                                'energy':sub_df['energy'].mean(),
                                'instrumentalness':sub_df['instrumentalness'].mean(),
                                'loudness':sub_df['loudness'].mean(),
                                'speechiness':sub_df['speechiness'].mean(),
                                'valence':sub_df['valence'].mean(),
                                'tempo':sub_df['tempo'].mean(),
                                'liveliness':sub_df['liveliness'].mean()}
    #Nested dict
    return data_dict

average_data = data_dict_generator()

#%%

def data_plotter(internal_feature):
    year_range = np.arange(1999, 2019, dtype=np.int)
    acousticness_list = []
    for i in range(1999, 2019):
        acousticness_list.append(average_data[f'pos{i}'][f'{internal_feature}'])
    plt.plot(year_range, acousticness_list, '-o')
    plt.title(f'{internal_feature} in top2000 over the years')
    plt.xscale('linear')
    plt.xlabel("Year")
    plt.ylabel(f"{internal_feature}")
    plt.xscale("linear")
    plt.xticks(np.arange(1999, 2019, step=2))
    plt.show()


data_plotter('danceability')