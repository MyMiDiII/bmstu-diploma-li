Через пакетный менеджер установить:

```
python3
sqlite3
```

```
pip3 install -r requirements.txt
```

```
cd data
python3 generate.py
cd ..
```

```
cd sqlite
make
sqlite3 test.db
```

```
.load ./lindex
create virtual table hoba using lindex(keys INTEGER);
drop table hoba;
.mode csv
.import <path_to_csv> rhoba;
create virtual table hoba using lindex(keys INTEGER);
select * from hoba where keys = <key>;
```

Если не находит модули:
```
export PYTHONPATH=<path_to_repo_src_dir>:$PYTHONPATH
```

Время запроса:
```
.timer on
```


