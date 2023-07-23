int lindexFilter(sqlite3_vtab_cursor *cur,
                 int idxNum,
                 const char *idxStr,
                 int argc,
                 sqlite3_value **argv)
{
    import_array()
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyObject* keys = PyList_New(0);
    PyList_Append(keys, PyLong_FromLong(sqlite3_value_int(argv[i])));

    PyObject* find = PyUnicode_FromString("find");
    PyObject* rowids = PyObject_CallMethodObjArgs(lTab->lindex, find, keys, NULL);
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
