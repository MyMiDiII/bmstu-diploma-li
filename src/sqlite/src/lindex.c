#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sqlite3ext.h>

#include "queries.h"

SQLITE_EXTENSION_INIT1

typedef struct lindex_vtab {
  sqlite3_vtab base;
} lindex_vtab;

typedef struct lindex_cursor {
  sqlite3_vtab_cursor base;
  sqlite3_int64 iRowid;
} lindex_cursor;



static int lindexCreate(sqlite3 *db,
                        void *pAux,
                        const int argc,
                        const char *const *argv,
                        sqlite3_vtab **ppVtab,
                        char **errMsg)
{
    puts("CREATE");
    lindex_vtab *vtab = sqlite3_malloc(sizeof(lindex_vtab));

    if (!vtab)
        return SQLITE_NOMEM;

    memset(vtab, 0, sizeof(*vtab));
    *ppVtab = &vtab->base;

    char *sql_template = get_create_table_query_by_args(argc, argv);

    const char *table_name = argv[2];

    char *vtab_name = sqlite3_mprintf(sql_template, "", table_name);
    char *rtab_name = sqlite3_mprintf(sql_template, "r", table_name);

    puts(vtab_name);
    puts(rtab_name);

    int rc = sqlite3_declare_vtab(db, vtab_name);

    if (!rc)
        rc = sqlite3_exec(db, rtab_name, NULL, NULL, errMsg);

    sqlite3_free(sql_template);
    sqlite3_free(vtab_name);
    sqlite3_free(rtab_name);

    return rc;
}

static int lindexConnect(sqlite3 *db,
                         void *pAux,
                         int argc,
                         const char *const *argv,
                         sqlite3_vtab **ppVtab,
                         char **pzErr)
{
    return lindexCreate(db, pAux, argc, argv, ppVtab, pzErr);
}

static int lindexDisconnect(sqlite3_vtab *pVtab)
{
    puts("DISCONNECT");
    lindex_vtab *p = (lindex_vtab*)pVtab;
    puts("free");
    sqlite3_free(p);
    puts("ok");
    return SQLITE_OK;
}

static int lindexOpen(sqlite3_vtab *p, sqlite3_vtab_cursor **ppCursor)
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

static int lindexClose(sqlite3_vtab_cursor *cur)
{
    puts("CLOSE");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    sqlite3_free(pCur);
    return SQLITE_OK;
}


static int lindexNext(sqlite3_vtab_cursor *cur)
{
    puts("NEXT");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    pCur->iRowid++;
    return SQLITE_OK;
}

static int lindexColumn(sqlite3_vtab_cursor *cur,
                        sqlite3_context *ctx,
                        int i)
{
   puts("COLUMN");
   lindex_cursor *pCur = (lindex_cursor*)cur;

   sqlite3_result_int(ctx, pCur->iRowid);

   return SQLITE_OK;
}

static int lindexRowid(sqlite3_vtab_cursor *cur, sqlite_int64 *pRowid)
{
    puts("ROWID");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    *pRowid = pCur->iRowid;
    return SQLITE_OK;
}

static int lindexEof(sqlite3_vtab_cursor *cur)
{
    puts("EOF");
    lindex_cursor *pCur = (lindex_cursor*)cur;
    return pCur->iRowid >= 10;
}

static int lindexFilter(sqlite3_vtab_cursor *pVtabCursor, 
                        int idxNum,
                        const char *idxStr,
                        int argc,
                        sqlite3_value **argv)
{
    puts("FILTER");
    lindex_cursor *pCur = (lindex_cursor *)pVtabCursor;
    pCur->iRowid = 1;
    return SQLITE_OK;
}

static int lindexBestIndex(sqlite3_vtab *tab,
                           sqlite3_index_info *pIdxInfo)
{
    puts("BEST");
    //pIdxInfo->estimatedCost = (double)10;
    //pIdxInfo->estimatedRows = 10;
    return SQLITE_OK;
}

static sqlite3_module lindexModule = {
  /* iVersion    */ 0,
  /* xCreate     */ lindexCreate,
  /* xConnect    */ lindexConnect,
  /* xBestIndex  */ lindexBestIndex,
  /* xDisconnect */ lindexDisconnect,
  /* xDestroy    */ lindexDisconnect,
  /* xOpen       */ lindexOpen,
  /* xClose      */ lindexClose,
  /* xFilter     */ lindexFilter,
  /* xNext       */ lindexNext,
  /* xEof        */ lindexEof,
  /* xColumn     */ lindexColumn,
  /* xRowid      */ lindexRowid,
  /* xUpdate     */ 0,
  /* xBegin      */ 0,
  /* xSync       */ 0,
  /* xCommit     */ 0,
  /* xRollback   */ 0,
  /* xFindMethod */ 0,
  /* xRename     */ 0,
  /* xSavepoint  */ 0,
  /* xRelease    */ 0,
  /* xRollbackTo */ 0,
  /* xShadowName */ 0
};


int sqlite3_lindex_init(sqlite3 *db, 
                        char **pzErrMsg, 
                        const sqlite3_api_routines *pApi)
{
    SQLITE_EXTENSION_INIT2(pApi);
    int rc = sqlite3_create_module(db, "lindex", &lindexModule, 0);
    printf("rc = %d\n", rc);
    return rc;
}
