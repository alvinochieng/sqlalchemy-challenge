import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

postgresStr = ("postgresql://postgres:password@localhost:5432/climate")
engine = create_engine(postgresStr)

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (f"Available routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start_date<br/>"
           f"/api/v1.0/start_end_date<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    result_dict = []
    
    for date, precipitation in results:
        data_dict={}
        data_dict["prcp"] = precipitation
        data_dict["date"] = date
        result_dict.append(data_dict)
    
    result_dict_list = list(np.ravel(result_dict))
    
    return jsonify(result_dict_list)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    stations_json = session.query(Station.name).all()
    
    session.close()
    
    stations_dict_list = list(np.ravel(stations_json))
    
    return jsonify(stations_dict_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    tobs_list = list(np.ravel(tobs_data))
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_date")
def start_date():
    
    session = Session(engine)
    
    start_data = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), 
                               func.avg(Measurement.tobs) ).\
    filter(Measurement.date >= '2016-08-23').\
    group_by(Measurement.date).all()
    
    start_data_list = list(np.ravel(start_data))
    
    session.close()
    
    tmp_data = []
    
    for tmp_date, tmp_min, tmp_max, tmp_avg in start_data:
        tmp_dict = {}
        tmp_dict["date"] = tmp_date
        tmp_dict["Min temp"] = tmp_min
        tmp_dict["Max temp"] = tmp_max
        tmp_dict["Avg temp"] = int(tmp_avg)
        tmp_data.append(tmp_dict)
                               
    return jsonify(tmp_data)

@app.route("/api/v1.0/start_end_date")
def start_to_end_date():
    
    session = Session(engine)
    
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),
                                  func.avg(Measurement.tobs) ).\
    filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').\
    group_by(Measurement.date).all()
    
    start_end_list = list(np.ravel(start_end_date))
    
    session.close()
    
    start_end_data = []
    
    for dte, tmin, tmax, tavg in start_end_date:
        ste_dict = {}
        ste_dict["date"] = dte
        ste_dict["min temp"] = tmin
        ste_dict["max temp"] = tmax
        ste_dict["avg temp"] = int(tavg)
        start_end_data.append(ste_dict)
        
        return jsonify(start_end_data)
    
if __name__ == '__main__':
    app.run(debug=True)
    