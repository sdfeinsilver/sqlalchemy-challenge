#Import Numpy, Pandas, and Datetime Libraries
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#Import Flask
from flask import Flask, jsonify

# create path to hawaii sqlite database
hawaii_path = "Resources/hawaii.sqlite"

# create engine and connection to hawaii.sqlite
engine = create_engine(f"sqlite:///{hawaii_path}")
conn = engine.connect()

#Declare a base using autobase_map
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

###################################################################

#Flask Code - Beginning
app = Flask(__name__)

#Home Page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

#Precipitation Page
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return Precipitation Data for last year"""
    
    #Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Find date 1 year prior to most recent date
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Query for the date and precipitation for the last year
    prec_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago_date).all()
    
    #Close the session
    session.close()
    
    #Convert list of tuples into normal list
    prec_data_json = list(np.ravel(prec_data))
    
    #Return and Jsonify precipitation data
    return jsonify(prec_data_json)

#Stations Page
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""

    #Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the list of stations
    list_of_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    #Close the session
    session.close()

    #Convert list of tuples into normal list
    list_of_stations_json = list(np.ravel(list_of_stations))
    
    #Return and Jsonify List of Stations
    return jsonify(list_of_stations_json)

#Tobs Page
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs for the previous year"""

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Find date 1 year prior to most recent date
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #Query the dates and temperature observations of the most active station for the last year of data
    temp_data_12mos = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= year_ago_date).all()

    #Close the session
    session.close()

    #Convert list of tuples into normal list
    temp_data_12mos_json = list(np.ravel(temp_data_12mos))
    
    #Return and Jsonify Tobs for past year
    return jsonify(temp_data_12mos_json)

#Date Page - Need to study!


#Flask Code - Ending
if __name__ == '__main__':
    app.run()






