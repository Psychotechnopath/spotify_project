import requests
import pandas as pd
import time
import pickle


CLIENT_ID = "6a4beafca96b44fb8d15c07a64b1ab3c"
CLIENT_SECRET = "bb451993cd9c4d44aed64f7cc901d0bb"
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

#Convert response to JSON
auth_response_data = auth_response.json()

#Save the access token
access_token = auth_response_data['access_token']

#Need to pass access token into header to send properly formed GET request to API server
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

def top2000_merger():
    """Function that takes all the excel lists in the top2000_excel folder, and merges them into one big dataframe"""
    #Initalize empty dataframe
    total_df = pd.DataFrame(columns = {'title', 'artist', 'title_artist', 'year', "pos1999", "pos2000", "pos2001",
                                  "pos2002", "pos2003", "pos2004", "pos2005", "pos2006", "pos2007",
                                  "pos2008", "pos2009", "pos2010", "pos2011", "pos2012", "pos2013",
                                  "pos2014", "pos2015", "pos2016", "pos2017", "pos2018", "pos2019"})
    #For all top2000 files
    for i in range(1999, 2019):
        df = pd.read_excel(f'top2000_excel/top-2000-{i}.xlsx')
        df.rename(columns={i: f'pos{i}'}, inplace=True)
        df['title_artist'] = df['titel'] + df['artiest']
        for ind, row in df.iterrows():
            #If title is already in total df of top2000's aggregated, and
            #If title and artist index are equal, it means the song title does not have the same title, but is performed by another artist.
            #For example, the song Power Of love occurs 4 times, performed by 4 different artists.
            #If indices are equal, we are sure it is already in our list, so we only add the position. at the right place.
            #THIS LINE TOOK ME 1 HOUR TO WRITE :'(
            if ((total_df['title'] == row['titel']) & (total_df['artist'] == row['artiest'])).any():
                #Only insert position at the right place
                index = total_df[total_df['title_artist'] == row['title_artist']].index
                total_df.loc[index, f'pos{i}'] = row[f'pos{i}']
            else:
                #Append all data
                total_df = total_df.append({'title': row['titel'], 'artist':row['artiest'], 'title_artist':row['title_artist'],
                                            'year':row['jaar'], f'pos{i}':row[f'pos{i}']}, ignore_index=True)
    #Subset and remove unique column.
    total_df = total_df[['title', 'artist', 'year', "pos1999", "pos2000", "pos2001",
                                  "pos2002", "pos2003", "pos2004", "pos2005", "pos2006", "pos2007",
                                  "pos2008", "pos2009", "pos2010", "pos2011", "pos2012", "pos2013",
                                  "pos2014", "pos2015", "pos2016", "pos2017", "pos2018"]]
    return total_df


def get_song_uri(total_df_param):
    """Function that hits the spotify API to obtain all the song URI's.
    Take care in re-running this, as some URI's were entered into the resulting CSV of this function,
    as the search endpoint does not work flawlessly."""
    #Initialize empty uri_list to store all the URI's
    uri_list = []
    empty_responses = []
    #Loop over dataframe
    for index, row in total_df_param.iterrows():
        #Generate song title in correct format for search query
        song_title = row['title'].replace("'", " ").replace(' ', '%20').lower()
        #Generate artist name in correct format for search query
        song_artist = row['artist'].replace(' ', '%20').replace('&', '%20').lower()
        #Build search query
        search_query = f"search?q=track:{song_title}%20artist:{song_artist}&type=track&limit=1&market=NL&DE"
        #Build actual requests
        search_request = requests.get(BASE_URL + search_query, headers=headers)
        print("Sending request " + BASE_URL + search_query + " to API server")
        #Convert response to JSON
        response_json = search_request.json()
        #If response not empty, append uri to uri_list. Else append 0.
        try:
            uri_list.append(response_json['tracks']['items'][0]['uri'].replace("spotify:track:", ""))
        except (KeyError, IndexError):
            print("Empty response on song " + row['title'])
            empty_responses.append(row['title'])
            uri_list.append(0)
            continue
    total_df_param['track_uri'] = uri_list
    #Put columns in right order so its easy to manually look up missing URI's
    total_df_param = total_df_param[['title', 'artist', 'track_uri', 'year', "pos1999", "pos2000", "pos2001",
                                  "pos2002", "pos2003", "pos2004", "pos2005", "pos2006", "pos2007",
                                  "pos2008", "pos2009", "pos2010", "pos2011", "pos2012", "pos2013",
                                  "pos2014", "pos2015", "pos2016", "pos2017", "pos2018"]]
    return total_df_param

#Calls are commented out since top2000 dataframe (and should) can be loaded from disk
# total_top_2000 = top2000_merger()
# total_top_2000_uri = get_song_uri(total_top_2000)

#Build in check point because previous two functions take long to execute.
# total_top_2000_uri.to_csv('total_top_2000_uri.csv', header=True)

#Some manual work was done on this spreadsheet, to obtain URI's that were not found by search query. DO NOT OVERWRITE CSV FILE!
top_2000_correct_uri = pd.read_csv('Dataframes_Pickles/total_top_2000_uri.csv', header=0, index_col=[0])

#Sort on index, fill nan values
top_2000_correct_uri.sort_index(inplace=True)
top_2000_correct_uri.fillna(0, inplace=True)

