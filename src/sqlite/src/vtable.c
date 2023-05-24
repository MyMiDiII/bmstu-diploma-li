#include <Python.h>

#include "vtable.h"
#include "queries.h"
#include "sqlite_api.h"

int initPythonIndex(sqlite3 *db,
                    const char *const tableName,
                    const char *const modelName,
                    const int column_index,
                    lindex_vtab *vTab)
{
    puts("CREATE");
    char* query = sqlite3_mprintf("SELECT ROWID, * FROM %s", tableName);

    puts("CREATE");
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, query, -1, &stmt, NULL);
    sqlite3_free(query);

    puts("CREATE");
    if (rc)
        return rc;

    PyObject* builderModule = PyImport_ImportModule("indexes.builder");
    if (!builderModule)
    {
        PyErr_Print();
        PyErr_Clear();
    }
    printf("%p\n", (void *)builderModule);
    
    PyObject* builderClassName = PyObject_GetAttrString(builderModule, "LindexBuilder");
    printf("%p\n", (void *)builderClassName);
    PyObject* pyModelName = PyTuple_Pack(1, PyUnicode_FromString(modelName));
    PyObject* builder = PyObject_CallObject(builderClassName, pyModelName);
    printf("%p\n", (void *)builder);

    PyObject* lindex = PyObject_CallMethod(builder, "build", NULL);
    PyObject* keys = PyList_New(0);
    PyObject* rows = PyList_New(0);

    int i = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW)
    {
        int key = sqlite3_column_int(stmt, column_index);
        int64_t rowid = sqlite3_column_int64(stmt, 0);

        PyList_Append(keys, PyLong_FromLong(key));
        PyList_Append(rows, PyLong_FromLong(rowid));

        i++;
    }
    puts("ok");

    if (i)
    {
        puts("train");
        PyObject* train = PyUnicode_FromString("train");
        if (!train)
        {
            PyErr_Print();
            PyErr_Clear();
        }

        PyObject* check = PyObject_CallMethodObjArgs(lindex, train, keys, rows, NULL);
        if (!check)
        {
            PyErr_Print();
            PyErr_Clear();
        }

        Py_DECREF(check);
        Py_DECREF(train);
    }

    vTab->lindex = lindex;

    Py_DECREF(keys);
    Py_DECREF(rows);
    Py_DECREF(builder);
    Py_DECREF(pyModelName);
    Py_DECREF(builderClassName);
    Py_DECREF(builderModule);
    sqlite3_finalize(stmt);

    return SQLITE_OK;
}

int lindexCreate(sqlite3 *db,
                 void *pAux,
                 const int argc,
                 const char *const *argv,
                 sqlite3_vtab **ppVtab,
                 char **errMsg)
{
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

    rc = initPythonIndex(db, rTableName, "fcnn2", 1, vtab);

    char* result_query = sqlite3_mprintf("SELECT * FROM %s WHERE ROWID = ?;", rTableName);
    sqlite3_prepare_v2(db, result_query, -1, &vtab->stmt, NULL);
    //sqlite3_finalize(vtab->stmt);

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
        ////printf("%d %s\n", i, argv[i]);
    }

    return lindexCreate(db, pAux, argc, argv, ppVtab, pzErr);
}

int lindexDisconnect(sqlite3_vtab *pVtab)
{
    puts("DISCONNECT");
    lindex_vtab *p = (lindex_vtab*)pVtab;
    //puts("free");
    sqlite3_free(p);
    //puts("ok");
    return SQLITE_OK;
}
