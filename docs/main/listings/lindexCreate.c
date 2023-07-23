int lindexCreate(sqlite3 *db, void *pAux,
                 const int argc, const char *const *argv,
                 sqlite3_vtab **ppVtab, char **errMsg)
{
    lindex_vtab *vtab = sqlite3_malloc(sizeof(lindex_vtab));

    memset(vtab, 0, sizeof(*vtab));
    *ppVtab = &vtab->base;

    const char *vTableName = argv[2];
    const char *rTableName = vTableName + 4;

    char *sql_template = "SELECT sql FROM sqlite_master WHERE type='table' AND name='%s';";
    char *schemaQuery = sqlite3_mprintf(sql_template, rTableName);

    char* messaggeError;
    char vSqlQuery[10000];
    strcpy(vSqlQuery, vTableName);
    sqlite3_exec(db, schemaQuery, callback, vSqlQuery, &messaggeError);
    char *resVSqlQuery = sqlite3_mprintf("%s;", vSqlQuery);

    sqlite3_declare_vtab(db, resVSqlQuery);

    sqlite3_free(schemaQuery);
    sqlite3_free(resVSqlQuery);

    long column_index = strtol(argv[3], NULL, 10);
    const char *model = argv[4];

    initPythonIndex(db, rTableName, model, column_index, vtab);

    char* result_query = sqlite3_mprintf("SELECT * FROM %s WHERE ROWID = ?;", rTableName);
    sqlite3_prepare_v2(db, result_query, -1, &vtab->stmt, NULL);

    return SQLITE_OK;
}
