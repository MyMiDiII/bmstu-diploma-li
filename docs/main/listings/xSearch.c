int lindexNext(sqlite3_vtab_cursor *cur) {
    lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyArray_ITER_NEXT(pCur->iter);

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);

    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);

    return SQLITE_OK;
}

int lindexColumn(sqlite3_vtab_cursor *cur,
                 sqlite3_context *ctx,
                 int i)
{
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;
    int64_t columnValue = sqlite3_column_int64(lTab->stmt, i);
    sqlite3_result_int64(ctx, columnValue);

    return SQLITE_OK;
}

int lindexEof(sqlite3_vtab_cursor *cur)
{
    lindex_cursor *pCur = (lindex_cursor*)cur;
    return !PyArray_ITER_NOTDONE(pCur->iter);
}
