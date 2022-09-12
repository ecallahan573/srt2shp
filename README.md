# srt2shp
Parses multiple SRT files produced by DJI drones when recording video.  Converts data into an excel spreadsheet and ESRI shapefiles (Points and Lines).

A demo.srt file is included for testing.

# Install
 ~~~
 pip install srt2shp
 ~~~

# Build from Source (Optional)

1. Install python if you don't already have it (https://www.python.org/downloads/)

2. Open a terminal or command prompt and navigate the the folder where the project is saved. 

3. Create a virtual environment:
~~~~
python -m venv srtvenv
~~~~

4. Activate the virutal environment
~~~~
\srtvenv\Scripts\activate
~~~~

5. Make sure you have the latest version of PyPA’s build installed:
~~~~
python -m pip install --upgrade build
~~~~

6. Build the project:
~~~~
python -m build
~~~~

7. Install the project wheel
~~~
pip install .\dist\srt2shp-0.0.1-py3-none-any.whl
~~~

# Run the Script
1. Place the SRT files you would like to process in the directory where the srt2shp.py file is saved.

2. Run the srtConvert.py script:
~~~~
python srtConvert.py
~~~~

3. Files will be saved in the "Converted Files" folder where the script was executed.
