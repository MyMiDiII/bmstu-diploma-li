#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <Python.h>

#include "vtable.h"
#include "cursor.h"
#include "sqlite_api.h"


SQLITE_EXTENSION_INIT1


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
  /* xUpdate     */ lindexUpdate,
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
    Py_Initialize();
    return sqlite3_create_module(db, "lindex", &lindexModule, 0);
}
