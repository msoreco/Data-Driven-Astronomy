# Adding stars
insert into Star (kepler_id, t_eff, radius)
values
(7115384, 3789, 27.384),
(8106973, 5810, 0.811),
(9391817, 6200, 0.958);

# Misc (messed up table task)
delete from Planet where radius < 0;
update Planet set kepler_name = NULL where status != 'CONFIRMED';

# Create own table
create table Planet (
  kepler_id INTEGER NOT NULL,
  koi_name VARCHAR(15) UNIQUE NOT NULL,
  kepler_name VARCHAR(15),
  status VARCHAR(20) NOT NULL,
  radius FLOAT NOT NULL
);

insert into Planet (kepler_id, koi_name, kepler_name, status, radius)
values
(6862328, 'K00865.01', NULL, 'CANDIDATE', 119.021),
(10187017, 'K00082.05', 'Kepler-102 b', 'CONFIRMED', 5.286),
(10187017, 'K00082.04', 'Kepler-102 c', 'CONFIRMED', 7.071);

# Create tables incl keys
CREATE TABLE Star (
  kepler_id INTEGER PRIMARY KEY,
  t_eff INTEGER NOT NULL,
  radius FLOAT NOT NULL
);

create table Planet (
  kepler_id INTEGER REFERENCES Star(kepler_id),
  koi_name VARCHAR(20) PRIMARY KEY,
  kepler_name VARCHAR(20),
  status VARCHAR(20) NOT NULL,
  period FLOAT,
  radius FLOAT,
  t_eq INTEGER
);

copy Star from 'stars.csv' CSV;
copy Planet from 'planets.csv' CSV;

\d Star;
\d Planet;

# Add columns then load from CSV
alter table Star add column ra FLOAT;
alter table Star add column decl FLOAT;
delete from Star;
copy Star from 'stars_full.csv' CSV;
