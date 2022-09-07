# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 15:55:15 2019

@author: ecallahan
https://github.com/ecallahan573
https://www.cteh.com/

srt2shp is licensed under the
GNU General Public License v3.0

Parses SRT files produced by DJI drones when recording video. Converts data into an excel spreadsheet and ESRI shapefiles (Points and Lines)

Compatible with Python 3.x
"""

import pandas as pd
from glob import glob
from datetime import datetime
import shapefile as shp
import os


class SRTReader():
    """
    Converts DJI SRT files into an excel spreadsheet, point shapefile,
    and line shapefile.
    """
    
    def process(self, files=[]):
        """
        Searches script directory for DJI SRT files for parsing.  Saves SRT conctents to excel spreadsheet, shapefiles, and returnds Pandas dataframe.
        ----
        
        files : array, Default None
            List of file paths to process
        """
        
        self.export_folder = os.path.join(os.getcwd(), 'Converted Files')
        
        if not os.path.isdir(self.export_folder): # Check if export folder exists and create it if does not
            os.mkdir(self.export_folder)
        
        if files == []:
            files = glob('*.srt') # Search script directory for dji srt files
        
        for filename in files:
            
            print(f'Reading {filename!s}...')
            
            with open(filename,'r') as srt:
                srtfile = srt.read()
            
            records = srtfile.split('\n\n')
            
            dicts = []
            
            for record in records:
                data = {}
                rows = record.split('\n')
                
                if len(rows[0]) != 0:
            
                    g = rows[3][rows[3].find('(')+1:rows[3].find(')')].split(',')
                    
                    data['id'] = int(rows[0])
                    data['time'] = datetime.strptime(rows[2][-19:].replace('.','-'), '%Y-%m-%d %H:%M:%S')
                    data['home_gps'] = rows[2]
                    data['gps'] = rows[3]
                    data['lat'] = float(g[1])
                    data['lng'] = float(g[0])
                    data['camera'] = rows[4]
                    data['file'] = filename
                    
                    dicts.append(data)
            
            df = pd.DataFrame.from_dict(dicts)
            
            self.create_shps(df)
            
            excel_file = f'{filename!s}.xlsx'
            
            print(f'Creating {excel_file!s}...')

            df.to_excel(os.path.join(self.export_folder, excel_file),index=False)
            
            del dicts
            
            input('\nProcessing complete.  Press ENTER to close.')
            
        return df
    
    def fieldnames(self, dataframe):
        """
        Returns list of field names from input dataframe.
        ----
        
        dataframe : dataframe
            Pandas dataframe
        """
        
        fields = dataframe.keys().values
        
        return fields
    
    def getWKT_PRJ(self, filename, epsg_code):
        """
        Creates prj file with output from spatialreference.org.
        ----
        
        filename : str
            Filename of shapefile (without file extension).
        epsg_code : str or int
            EPSG code of desired spatial reference
        """
        
        import urllib.request
    
        wkt = urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
        projection = wkt.read().decode('utf-8').replace(" ","").replace("\n", "")
    
        with open(os.path.join(self.export_folder, filename + '.prj'),'w') as prjfile:
            prjfile.write(projection)
        
        return projection
        
    def create_shps(self, dataframe):
        """
        Creates point and line shapfiles from parsed SRT file.
        ----
        
        dataframe : dataframe
            Parsed SRT data from output of process_srt() function.
        """
        
        # Generate line shapefile
        d = dataframe.to_dict(orient='records')
        filename_path = os.path.join(self.export_folder, d[0]['file'].replace('.SRT','_flightpath'))
        filename_points = os.path.join(self.export_folder, d[0]['file'].replace('.SRT','_points'))
        
        print(f'Creating shapefile {filename_path!s}.shp')
        w = shp.Writer(filename_path)
        
        w.field('filename', 'C')
        w.field('start_time','C')
        
        lats = []
        
        for each in d:
            lats.append([each['lng'],each['lat']])
            
        w.line([lats])
        w.record(d[0]['file'],d[0]['time'])
        self.getWKT_PRJ(filename_path,4326)
        
        w.close()
        
        # Generate point shapefile 
        print(f'Creating shapefile {filename_points!s}.shp')
        p = shp.Writer(filename_points)
        
        cols = self.fieldnames(dataframe)
        
        # Generate columns for shapefile dbf
        for col in cols:
            if col in ('lat','lng','id'):
                p.field(col,'F')
            else:
                p.field(col,'C', '255')
            
        for point in d:
            p.point(point['lng'],point['lat']) # Y and X coordinate of point
            p.record(point['id'],point['time'],point['home_gps'], point['gps'], point['lat'], point['lng'], point['camera'], point['file']) # Populate dbf
        
        self.getWKT_PRJ(filename_points,4326)
       
        p.close()

if __name__ == '__main__':
    srt = SRTReader()        
        
    df = srt.process()
