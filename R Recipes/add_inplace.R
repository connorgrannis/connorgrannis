`%+=%` = function(x, y) eval.parent(substitute(x <- x + y))


x <- 0
print(x)

x %+=% 1
print(x)
