#ifndef __VTABLE_H__
#define __VTABLE_H__

#include <stdint.h>
#include <sqlite3ext.h>

#include <Python.h>

typedef struct lindex_vtab {
    sqlite3_vtab base;
    sqlite3_stmt *stmt;
    PyObject *lindex;
} lindex_vtab;

int lindexCreate(sqlite3 *db,
                 void *pAux,
                 const int argc,
                 const char *const *argv,
                 sqlite3_vtab **ppVtab,
                 char **errMsg);

int lindexConnect(sqlite3 *db,
                  void *pAux,
                  int argc,
                  const char *const *argv,
                  sqlite3_vtab **ppVtab,
                  char **pzErr);

int lindexDisconnect(sqlite3_vtab *pVtab);

#endif
