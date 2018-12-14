from flask import Flask,render_template,request,json,redirect,jsonify
from geojson import LineString, Feature, dump, FeatureCollection
from app import app
from pathlib import Path
from collections import Counter
from app.functions import is_number
from app.functions import findMatch
import geojson
import json
import csv

@app.route('/getTurf', methods=['POST'])
def getTurf():
    req_data = request.get_json()
    lines = []
    with open('input/line.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if ((is_number(row['latitude1']) and is_number(row['longitude1']) and is_number(row['latitude2']) and is_number(row['longitude2'])) and ((row['latitude1'] != row['latitude2']) and (row['longitude1'] != row['longitude2']))):
                flres = findMatch(row['latitude1'],row['longitude1'],row['latitude2'],row['longitude2'],req_data)
                foo = flres.split(", ")
                if len(foo) == 4:
                    line = LineString([(float(foo[1]), float(foo[0])), (float(foo[3]), float(foo[2]))]) 
                else:
                    line = LineString([(float(foo[1]), float(foo[0])), (float(foo[3]), float(foo[2])), (float(foo[5]), float(foo[4])), (float(foo[7]), float(foo[6]))])
                linejson = Feature(name="cv"+row['trail_id'], geometry=line, style={"color": "#ff46b5", "weight": 10,"opacity": 0.85}, properties={"direction":row['direction'], "source":row['source'], "sink":row['sink'], "level":row['level'], "power":int(row['power'])})
                lines.append(linejson)

        feature_collection = FeatureCollection(lines)

    # populate file to confirm content 
    with open('output/offset_output.geojson', 'w') as f:
        dump(feature_collection, f)

    return "GeoJSON dump complete!"

@app.route('/')
def geojson_out():
    unique = []
    with open('input/line.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # ensure coordinates are numeric and start and end points are not identical
            if ((is_number(row['latitude1']) and is_number(row['longitude1']) and is_number(row['latitude2']) and is_number(row['longitude2'])) and ((row['latitude1'] != row['latitude2']) and (row['longitude1'] != row['longitude2']))):
                unique.append(row['latitude1'] + "," + row['longitude1'] + "," + row['latitude2'] + "," + row['longitude2'])

    # get unique values and associated count from unique list
    res = Counter(unique)

    output = str(res)[8:-1].replace("'", "\"")
    d = json.loads(output)
    return render_template("preprocess.html", user=d)

@app.route('/checkGeo', methods=['POST'])
def checkGeo():
    my_file = Path("output/offset_output.geojson")
    if my_file.is_file():
        return "1"
    else:
        return "0"

@app.route('/getGeoj')
def getGeoj():
    with open('output/offset_output.geojson') as f:
    	data = json.load(f)

    return render_template("map.html", user=data)