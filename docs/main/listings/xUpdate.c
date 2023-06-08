int lindexUpdate(sqlite3_vtab *pVTab,
                 int argc, sqlite3_value **argv,
                 sqlite_int64 *pRowid) {
    if (!(argc > 1 && sqlite3_value_type(argv[0]) == SQLITE_NULL))
        return SQLITE_CONSTRAINT;

    lindex_vtab *lTab = (lindex_vtab*)pVTab;
    sqlite3 *db = lTab->db;
    int64_t column = sqlite3_value_int64(argv[2]);
    char *query = sqlite3_mprintf("INSERT INTO maps VALUES(%d);", column);
    sqlite3_exec(db, query, 0, 0, 0);
    sqlite3_int64 lastRowID = sqlite3_last_insert_rowid(db);

    PyObject* insert = PyUnicode_FromString("insert");
    PyObject* key = PyLong_FromLongLong(column);
    PyObject* data = PyLong_FromLongLong(lastRowID);

    PyObject_CallMethodObjArgs(lTab->lindex, insert, key, data, NULL);

    return SQLITE_OK;
}
