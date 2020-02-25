import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


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
           f"/api/v1.0/<start><br/>"
           f"/api/v1.0/<start>/<end><br/>")

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
    
    return jsonify(result_dict)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    stations_json = session.query(Station.station, Station.name).all()
    
    session.close()
    
    return jsonify(stations_json)
    
if __name__ == '__main__':
    app.run(debug=True)
    