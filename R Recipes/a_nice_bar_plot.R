library(plyr)
library(tidyverse)

# This uses the summarySE function found in the `summary.R` recipe.

bar.plot <- function(data, x, y, fill=x, xlabel="variable", ylabel="value", title="title", y_axis_amount) {
  h <- summarySE(data, measurevar=y, groupvars=x, na.rm=TRUE)
  y_vals <- c(h[,y])
  se <- h$se
  y_min <- y_vals - se
  y_max <- y_vals + se
  g <-ggplot(h, aes_string(x=x, y=y, fill=fill)) +
    geom_bar(position=position_dodge(), stat='identity', colour="black", size=.3) +
    geom_errorbar(aes(ymin=y_min, ymax=y_max), width=.2, size=.3,
                      position=position_dodge(.9)) +
    xlab(xlabel) + 
    ylab(ylabel) +
    ggtitle(title) +
    theme_bw() +
    theme(plot.title=element_text(hjust=0.5), 
          panel.border=element_blank(), 
          axis.line=element_line(color='black'),
          legend.position="none")
  return(g)
}
