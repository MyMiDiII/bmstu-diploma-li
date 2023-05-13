#include <stdlib.h>
#include <sqlite3.h>

#include "queries.h"

#define COLUMN_SEP ", "

char *get_create_table_query_by_args(
        const int argc,
        const char *const *argv)
{
    sqlite3_str *createTableStmt = sqlite3_str_new(NULL);
    sqlite3_str_appendall(createTableStmt, "CREATE TABLE IF NOT EXISTS %s%s(");

    int i = 3;
    for (; i < argc - 1; ++i)
    {
        sqlite3_str_appendall(createTableStmt, argv[i]);
        sqlite3_str_appendall(createTableStmt, COLUMN_SEP);
    }

    sqlite3_str_appendall(createTableStmt, argv[i]);
    sqlite3_str_appendall(createTableStmt, ");");

    return sqlite3_str_finish(createTableStmt);
}
