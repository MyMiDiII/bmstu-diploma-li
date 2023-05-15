#include <Python.h>

#include "vtable.h"
#include "queries.h"
#include "sqlite_api.h"

int lindexCreate(sqlite3 *db,
                 void *pAux,
                 const int argc,
                 const char *const *argv,
                 sqlite3_vtab **ppVtab,
                 char **errMsg)
{
    Py_Initialize();
    PyRun_SimpleString("print('Hello, Python!')");
    Py_Finalize();
    //puts("CREATE");
    lindex_vtab *vtab = sqlite3_malloc(sizeof(lindex_vtab));

    if (!vtab)
        return SQLITE_NOMEM;

    memset(vtab, 0, sizeof(*vtab));
    *ppVtab = &vtab->base;

    char *sql_template = get_create_table_query_by_args(argc, argv);

    const char *vTableName = argv[2];
    const char *rTableName = sqlite3_mprintf("r%s", vTableName);

    char *vSqlQuery = sqlite3_mprintf(sql_template, vTableName);
    char *rSqlQuery = sqlite3_mprintf(sql_template, rTableName);

    //puts(vSqlQuery);
    //puts(rSqlQuery);

    int rc = sqlite3_declare_vtab(db, vSqlQuery);

    if (!rc)
        rc = sqlite3_exec(db, rSqlQuery, NULL, NULL, errMsg);

    sqlite3_free(sql_template);
    sqlite3_free(vSqlQuery);
    sqlite3_free(rSqlQuery);

    char* query = sqlite3_mprintf("SELECT ROWID, * FROM %s", rTableName);

    sqlite3_stmt* stmt;
    rc = sqlite3_prepare_v2(db, query, -1, &stmt, NULL);

    vtab->number = 0;

    int i = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW)
    {
        if (i != 1)
        {
            int64_t rowid = sqlite3_column_int64(stmt, 0);
            //printf("rowid %ld\n", rowid);
            vtab->values[vtab->number] = rowid;

            int key = sqlite3_column_int(stmt, 1);
            //printf("key %d\n", key);
            vtab->keys[vtab->number] = key;

            vtab->number++;
        }
        i++;
    }

    char* result_query = sqlite3_mprintf("SELECT * FROM %s WHERE ROWID = ?;", rTableName);
    sqlite3_prepare_v2(db, result_query, -1, &vtab->stmt, NULL);

    return rc;
}

int lindexConnect(sqlite3 *db,
                  void *pAux,
                  int argc,
                  const char *const *argv,
                  sqlite3_vtab **ppVtab,
                  char **pzErr)
{
    //puts("CONNECT");
    for (int i = 0; i < argc; ++i)
    {
        //printf("%d %s\n", i, argv[i]);
    }

    return lindexCreate(db, pAux, argc, argv, ppVtab, pzErr);
}

int lindexDisconnect(sqlite3_vtab *pVtab)
{
    //puts("DISCONNECT";
    lindex_vtab *p = (lindex_vtab*)pVtab;
    //puts("free");
    sqlite3_free(p);
    //puts("ok");
    return SQLITE_OK;
}
