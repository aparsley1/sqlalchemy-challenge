# Import the dependencies.
from  flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    prev_last_date = dt.date(one_year.year, one_year.month, one_year.day)

    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_last_date).order_by(Measurement.date.desc()).all()
    session.close()

    prcp_list = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["date"] =  date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    result = session.query(Station.station, Station.name).all()
    session.close()

    station_list = list(np.ravel(result))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    result = session.query(Measurement.date,  Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    session.close()

    tobs_list = []
    for date, tobs in  result:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def get_temp_start(start):
    session = Session(engine)

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temps_list = []
    for min_temp,  avg_temp, max_temp in  result:
        temps_dict = {}
        temps_dict["minimum temperature"] = min_temp
        temps_dict["average temperature"] = avg_temp
        temps_dict["maximum temperature"] = max_temp
        temps_list.append(temps_dict)

    return jsonify(temps_list)


@app.route("/api/v1.0/<start>/<end>")
def get_temp_start_end(start, end):
    session = Session(engine)

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps_list = []
    for min_temp,  avg_temp, max_temp in  result:
        temps_dict = {}
        temps_dict["minimum temperature"] = min_temp
        temps_dict["average temperature"] = avg_temp
        temps_dict["maximum temperature"] = max_temp
        temps_list.append(temps_dict)

    return jsonify(temps_list)



if __name__ == '__main__':
    app.run(debug=True)

