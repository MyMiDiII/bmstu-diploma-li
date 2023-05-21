typedef struct lindex_vtab {
    sqlite3_vtab base;  /* основа виртуальной таблицы */
    sqlite3_stmt *stmt; /* инструкция доступа к записи по ROWID*/
    PyObject *lindex;   /* собственно объект индекса */
} lindex_vtab;

typedef struct lindex_cursor {
    sqlite3_vtab_cursor base; /* базовая структура курсора */
    PyObject *rowids;         /* массив выбранных ROWID */
    PyArrayIterObject *iter;  /* итератор по массиву ROWID */
} lindex_cursor;

