$ sqlite3 test.db
sqlite> .load ./lindex
sqlite> create table maps(keys INTEGER);
sqlite> .mode csv
sqlite> .import osm1000.csv maps
sqlite> create virtual table virtmaps using lindex(0, fcnn2);
Epoch 1/30
1000/1000 [====================] - 1s 768us/step - loss: 0.0011
...
sqlite> select * from virtmaps where keys = 232131750;
keys
232131750