#Make sure everything has correct type again after modifying with excel
top_2000_correct_uri = top_2000_correct_uri.astype({"title": str, "artist":str, "track_uri":str, "year":int,"pos1999":int, "pos2000":int, "pos2001":int,
                                  "pos2002":int, "pos2003":int, "pos2004":int, "pos2005":int, "pos2006":int, "pos2007":int,
                                  "pos2008":int, "pos2009":int, "pos2010":int, "pos2011":int, "pos2012":int, "pos2013":int,
                                  "pos2014":int, "pos2015":int, "pos2016":int, "pos2017":int, "pos2018":int})



def get_audio_features(top2000_df):
    """Function for obtaining internal track features of the songs"""
    #Initialize empty lists to store audio features
    accousticness_list, danceability_list, duration_list, \
    energy_list, instrumentalness_list, loudness_list, \
    speechiness_list, valence_list, tempo_list, liveness_list  = [], [] ,[], [], [] ,[], [], [], [], []
    uri_list = list(top2000_df['track_uri'])

    for uri in uri_list:
        try:
            #Hit API for audio features, append the response to the proper list
            audio_feature_request = requests.get(BASE_URL + 'audio-features/' + uri, headers=headers)
            print("Sending request " + BASE_URL + 'audio-features/'  + uri + " to API server")
            response_json = audio_feature_request.json()
            accousticness_list.append(response_json['acousticness'])
            danceability_list.append(response_json['danceability'])
            duration_list.append(response_json['duration_ms'])
            energy_list.append(response_json['energy'])
            instrumentalness_list.append(response_json['instrumentalness'])
            loudness_list.append(response_json['loudness'])
            speechiness_list.append(response_json['speechiness'])
            valence_list.append(response_json['valence'])
            tempo_list.append(response_json['tempo'])
            liveness_list.append(response_json['liveness'])
        #Except without catch because sometimes there would be a JsonDecodeError and sometimes a KeyError.
        #Non pythonic but it does work. If error, append 0 to audio-feature list.
        except:
            accousticness_list.append(0)
            danceability_list.append(0)
            duration_list.append(0)
            energy_list.append(0)
            instrumentalness_list.append(0)
            loudness_list.append(0)
            speechiness_list.append(0)
            valence_list.append(0)
            tempo_list.append(0)
            liveness_list.append(0)
            continue
    #Set the lists as columns in the dataframe
    top2000_df['acousticness'] = accousticness_list
    top2000_df['danceability'] = danceability_list
    top2000_df['duration_ms'] = duration_list
    top2000_df['energy'] = energy_list
    top2000_df['instrumentalness'] = instrumentalness_list
    top2000_df['loudness'] = loudness_list
    top2000_df['speechiness'] = speechiness_list
    top2000_df['valence'] = valence_list
    top2000_df['tempo'] = tempo_list
    top2000_df['liveness'] = liveness_list
    return top2000_df

#Write the dataframe to CSV
# final_df_audio_features = get_audio_features(top_2000_correct_uri)
# final_df_audio_features.to_csv('full_top_2000_audio_features.csv', header=True)


#Load in again (Checkpoint)
# df_audio_features_loaded = pd.read_csv('Dataframes_Pickles/full_top_2000_audio_features.csv')


def get_artist_uri(top_2000_df):
    """Function to get the Artist URI from the Spotify API"""
    #Load all song uri's
    uri_list = list(top_2000_df['track_uri'])
    #Initialize empty artist_uri list
    artist_uri_list = []
    for uri in uri_list:
        #Hit API to obtain artist URI.
        try:
            complete_track_request = requests.get(BASE_URL + 'tracks/' + uri, headers=headers)
            print("Sending request " + BASE_URL + 'tracks/'  + uri + " to API server")
            print(complete_track_request)
            response_json = complete_track_request.json()
            artist_uri = response_json['album']['artists'][0]['uri'].replace("spotify:artist:", "")
            artist_uri_list.append(artist_uri)
            time.sleep(0.2)
        #Except empty response
        except KeyError:
            print("Key Error")
            artist_uri_list.append(0)
    return artist_uri_list

#CHECKPOINT
# artist_uri_list = get_artist_uri(df_audio_features_loaded)
# with open('artist_uri_list.pkl', 'wb') as f:
#     pickle.dump(artist_uri_list, f)

with open('Dataframes_Pickles/artist_uri_list.pkl', 'rb') as f2:
    artist_uri_list_pkl = pickle.load(f2)


def get_genre_data(artist_uri_list_param):
    """Function to obtain genre data"""
    artist_list_string = [str(i) for i in artist_uri_list_param]
    genre_data_list = []
    for artist_uri in artist_list_string:
        try:
            complete_artist_request = requests.get(BASE_URL + 'artists/'+ artist_uri,  headers=headers)
            print("Sending request " + BASE_URL + 'artists/'  + artist_uri + " to API server")
            print(complete_artist_request)
            artist_response_json = complete_artist_request.json()
            genre = artist_response_json['genres']
            print(type(genre))
            genre_data_list.append(genre)
            time.sleep(0.1)
        except KeyError:
            genre_data_list.append(0)
    return genre_data_list

# genre_data_list = get_genre_data(artist_uri_list_pkl)

#Sometimes empty list because of no genre, sometimes 0 because of keyerror
# for index, sublist in enumerate(genre_data_list):
#     if not sublist:
#         genre_data_list[index] = 0
#
# #Pickle the object for later use, checkpoint
# with open('Dataframes_Pickles/genre_data_list.pkl', 'wb') as f3:
#     pickle.dump(genre_data_list, f3)


