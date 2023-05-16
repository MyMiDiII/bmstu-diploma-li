#include <stdio.h>
#include <string.h>

#include <sqlite3.h>

#include "cursor.h"
#include "vtable.h"
#include "sqlite_api.h"

typedef struct lindex_cursor {
    sqlite3_vtab_cursor base;
    int array_index;
} lindex_cursor;

int lindexOpen(sqlite3_vtab *p, sqlite3_vtab_cursor **ppCursor)
{
    puts("OPEN");
    lindex_cursor *pCur;
    pCur = sqlite3_malloc(sizeof(*pCur));

    if (pCur == 0)
        return SQLITE_NOMEM;

    memset(pCur, 0, sizeof(*pCur));
    //pCur->vtab = (lindex_vtab*)p;
    pCur->array_index = -1;
    *ppCursor = &pCur->base;

    return SQLITE_OK;
}

int lindexClose(sqlite3_vtab_cursor *cur)
{
    puts("CLOSE");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    sqlite3_free(pCur);
    return SQLITE_OK;
}

int lindexNext(sqlite3_vtab_cursor *cur)
{
    puts("NEXT");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    pCur->array_index++;

    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;

    sqlite3_reset(lTab->stmt);
    sqlite3_clear_bindings(lTab->stmt);
    sqlite3_bind_int64(lTab->stmt, 1, lTab->values[pCur->array_index]);
    sqlite3_step(lTab->stmt);

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
    printf("colVal %d\n", columnValue);

    sqlite3_result_int(ctx, columnValue);

    puts("it ok");
    return SQLITE_OK;
}

int lindexRowid(sqlite3_vtab_cursor *cur, sqlite_int64 *pRowid)
{
    puts("ROWID");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;
    *pRowid = lTab->values[pCur->array_index];

    return SQLITE_OK;
}

int lindexEof(sqlite3_vtab_cursor *cur)
{
    puts("EOF");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    lindex_vtab *lTab = (lindex_vtab*)cur->pVtab;
    return pCur->array_index >= lTab->number;
}

int lindexFilter(sqlite3_vtab_cursor *pVtabCursor, 
                 int idxNum,
                 const char *idxStr,
                 int argc,
                 sqlite3_value **argv)
{
    puts("FILTER");

    //printf("argc %d\n", argc);
    for (int i = 0; i < argc; ++i)
    {
        //printf("%d %s\n", i, (char *)argv[i]);
    }
    //lindex_cursor *pCur = (lindex_cursor *)pVtabCursor;
    lindex_vtab *lTab = (lindex_vtab*)pVtabCursor->pVtab;

    for (int i = 0; i < lTab->number; ++i)
    {
        puts("p3");
        //printf("key %d value %ld\n", lTab->keys[i], lTab->values[i]);
    }

    lindexNext(pVtabCursor);

    return SQLITE_OK;
}

int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIdxInfo)
{
    puts("BEST");

    //if (pIdxInfo->nConstraint != 1)
    //{
    //    puts("ERR");
    //    return SQLITE_OK;
    //}

    //struct sqlite3_index_constraint *pConstraint = &pIdxInfo->aConstraint[0];

    //if (pConstraint->op == SQLITE_INDEX_CONSTRAINT_EQ)
    //{
    //    puts("OK1");
    //    //printf("%d\n", pConstraint->iColumn);
    //    if (pConstraint->iColumn == 0)
    //    {
    //        puts("OK2");
    //        pIdxInfo->idxNum = -1;
    //        pIdxInfo->aConstraintUsage[0].omit = 1;
    //    }
    //}

    return SQLITE_OK;
}

