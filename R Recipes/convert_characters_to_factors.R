df[, sapply(df, is.character)] <- lapply(df[, sapply(df, is.character)], as.factor)
