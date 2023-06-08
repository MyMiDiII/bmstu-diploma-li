$ sqlite3 test.db
sqlite> .load ./lindex
sqlite> create table maps(key INTEGER UNIQUE);
sqlite> .mode csv
sqlite> .import osm10.csv maps
sqlite> select * from maps;
5694768947
1000
4577603404
8742104813
2577217863
3465205493
10920113439
814309230
6943212874
1766254734
sqlite> create virtual table virtmaps using lindex(1, fcnn2);
Epoch [1/30], Loss: 1.963e-01
...
sqlite> select * from virtmaps where key = 3465205493;
3465205493
sqlite> select * from virtmaps where key > 3465205493;
4577603404
5694768947
6943212874
8742104813
10920113439
sqlite> select * from virtmaps where key < 3465205493;
1000
814309230
1766254734
2577217863
sqlite> select * from virtmaps where key <= 3465205493;
1000
814309230
1766254734
2577217863
3465205493
sqlite> select * from virtmaps where key >= 3465205493;
3465205493
4577603404
5694768947
6943212874
8742104813
10920113439
sqlite> select * from virtmaps where key between 3465205493 and 5694768947 ;
3465205493
4577603404
5694768947
sqlite> insert into virtmaps values(1);
Epoch [1/30], Loss: 5.933e-02
...
sqlite> select * from virtmaps where key = 1;
1
