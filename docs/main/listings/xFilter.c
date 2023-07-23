int lindexFilter(sqlite3_vtab_cursor *cur, int idxNum,
                 const char *idxStr, int argc,
                 sqlite3_value **argv) {
    import_array()
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyObject* keys = PyList_New(0);

    for (int i = 0; i < argc; ++i) {
        int64_t value = (int64_t)sqlite3_value_int64(argv[i]);
        PyList_Append(keys, PyLong_FromLong(value));
    }

    PyObject* tuple_rowids;

    if (!idxNum) {
        PyObject* find = PyUnicode_FromString("find");
        tuple_rowids = PyObject_CallMethodObjArgs(lTab->lindex, find, keys, NULL);
    }
    else {
        PyObject* constraints = PyList_New(0);
        PyObject* noneObj = Py_None;

        for (int i = 0; i < argc; ++i) {
            PyList_Append(constraints, PyLong_FromLong(idxNum % 10));
        }

        if (idxNum / 10 != 3) {
            Py_INCREF(noneObj);
            PyList_Insert(keys, idxNum / 10 % 2, noneObj);

            Py_INCREF(noneObj);
            PyList_Insert(constraints, idxNum / 10 % 2, noneObj);
        }

        PyObject* prange= PyUnicode_FromString("predict_range");
        tuple_rowids = PyObject_CallMethodObjArgs(lTab->lindex, prange,
                keys, constraints, NULL);
    }

    PyObject* rowids;

    int tmp;
    PyArg_ParseTuple(tuple_rowids, "Oi", &rowids, &tmp);
    npy_intp size = PyArray_SIZE(rowids);
    PyArrayIterObject *iter = (PyArrayIterObject *)PyArray_IterNew(rowids);

    lindex_cursor *pCur = (lindex_cursor*)cur;
    pCur->rowids = rowids;
    pCur->iter = iter;

    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);

    return SQLITE_OK;
}
