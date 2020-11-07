# Spotify dataset

This bundle contains two different datasets. The readme will explain the contents of both datasets and how to use them. The following datasets are present:

* Spotify music dataset
* Online user rating study

## Spotify music dataset

This dataset contains data on a large number of tracks, artists, albums, genres, user preferences, and recommendations. The data is structured across multiple tables.

### Tables

* album
	* Contains data on music albums
* artists
	* Contains data on artists
* artist_genres
	* Links artists to genres
* audio_features
	* Contains audio analysis features for each tracks
* behavior_log
	* A log file of user behavior of a music player
* cluster_components
	* Results from a clustering algorithm based on the audio_features table
* clusters
	* Results from a clustering algorithm based on the audio_features table
* conditions
	* Links condition identifiers with a framework configuration (recommender system, aggregation function, satisfaction function, track weighting function) See [Master Thesis](https://research.tue.nl/en/studentTheses/evaluating-a-framework-for-sequential-group-music-recommendations).
* configurations
	* Same as conditions, but linked to a specific device that is hosting a group music player system
* genre_distance
	* Results of an algorithm that computes the similarity between two genres based on how often artists belong to both genres.
* genres
	* List of genres and their identifiers
* log
	* Technical logbook of an online group music player
* playback_history
	* The history of played tracks of an online group music player
* recommendations
	* A huge table (>100 million rows) containing predictions of items (e.g. tracks, artists) to users based on algorithms described in [Master Thesis](https://research.tue.nl/en/studentTheses/evaluating-a-framework-for-sequential-group-music-recommendations).
* top
	* Top tracks and artists for anonymous Spotify users
* track_artists
	* Links tracks to their artists
* tracks
	* Contains data on the tracks.
	
### Data format

The data is exported to a tab delimited *.txt file. The structure of the data is available in *.sql files. You can open the sql files in a text editor program such as notepad to learn more about the fields in the tables. The tables contain a maximum of 10,000 rows, but more is available on request.

### Importing to Stata

The data can be imported to Stata. An example import file is created to show how this can be done:

```
import.do
```

And the result of this import is:

```
import.result.dta
```
The *.do file can be openened in Stata and contains additional information about the import procedure.

## Online user rating study

This dataset is data contained from an online study in which participants provided user ratings of tracks. The tracks were predicted based on varying algorithms to match the preferences of the participants. Tracks were rated on three occasions in three playlists. The attractiveness and diversity of the playlists was measured as well. For a more detailed overview of the study please refer to [Master Thesis](https://research.tue.nl/en/studentTheses/evaluating-a-framework-for-sequential-group-music-recommendations). 

### Data format

The data is present in both raw and processed forms:

#### Raw

* participants.csv
	* Each row corresponds to a study session. Each session contained one participant. The order of the conditions and the answers to the questionnaires are present in columns. Answers to questionnaires are encoded in [JSON format](https://nl.wikipedia.org/wiki/JSON).
* user_ratings.csv
	* Each row corresponds to a single user rating of a track. Contains data on the predicted rating, position in the playlist, condition, audio features. _rating_id_ is zero for the user ratings (how much they liked the tracks) and one for the personalization rating (whether they thought the track matched their preferences).

#### Processed

* spotifystudy
	* Present in both long and wide format. All aggregate scores are calculated (i.e. music sophistication index) and both user ratings and questionnaire answers are combined in one table. Incomplete submissions are removed.

## Authors

* **Sophia Hadash** - [SophiaHadash](https://github.com/SophiaHadash)