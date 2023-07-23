create table maps(key INTEGER UNIQUE);
.mode csv
.import osm10.csv maps
select * from maps;
