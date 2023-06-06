#ifndef __CURSOR_H__
#define __CURSOR_H__

#include <sqlite3ext.h>

int lindexOpen(sqlite3_vtab *p, sqlite3_vtab_cursor **ppCursor);
int lindexClose(sqlite3_vtab_cursor *cur);
int lindexNext(sqlite3_vtab_cursor *cur);
int lindexColumn(sqlite3_vtab_cursor *cur,
                 sqlite3_context *ctx,
                 int i);
int lindexRowid(sqlite3_vtab_cursor *cur, sqlite_int64 *pRowid);
int lindexEof(sqlite3_vtab_cursor *cur);
int lindexFilter(sqlite3_vtab_cursor *pVtabCursor, 
                 int idxNum,
                 const char *idxStr,
                 int argc,
                 sqlite3_value **argv);
int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIdxInfo);
int lindexUpdate(sqlite3_vtab *pVTab,
                 int argc,
                 sqlite3_value **argv,
                 sqlite_int64 *pRowid);

#endif
