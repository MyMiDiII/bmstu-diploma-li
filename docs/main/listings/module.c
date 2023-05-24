struct sqlite3_module {
    int iVersion;
    int (*xCreate)(sqlite3*, void *pAux,
                 int argc, char *const*argv,
                 sqlite3_vtab **ppVTab,
                 char **pzErr);
    int (*xConnect)(sqlite3*, void *pAux,
                 int argc, char *const*argv,
                 sqlite3_vtab **ppVTab,
                 char **pzErr);
    int (*xBestIndex)(sqlite3_vtab *pVTab, sqlite3_index_info*);
    int (*xDisconnect)(sqlite3_vtab *pVTab);
    int (*xDestroy)(sqlite3_vtab *pVTab);
    int (*xOpen)(sqlite3_vtab *pVTab,
                 sqlite3_vtab_cursor **ppCursor);
    int (*xClose)(sqlite3_vtab_cursor*);
    int (*xFilter)(sqlite3_vtab_cursor*,
                   int idxNum, const char *idxStr,
                   int argc, sqlite3_value **argv);
    int (*xNext)(sqlite3_vtab_cursor*);
    int (*xEof)(sqlite3_vtab_cursor*);
    int (*xColumn)(sqlite3_vtab_cursor*, sqlite3_context*, int);
    int (*xRowid)(sqlite3_vtab_cursor*, sqlite_int64 *pRowid);
    int (*xUpdate)(sqlite3_vtab *, int,
                   sqlite3_value **, sqlite_int64 *);
    /* представлены указатели на реализующиеся методы */
    /* при инициализации структуры, */
    /* остальные поля принимают значение 0 */
};

int sqlite3_create_module(
    sqlite3 *db,          /* соединение для регистрации модуля */
    const char *zName,      /* имя модуля */
    const sqlite3_module *, /* ссылка на структуру модуля */
    void *,                 /* данные для xCreate/xConnect*/
);
