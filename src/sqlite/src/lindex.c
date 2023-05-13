#include <stdio.h>
#include <string.h>

#include <sqlite3ext.h>

SQLITE_EXTENSION_INIT1

typedef struct lindex_vtab {
  sqlite3_vtab base;
} lindex_vtab;

typedef struct lindex_cursor {
  sqlite3_vtab_cursor base;
  sqlite3_int64 iRowid;
} lindex_cursor;


#define MYTABLE_A  0
#define MYTABLE_B  1
static int lindexCreate(sqlite3 *db,
                        void *pAux,
                        int argc,
                        const char *const *argv,
                        sqlite3_vtab **ppVtab,
                        char **pzErr)
{
    puts("CREATE");
    lindex_vtab *pNew;
    int rc;
    
    rc = sqlite3_declare_vtab(db, "CREATE TABLE x(a,b)");

    if (rc == SQLITE_OK)
    {
        pNew = sqlite3_malloc(sizeof(*pNew));
        *ppVtab = (sqlite3_vtab*)pNew;

        if (pNew == 0)
            return SQLITE_NOMEM;

        memset(pNew, 0, sizeof(*pNew));
    }

    return rc;
}

static int lindexConnect(sqlite3 *db,
                         void *pAux,
                         int argc,
                         const char *const *argv,
                         sqlite3_vtab **ppVtab,
                         char **pzErr)
{
    puts("CONNECT");
    return lindexCreate(db, pAux, argc, argv, ppVtab, pzErr);
}

static int lindexDisconnect(sqlite3_vtab *pVtab)
{
    puts("DISCONNECT");
    lindex_vtab *p = (lindex_vtab*)pVtab;
    sqlite3_free(p);
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

   switch (i)
   {
     case MYTABLE_A:
       sqlite3_result_int(ctx, 1000 + pCur->iRowid);
       break;
     default:
       sqlite3_result_int(ctx, 2000 + pCur->iRowid);
       break;
   }

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
    pIdxInfo->estimatedCost = (double)10;
    pIdxInfo->estimatedRows = 10;
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
