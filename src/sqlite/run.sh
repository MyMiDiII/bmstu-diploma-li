rm *.db
export PYTHONPATH=/home/mymidi/Desktop/BMSTU/bmstu-diploma-li/src:$PYTHONPATH

echo "Инициализация данных"

sqlite3 -echo test.db < init.sql

sleep 2

echo "Проверка работы индекса"

sqlite3 -echo test.db < lindex.sql

printf '\e[3J'

sleep 4
