# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Define the home page route
@app.route("/")
def home():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    # Calculate the date 1 year ago from the last data point in the database
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()
    #End Session
    session.close()  
    # Return the JSON representation of your dictionary.
    all_precipitation = []
    for date, prcp in precipitation:
        precipitation_dict = {}
        precipitation_dict[date] = prcp 
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)


# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    
    # Query all stations
    results = session.query(Station.station).all()
    #End Session
    session.close()

    # Return a JSON list of stations from the dataset.
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():

# Query the dates and temperature observations of the most-active station for the previous year of data.
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        all()
    #End Session
    session.close()

    # Return a JSON list of temperature observations for the previous year.

    all_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

# Define the start and start_end route
@app.route("/api/v1.0/<start>")
@app.route('/api/v1.0/<start>/<end>')
def start_end(start=None, end=None):
    
    # Query all temperature observations
    if not end:
        temp_data = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

        all_temps = list(np.ravel(temp_data))
        return jsonify(all_temps)
    
    temp_data = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_temps = list(np.ravel(temp_data))
    return jsonify(all_temps)

#End Session
session.close()   

if __name__ == '__main__':
    app.run(debug=True)
