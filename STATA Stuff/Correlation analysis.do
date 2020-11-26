clear all
set more off

// import the data from the csv file
import delimited "stata_data.csv"

// preprocess the v1 (year) variable to be an integer
replace v1 = "1999" in 1
replace v1 = "2000" in 2
replace v1 = "2001" in 3
replace v1 = "2002" in 4
replace v1 = "2003" in 5
replace v1 = "2004" in 6
replace v1 = "2005" in 7
replace v1 = "2006" in 8
replace v1 = "2007" in 9
replace v1 = "2008" in 10
replace v1 = "2009" in 11
replace v1 = "2010" in 12
replace v1 = "2011" in 13
replace v1 = "2012" in 14
replace v1 = "2013" in 15
replace v1 = "2014" in 16
replace v1 = "2015" in 17
replace v1 = "2016" in 18
replace v1 = "2017" in 19
replace v1 = "2018" in 20
destring v1, replace

// show some stats
codebook, compact

// do the analysis
asdoc pwcorr v1 acousticness danceability duration_ms energy instrumentalness loudness speechiness valence year tempo liveness, sig star(5) save(correlation_matrix.doc)
