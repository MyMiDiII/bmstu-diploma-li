int initPythonIndex(sqlite3 *db,
                    const char *const tableName,
                    const char *const modelName,
                    lindex_vtab *vTab) {
    char* query = sqlite3_mprintf("SELECT ROWID, * FROM %s", tableName);

    sqlite3_stmt* stmt;
    sqlite3_prepare_v2(db, query, -1, &stmt, NULL);
    sqlite3_free(query);

    PyObject* builderModule = PyImport_ImportModule("indexes.builder");
    PyObject* builderClassName = PyObject_GetAttrString(builderModule, "LindexBuilder");
    PyObject* pyModelName = PyTuple_Pack(1, PyUnicode_FromString(modelName));
    PyObject* builder = PyObject_CallObject(builderClassName, pyModelName);
    PyObject* lindex = PyObject_CallMethod(builder, "build", NULL);
    PyObject* keys = PyList_New(0);
    PyObject* rows = PyList_New(0);

    int i = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int key = sqlite3_column_int(stmt, 1);
        int64_t rowid = sqlite3_column_int64(stmt, 0);

        PyList_Append(keys, PyLong_FromLong(key));
        PyList_Append(rows, PyLong_FromLong(rowid));

        i++;
    }

    if (i) {
        PyObject* train = PyUnicode_FromString("train");
        PyObject* check = PyObject_CallMethodObjArgs(lindex, train, keys, rows, NULL);
        Py_DECREF(check);
        Py_DECREF(train);
    }

    vTab->lindex = lindex;
    vTab->db = db;

    Py_DECREF(keys);
    /* ... */
    sqlite3_finalize(stmt);

    return SQLITE_OK;
}

