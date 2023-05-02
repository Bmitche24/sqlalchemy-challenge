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
print(precipitation)