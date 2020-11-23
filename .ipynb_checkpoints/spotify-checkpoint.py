import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

username = "vtbsehx9v3qo47y03eznmrz5o"
clientid = "-"
secret = "-"

client_credentials_manager = SpotifyClientCredentials(clientid, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#genres available according to spotify
'''
avgenres = sp.recommendation_genre_seeds()
for genre in avgenres["genres"]:
	print(genre, end="\n")
	'''

#genres according to website
genres1 = ["pop","dance pop","rap","pop rap","rock","post-teen pop","hip hop","trap music","r&b","modern rock"]

#genres according to website and available
genres2 = ["pop","dance","rock","hip-hop","r-n-b"]

f = open(filename,"w")
f.write("artist,name,popularity,id,genre,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,duration\n")

for genre in genres2:
	#for i in range(10):
	songs = sp.recommendations(seed_artists=None, seed_genres=[genre], seed_tracks=None, limit=100, country="NL")
	print("gathered songs from genre: " + genre + " " + str(i+1) + " times")
	
	ids = [song["id"] for song in songs["tracks"]]
	features = sp.audio_features(ids)
	print("gathered features from genre: " + genre + " " + str(i+1) + " times")
	
	for i, song in enumerate(songs["tracks"]):
		f.write(song["artists"][0]["name"]+ "," + 
				str(song["name"].replace(",","")) + "," + 
				str(song["popularity"]) + "," + 
				str(song["id"]) + "," +
				str(genre) + "," + 
				str(features[i]["danceability"]) + "," + 
				str(features[i]["energy"]) + "," +
				str(features[i]["key"]) + "," +
				str(features[i]["loudness"]) + "," +
				str(features[i]["mode"]) + "," +
				str(features[i]["speechiness"]) + "," +
				str(features[i]["acousticness"]) + "," +
				str(features[i]["instrumentalness"]) + "," +
				str(features[i]["liveness"]) + "," +
				str(features[i]["valence"]) + "," +
				str(features[i]["tempo"])+ "," +
				str(features[i]["duration_ms"]) + "\n" )
	print("saved features of genre: " + genre + " to " + filename)
f.close()
