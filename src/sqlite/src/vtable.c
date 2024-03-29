#include <Python.h>

#include "vtable.h"
#include "queries.h"
#include "sqlite_api.h"

int initPythonIndex(sqlite3 *db,
                    const char *const tableName,
                    const char *const modelName,
                    const long column_index,
                    lindex_vtab *vTab)
{
    char* query = sqlite3_mprintf("SELECT ROWID, * FROM %s", tableName);

    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, query, -1, &stmt, NULL);
    sqlite3_free(query);

    if (rc)
        return rc;

    PyObject* builderModule = PyImport_ImportModule("indexes.builder");
    if (!builderModule)
    {
        PyErr_Print();
        PyErr_Clear();
    }
    
    PyObject* builderClassName = PyObject_GetAttrString(builderModule, "LindexBuilder");
    PyObject* pyModelName = PyTuple_Pack(1, PyUnicode_FromString(modelName));
    PyObject* builder = PyObject_CallObject(builderClassName, pyModelName);

    PyObject* lindex = PyObject_CallMethod(builder, "build", NULL);
    PyObject* keys = PyList_New(0);
    PyObject* rows = PyList_New(0);

    int i = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW)
    {
        int64_t key = sqlite3_column_int64(stmt, column_index);
        int64_t rowid = sqlite3_column_int64(stmt, 0);

        PyList_Append(keys, PyLong_FromLong(key));
        PyList_Append(rows, PyLong_FromLong(rowid));

        i++;
    }

    if (i)
    {
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
    vTab->db = db;

    Py_DECREF(keys);
    Py_DECREF(rows);
    Py_DECREF(builder);
    Py_DECREF(pyModelName);
    Py_DECREF(builderClassName);
    Py_DECREF(builderModule);
    sqlite3_finalize(stmt);

    return SQLITE_OK;
}

static int callback(void* data, int argc, char** argv, char** azColName)
{
    char rTableName[1000];
    strcpy(rTableName, (char*)data);

    char *schema = (char*)data;

    int i = 0;
    for (; i < 13; ++i)
    {
        schema[i] = argv[0][i];
    }
    schema[i] = '\0';

    strcat(schema, rTableName);

    for (; argv[0][i] != '(' && argv[0][i] != '\0'; ++i);

    char *end = argv[0] + i;

    strcat(schema, end);

    return 0;
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

    const char *vTableName = argv[2];
    const char *rTableName = vTableName + 4;

    /* проверить существование регулярной таблицы */

    char *sql_template = "SELECT sql FROM sqlite_master WHERE type='table' AND name='%s';";
    char *schemaQuery = sqlite3_mprintf(sql_template, rTableName);

    char* messaggeError;
    char vSqlQuery[10000];
    strcpy(vSqlQuery, vTableName);
    int rc = sqlite3_exec(db, schemaQuery, callback, vSqlQuery, &messaggeError);
    char *resVSqlQuery = sqlite3_mprintf("%s;", vSqlQuery);

    rc = sqlite3_declare_vtab(db, resVSqlQuery);

    sqlite3_free(schemaQuery);
    sqlite3_free(resVSqlQuery);

    long column_index = strtol(argv[3], NULL, 10);
    const char *model = argv[4];

    rc = initPythonIndex(db, rTableName, model, column_index, vtab);

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
    return lindexCreate(db, pAux, argc, argv, ppVtab, pzErr);
}

int lindexDisconnect(sqlite3_vtab *pVtab)
{
    lindex_vtab *p = (lindex_vtab*)pVtab;
    sqlite3_free(p);
    return SQLITE_OK;
}
