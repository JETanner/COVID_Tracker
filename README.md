# COVID_Tracker
This is a data presenter (can retrieve data from John Hopkins DataSet) and compartmental model (MSEIRS) for COVID-19

I am not a medical doctor nor am I an epidemiologist so I would treat the model as Naive. 
I am a physicist (PhD candidate) who does work with exponential growth so it is not complete rubbish,
but it is still not my main work and I already recognoize several simplifications and major guesses in it.

This program has a self installer for all needed dependencies and a GUI so should be fairly straightforward to use.
It is however mostly cobbled together from other modules I have written so there are still many bugs to work out.

Needs:
-installed version of python* installed : https://www.python.org/ 

Works on:
-Windows
-Linux   (likely - not yet fully tested)
-Android (with PyDroid and built in version of PIP used to get matplotlib)

Notes:
-To operate you only need the .pyw file but the "WIP" text file holds all the previous data:
  -Prevsiously downloaded data
  -Saved model variables 
  -Open tabs
-Retrieve data button checks if data exists already and adds only latest dates
-Included estimates for variables are rough but have been looked up
-Saved Graphs are saved just by page number for now
-If it fails to graph (or update graph) it usually means there is a variable number that has caused a problem (such as a 0 in divisor)
-Small compartment sizes quickly increase the run time but are necessary to calculate capacity limit effects and healthcare overrun
-Compartment growth is a bit more naive then most (simplified version of regular growth)
-Some changes cause auto regraphs

Known Issues:
-States still seem to need fixing on the data side since John Hopkins changed their data format on 3/23/2020
-No way to delete old data individually yet



*if Anaconda is installed, careful about PATH settings or run in Juypter notebook
