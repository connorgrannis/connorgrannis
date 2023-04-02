library(ggplot)       # plotting
library(ggtext)       # to enable element_markdown
library(glue)         # string concatenation

# a function that changes the color of 
highlight = function(x, pat, color="black", family="") {
  ifelse(grepl(pat, x), glue("<b style='font-family:{family}; color:{color}'>{x}</b>"), x)
}

# select 'f' in mpg$drv and mark is as bold
bold.f <- ifelse(levels(mpg$drv %>% as.factor) == "f", "bold", "plain")

ggplot(mpg, aes(drv, hwy)) +
  geom_point() +
  scale_x_discrete(labels=function(x) highlight(x, "f", "red")) +
  theme(axis.text.x = element_markdown(face=bold.f))

