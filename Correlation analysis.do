clear all 
set more off

cd "E:\Users\Wardw\Mijn documenten\GitHub\spotify_project"

use stata_datav2

codebook, compact

pwcorr v1 acousticness danceability duration_ms energy instrumentalness loudness speechiness valence year, sig star(5)
