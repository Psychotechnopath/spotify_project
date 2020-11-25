#%%
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import pickle
from collections import Counter

df = pd.read_csv("Dataframes_Pickles/full_top_2000_audio_features.csv", header=0, index_col=[0])

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


#Function for plotting average internal track features
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
# data_plotter('danceability')


with open('Dataframes_Pickles/genre_data_list.pkl', 'rb') as f4:
    genre_list = pickle.load(f4)
df['genre'] = genre_list


#This function returns a counter object for each year in the top2000
def genre_dict_generator(df_param):
    data_dict = {}
    for i in range(1999, 2019):
        flat_list = []
        #Subset dataframe; for example only take rows where pos1999 is not 0 (So song is in top 2000 of 1999)
        sub_df = df_param[df_param[f'pos{i}'] != 0]
        genre_list_in = list(sub_df['genre'])
        for sublist in genre_list_in:
            if sublist != 0:
                for item in sublist:
                    flat_list.append(item)
        counter = Counter(flat_list)
        data_dict[f'pos{i}'] = counter
    return data_dict


genre_dictionary = genre_dict_generator(df)

#Aggregate sub-genres into big genres. We do this for rock, jazz, hiphop, pop, and dance. We also consider
# the genres beatlesque and mellow gold seperately.
rock_list = ['rock', 'classic rock', 'art rock', 'blues rock',
             'album rock', 'alternative rock', 'belgian rock',
             'dutch rock', 'folk rock',
             'folk rock', 'yacht rock', 'glam rock',
             'hard rock', 'heartland rock', 'irish rock',
             'modern rock', 'permanent wave', 'progressive rock',
             'psychedelic rock', 'pub rock', 'rock-and-roll', 'soft rock', 'symphonic rock']

jazz_list = ['jazz funk', 'jazz', 'jazz blues', 'jazz fusion',
             'jazz pop', 'jazz rock', 'jazz trombone',
             'new orleans jazz', 'soul jazz', 'vocal jazz']

hiphop_list = ['rap', 'hip hop', 'alternative hip hop',
               'gangster rap', 'southern hip hop']

pop_list = ['art pop', 'baroque pop', 'brill building pop'
            'bubblegum pop', 'dutch pop', 'europop', 'french pop',
            'nederpop', 'new wave pop', 'sophisti pop', 'sunshine pop',
            'swedish pop', 'synth pop']

dance_list = ['freak beat', 'hip house', 'pop dance', 'progressive house', 'tropical house', 'eurodance'
              'australian dance', 'bubblegum dance', 'dutch trance', 'edm', 'electro', 'electro house']


#Function that counts the number of times a genre is present in a top2000 for every year we considered.
def genre_per_year_counter(genre_dict_year_param):
    total_rock_occurence, total_jazz_occurence, total_hiphop_occurence, \
    total_pop_occurence, total_dance_occurence, total_beatlesque_occurence, \
    total_mellow_gold_occurence = [] , [], [], [] , [], [], []
    for year in range(1999, 2019):
        year_dict = genre_dict_year_param[f'pos{year}']
        rock_counter ,jazz_counter ,hiphop_counter ,pop_counter, \
        dance_counter, beatlesque_counter ,mellow_gold_counter = 0, 0, 0, 0, 0, 0, 0

        for rock_genre in rock_list:
            rock_counter += year_dict[f'{rock_genre}']
        for jazz_genre in jazz_list:
            jazz_counter += year_dict[f'{jazz_genre}']
        for hiphop_genre in hiphop_list:
            hiphop_counter += year_dict[f'{hiphop_genre}']
        for pop_genre in pop_list:
            pop_counter += year_dict[f'{pop_genre}']
        for dance_genre in dance_list:
            dance_counter += year_dict[f'{dance_genre}']
        beatlesque_counter += year_dict['beatlesque']
        mellow_gold_counter += year_dict['mellow gold']

        total_rock_occurence.append((year, rock_counter))
        total_jazz_occurence.append((year, jazz_counter))
        total_hiphop_occurence.append((year, hiphop_counter))
        total_pop_occurence.append((year, pop_counter))
        total_dance_occurence.append((year, dance_counter))
        total_beatlesque_occurence.append((year, beatlesque_counter))
        total_mellow_gold_occurence.append((year, mellow_gold_counter))
    return total_rock_occurence, total_jazz_occurence,\
            total_hiphop_occurence, total_pop_occurence, total_dance_occurence, \
            total_beatlesque_occurence, total_mellow_gold_occurence

#Calling the function
ttal_rock_occurence, ttal_jazz_occurence, \
ttal_hiphop_occurence, ttal_pop_occurence, ttal_dance_occurence, \
ttal_beatlesque_occurence, ttal_mellow_gold_occurence  = genre_per_year_counter(genre_dictionary)

#Function to plot results
def tuple_plotter(genre_occurence_list, label, title, color, ylabel='Nr of occurences', xlabel='Year'):
    # Results are added to list in this order in previous for-loop
    # Make the actual plot
    plt.figure()
    plt.plot(*zip(*genre_occurence_list), '-o', label=label, color=color)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xscale("linear")
    plt.xticks(np.arange(1999, 2019, step=2))
    plt.legend()
    plt.show()

#Calling the function
tuple_plotter(ttal_rock_occurence, 'Rock Genre', 'Representation of Rock genre in Top2000 over the years', 'red')
tuple_plotter(ttal_jazz_occurence, 'Jazz Genre', 'Representation of Jazz genre in Top2000 over the years', 'purple')
tuple_plotter(ttal_hiphop_occurence, 'HipHop Genre', 'Representation of HipHop genre in Top2000 over the years', 'pink')
tuple_plotter(ttal_pop_occurence, 'Pop Genre', 'Representation of Pop genre in Top2000 over the years', 'blue')
tuple_plotter(ttal_dance_occurence, 'Dance Genre', 'Representation of Dance genre in Top2000 over the years', 'green')
tuple_plotter(ttal_beatlesque_occurence, 'Beatlesque Genre', 'Representation of Beatlesque genre in Top2000 over the years', 'orange')
tuple_plotter(ttal_mellow_gold_occurence, 'Mellow Gold Genre', 'Representation of Mellow Gold genre in Top2000 over the years', 'gold')





