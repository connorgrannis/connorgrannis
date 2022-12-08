library(tidyverse)
library(car)
library(emmeans)
library(glue)
library(effectsize)
library(rstatix)

get.results <- function(res_df, metric, rowname) {
  return(c(subset(as.data.frame(res_df[1])[metric], 
                  rownames(as.data.frame(res_df[1])[metric]) == rowname)))
}

get.eta <- function(res_df) {
  return(as.data.frame(res_df[2])$Eta2)
}

get.sentence <- function(res_df) {
  return(glue("F({get.results(res_df, 'Df', 'Group')},{get.results(res_df, 'Df', 'Residuals')})={round(as.double(get.results(res_df, 'F.value', 'Group')), 3)}, p={round(as.double(get.results(res_df, 'Pr..F.', 'Group')), 3)}, eta={round(get.eta(res_df), 3)}."))
}

