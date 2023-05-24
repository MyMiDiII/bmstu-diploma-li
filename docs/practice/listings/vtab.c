struct sqlite3_vtab {
    const sqlite3_module *pModule; /* модуль таблицы */
    int nRef; /* число ссылок, инициализирующееся ядром SQLite */
    char *zErrMsg; /* для передачи сообщений об ошибках ядру */
};
