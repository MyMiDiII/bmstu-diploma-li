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
    //puts("OPEN");
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
    //puts("CLOSE");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);

    sqlite3_free(pCur);

    return SQLITE_OK;
}

int lindexNext(sqlite3_vtab_cursor *cur)
{
    //puts("NEXT");
    lindex_cursor *pCur = (lindex_cursor*)cur;

    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyArray_ITER_NEXT(pCur->iter);

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);
    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    //printf("rowid %ld\n", rowid);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);


    return SQLITE_OK;
}

int lindexColumn(sqlite3_vtab_cursor *cur,
                 sqlite3_context *ctx,
                 int i)
{
    //puts("COLUMN");
    //printf("i %d\n", i);
    //lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    ////printf("stmt %p\n", (void *)lTab->stmt);
    int64_t columnValue = sqlite3_column_int64(lTab->stmt, i);
    ////printf("colVal %d\n", columnValue);

    sqlite3_result_int64(ctx, columnValue);

    //puts("it ok");
    return SQLITE_OK;
}

int lindexRowid(sqlite3_vtab_cursor *cur, sqlite_int64 *pRowid)
{
    //puts("ROWID");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    //lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;
    *pRowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);

    return SQLITE_OK;
}

int lindexEof(sqlite3_vtab_cursor *cur)
{
    //puts("EOF");

    lindex_cursor *pCur = (lindex_cursor*)cur;

    return !PyArray_ITER_NOTDONE(pCur->iter);
}

int lindexFilter(sqlite3_vtab_cursor *cur,
                 int idxNum,
                 const char *idxStr,
                 int argc,
                 sqlite3_value **argv)
{
    //puts("FILTER");
    //printf("%d\n", idxNum);

    import_array()
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    PyObject* keys = PyList_New(0);

    //printf("argc %d\n", argc);
    for (int i = 0; i < argc; ++i)
    {
        int64_t value = (int64_t)sqlite3_value_int64(argv[i]);
        //printf("%ld\n", value);
        PyList_Append(keys, PyLong_FromLong(value));
    }

    PyObject* tuple_rowids;

    if (!idxNum)
    {
        //puts("=");
        PyObject* find = PyUnicode_FromString("find");
        //printf("keys_size %ld\n", PyList_Size(keys));
        //printf("find%p\n", find);

        tuple_rowids = PyObject_CallMethodObjArgs(lTab->lindex, find, keys, NULL);
    }
    else
    {
        //puts("range");
        PyObject* constraints = PyList_New(0);
        PyObject* noneObj = Py_None;

        for (int i = 0; i < argc; ++i)
        {
            PyList_Append(constraints, PyLong_FromLong(idxNum % 10));
        }

        if (idxNum / 10 != 3)
        {
            Py_INCREF(noneObj);
            PyList_Insert(keys, idxNum / 10 % 2, noneObj);

            Py_INCREF(noneObj);
            PyList_Insert(constraints, idxNum / 10 % 2, noneObj);
        }

        PyObject* prange= PyUnicode_FromString("predict_range");
        //printf("keys_size %ld\n", PyList_Size(keys));
        //printf("find%p\n", prange);

        tuple_rowids = PyObject_CallMethodObjArgs(lTab->lindex, prange, keys, constraints, NULL);
    }

    PyObject* rowids;

    //if (PyTuple_Check(tuple_rowids)) {
    //    puts("ok");
    //}

    int tmp;
    PyArg_ParseTuple(tuple_rowids, "Oi", &rowids, &tmp);
    if (!rowids)
    {
        PyErr_Print();
        PyErr_Clear();
    }
    //printf("is array %d\n", PyArray_Check(rowids));
    npy_intp size = PyArray_SIZE(rowids);
    //printf("rowids size %d\n", size);
    //puts("are get");
    PyArrayIterObject *iter = (PyArrayIterObject *)PyArray_IterNew(rowids);
    //puts("iter");


    lindex_cursor *pCur = (lindex_cursor*)cur;
    pCur->rowids = rowids;
    pCur->iter = iter;
    //puts("save");

    int64_t rowid = *(int64_t *)PyArray_ITER_DATA(pCur->iter);
    //printf("rowid %ld\n", rowid);
    sqlite3_bind_int64(lTab->stmt, 1, rowid);
    sqlite3_step(lTab->stmt);

    return SQLITE_OK;
}

int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIndexInfo)
{
    //puts("BEST");
    //printf("num contr %d\n", pIndexInfo->nConstraint);

    if (pIndexInfo->nConstraint == 1)
    {
        if (pIndexInfo->aConstraint[0].usable)
        {
            int mode;
            switch (pIndexInfo->aConstraint[0].op)
            {
                case SQLITE_INDEX_CONSTRAINT_EQ:
                    //puts("=");
                    mode = 0;
                    break;
                case SQLITE_INDEX_CONSTRAINT_GT:
                    //puts(">");
                    mode = 11;
                    break;
                case SQLITE_INDEX_CONSTRAINT_GE:
                    //puts(">=");
                    mode = 10;
                    break;
                case SQLITE_INDEX_CONSTRAINT_LT:
                    //puts("<");
                    mode = 21;
                    break;
                case SQLITE_INDEX_CONSTRAINT_LE:
                    //puts("<=");
                    mode = 20;
                    break;
                default:
                    return SQLITE_CONSTRAINT;
            }
            pIndexInfo->idxNum = mode;
            pIndexInfo->aConstraintUsage[0].argvIndex = 1;
            pIndexInfo->aConstraintUsage[0].omit = 1;

            return SQLITE_OK;
        }

        return SQLITE_CONSTRAINT;
    }

    if (pIndexInfo->nConstraint == 2)
    {
        for (int i = 0; i < pIndexInfo->nConstraint; i++)
        {
            switch (pIndexInfo->aConstraint[i].op)
            {
                case SQLITE_INDEX_CONSTRAINT_LE:
                    break;
                case SQLITE_INDEX_CONSTRAINT_GE:
                    break;
                default:
                    return SQLITE_CONSTRAINT;
            }

            pIndexInfo->aConstraintUsage[i].argvIndex = i + 1;
            pIndexInfo->aConstraintUsage[i].omit = 1;
        }

        pIndexInfo->idxNum = 30;

        return SQLITE_OK;
    }

    return SQLITE_CONSTRAINT;
}

int lindexUpdate(sqlite3_vtab *pVTab,
                 int argc,
                 sqlite3_value **argv,
                 sqlite_int64 *pRowid
)
{
    puts("update");
    printf("%d\n", argc);
    printf("%p\n", argv[0]);
    if (!(argc > 1 && sqlite3_value_type(argv[0]) == SQLITE_NULL))
        return SQLITE_CONSTRAINT;

    puts("INSERT");
    lindex_vtab *lTab = (lindex_vtab*)pVTab;
    sqlite3 *db = lTab->db;
    int64_t column = sqlite3_value_int64(argv[2]);
    printf("%ld\n", column);
    char *query = sqlite3_mprintf("INSERT INTO maps VALUES(%d);", column);
    sqlite3_exec(db, query, 0, 0, 0);
    sqlite3_int64 lastRowID = sqlite3_last_insert_rowid(db);
    printf("ROWID = %ld\n", lastRowID);

    PyObject* insert = PyUnicode_FromString("insert");
    PyObject* key = PyLong_FromLongLong(column);
    PyObject* data = PyLong_FromLongLong(lastRowID);

    printf("%p\n", insert);
    PyObject_CallMethodObjArgs(lTab->lindex, insert, key, data, NULL);

    return SQLITE_OK;
}
