int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIndexInfo)
{
    if (pIndexInfo->nConstraint > 0) {
        for (int i = 0; i < pIndexInfo->nConstraint; i++) {
            if (pIndexInfo->aConstraint[i].usable
                && pIndexInfo->aConstraint[i].op == SQLITE_INDEX_CONSTRAINT_EQ) {
                pIndexInfo->aConstraintUsage[i].argvIndex = i+1;
                pIndexInfo->aConstraintUsage[i].omit = 1;
            }
        }
    }
    return SQLITE_OK;
}

