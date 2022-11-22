import sys
def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Will display a progress bar so you can monitor your .... progress.
    
    Here's an example of how to use it:
    import time
    for i in progressbar(range(15), "Computing: ", 40):
        time.sleep(0.1) # any calculation you need
    
    This will work correctly in putty but NOT in spyder -- it will output each increment on a newline
    
    """
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
