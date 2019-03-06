# srt2shp
Parses SRT files produced by DJI drones when recording video.  Converts data into an excel spreadsheet and ESRI shapefiles (Points and Lines).

A demo.srt file is included for testing.

# Instructions

1. Install python if you don't already have it (https://www.python.org/downloads/)

2. Open a terminal or command prompt and navigate the the folder wher the requirements.txt file is saved. 
Install required python libraries using the requirements.txt file.
~~~~
pip install -r requirements.txt
~~~~

3. Place the SRT files you would like to process in the directory where the srt2shp.py file is saved.

4. Run the srt2shp.py script.
~~~~
python srt2shp.py
~~~~

5. Files will be saved in the "Converted Files" folder where the script was executed.