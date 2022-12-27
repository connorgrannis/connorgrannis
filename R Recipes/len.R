# can handle missing values when calculating the length of a vector

len <- function(x, na.rm=F) {
  if(na.rm) sum(!is.na(x))
  else      length(x)
}
