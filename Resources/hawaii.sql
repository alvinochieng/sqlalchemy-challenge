CREATE TABLE measurements(
	ID SERIAL PRIMARY KEY NOT NULL,
	station VARCHAR(255) NOT NULL,
	date VARCHAR(255) NOT NULL,
	prcp FLOAT,
	tobs INT,
	FOREIGN KEY(station) REFERENCES station(station)
); 