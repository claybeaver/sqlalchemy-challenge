import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

################
# Database Setup
################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#############
# Flask Setup
#############
app = Flask(__name__)

##############
# Flask Routes
##############
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2012-02-28<br/>"
        f"/api/v1.0/2012-02-28/2012-03-05"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of precipitation data including the date and precipitation level"""
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations from the dataset"""
    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a list of temperature observations (TOBS) for the previous year"""
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()
    session.close()

    year_tobs = list(np.ravel(results))

    return jsonify(year_tobs)


@app.route("/api/v1.0/2012-02-28")
def calc_temps():
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start time forward."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= '2012-02-28').all()
    session.close()

    start_on = list(np.ravel(results))

    return jsonify(start_on)


@app.route("/api/v1.0/2012-02-28/2012-03-05")
def calc_temps_all():
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= '2012-02-28').\
    filter(Measurement.date <= '2012-03-05').all()
    session.close()

    start_to_end = list(np.ravel(results))

    return jsonify(start_to_end)
    

if __name__ == '__main__':
    app.run(debug=True)
