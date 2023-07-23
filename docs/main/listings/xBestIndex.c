int lindexBestIndex(sqlite3_vtab *tab,
                    sqlite3_index_info *pIndexInfo)
{
    if (pIndexInfo->nConstraint == 1)
    {
        if (pIndexInfo->aConstraint[0].usable)
        {
            int mode;
            switch (pIndexInfo->aConstraint[0].op)
            {
                case SQLITE_INDEX_CONSTRAINT_EQ:
                    mode = 0;
                    break;
                case SQLITE_INDEX_CONSTRAINT_GT:
                    mode = 11;
                    break;
                case SQLITE_INDEX_CONSTRAINT_GE:
                    mode = 10;
                    break;
                case SQLITE_INDEX_CONSTRAINT_LT:
                    mode = 21;
                    break;
                case SQLITE_INDEX_CONSTRAINT_LE:
                    mode = 20;
                    break;
                default:
                    return SQLITE_CONSTRAINT;
            }
            pIndexInfo->idxNum = mode;
            pIndexInfo->aConstraintUsage[0].argvIndex = 1;
            pIndexInfo->aConstraintUsage[0].omit = 1;

            return SQLITE_OK;
        }

        return SQLITE_CONSTRAINT;
    }

    if (pIndexInfo->nConstraint == 2)
    {
        for (int i = 0; i < pIndexInfo->nConstraint; i++)
        {
            switch (pIndexInfo->aConstraint[i].op)
            {
                case SQLITE_INDEX_CONSTRAINT_LE:
                    break;
                case SQLITE_INDEX_CONSTRAINT_GE:
                    break;
                default:
                    return SQLITE_CONSTRAINT;
            }

            pIndexInfo->aConstraintUsage[i].argvIndex = i + 1;
            pIndexInfo->aConstraintUsage[i].omit = 1;
        }

        pIndexInfo->idxNum = 30;

        return SQLITE_OK;
    }

    return SQLITE_CONSTRAINT;
}
