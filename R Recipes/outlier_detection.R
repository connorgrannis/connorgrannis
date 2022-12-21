library(tidyverse)

# defining vector
vec <- mpg$hwy

find_outliers <- function(vec) {
    # get the IQR
    iqr <- IQR(vec)
    s <- summary(vec)
    # Get the 1st and 3rd quartiles
    q1 <- s[["1st Qu."]]
    q3 <- s[["3rd Qu."]]
    # define outliers
    out <- vec < (q1-1.5*iqr) | vec > (q3+1.5*iqr)
    # implicit return a list of outlier values and their index posisitions
    list(out=vec[out],
         idx=which(vec %in% c(vec[out]))
        )
}

outliers <- find_outliers(vec)
outliers$out
outliers$idx
mpg[outliers$idx, ]


# or using the existing function
out <- boxplot.stats(vec)$out
out_idx <- which(vec %in% c(out))
mpg[out_idx, ]
