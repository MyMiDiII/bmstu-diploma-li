#include <stdio.h>
#include <string.h>

#include <sqlite3.h>
#include <numpy/arrayobject.h>

#include "cursor.h"
#include "vtable.h"
#include "sqlite_api.h"

typedef struct lindex_cursor {
    sqlite3_vtab_cursor base;
    PyObject *rowids;
    PyArrayIterObject *iter;
} lindex_cursor;

int lindexOpen(sqlite3_vtab *p, sqlite3_vtab_cursor **ppCursor)
{
    puts("OPEN");
    lindex_cursor *pCur;
    pCur = sqlite3_malloc(sizeof(*pCur));

    if (pCur == 0)
        return SQLITE_NOMEM;

    memset(pCur, 0, sizeof(*pCur));
    *ppCursor = &pCur->base;

    return SQLITE_OK;
}

int lindexClose(sqlite3_vtab_cursor *cur)
{
    puts("CLOSE");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);

    sqlite3_free(pCur);

    return SQLITE_OK;
}

int lindexNext(sqlite3_vtab_cursor *cur)
{
    puts("NEXT");
    lindex_cursor *pCur = (lindex_cursor*)cur;

    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);
    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    printf("rowid %ld\n", rowid);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);

    PyArray_ITER_NEXT(pCur->iter);

    return SQLITE_OK;
}

int lindexColumn(sqlite3_vtab_cursor *cur,
                 sqlite3_context *ctx,
                 int i)
{
    puts("COLUMN");
    printf("i %d\n", i);
    //lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    //printf("stmt %p\n", (void *)lTab->stmt);
    int columnValue = sqlite3_column_int(lTab->stmt, i);
    //printf("colVal %d\n", columnValue);

    sqlite3_result_int(ctx, columnValue);

    puts("it ok");
    return SQLITE_OK;
}

int lindexRowid(sqlite3_vtab_cursor *cur, sqlite_int64 *pRowid)
{
    puts("ROWID");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    //lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;
    *pRowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);

    return SQLITE_OK;
}

int lindexEof(sqlite3_vtab_cursor *cur)
{
    puts("EOF");

    lindex_cursor *pCur = (lindex_cursor*)cur;

    return !PyArray_ITER_NOTDONE(pCur->iter);
}

int lindexFilter(sqlite3_vtab_cursor *cur,
                 int idxNum,
                 const char *idxStr,
                 int argc,
                 sqlite3_value **argv)
{
    puts("FILTER");
    import_array()
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyObject* keys = PyList_New(0);

    printf("argc %d\n", argc);
    for (int i = 0; i < argc; ++i)
    {
        printf("val %d\n", sqlite3_value_int(argv[i]));
        PyList_Append(keys, PyLong_FromLong(sqlite3_value_int(argv[i])));
    }

    PyObject* find = PyUnicode_FromString("find");
    //printf("keys_size %ld\n", PyList_Size(keys));
    //printf("find%p\n", find);

    PyObject* rowids = PyObject_CallMethodObjArgs(lTab->lindex, find, keys, NULL);
    printf("%d\n", PyArray_Check(rowids));
    npy_intp size = PyArray_SIZE(rowids);
    printf("%d\n", size);
    puts("are get");
    PyArrayIterObject *iter = (PyArrayIterObject *)PyArray_IterNew(rowids);
    puts("iter");


    lindex_cursor *pCur = (lindex_cursor*)cur;
    pCur->rowids = rowids;
    pCur->iter = iter;
    puts("save");

    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    printf("rowid %ld\n", rowid);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);

    return SQLITE_OK;
}

int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIndexInfo)
{
    puts("BEST");

    if (pIndexInfo->nConstraint > 0)
    {
        for (int i = 0; i < pIndexInfo->nConstraint; i++)
        {
            if (pIndexInfo->aConstraint[i].usable
                && pIndexInfo->aConstraint[i].op == SQLITE_INDEX_CONSTRAINT_EQ)
            {
                pIndexInfo->aConstraintUsage[i].argvIndex = i+1;
                pIndexInfo->aConstraintUsage[i].omit = 1;
            }
        }
    }

    return SQLITE_OK;
}

