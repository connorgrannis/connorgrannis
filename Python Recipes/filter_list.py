import re
from functools import compress
def filter_list(needle, haystack):
    m = re.compile(needle)
    matches = list(map(lambda x: m.match(x), haystack))
    fltr    = list(map(lambda x: x is not None, matches))
    return    list(map(lambda x: x.group(0), list(compress(matches, fltr))))

# example
l = ['carrot', 'canoe', 'bed', 'frame', 'asparagus', 'roger']
pattern = ".*r.*"
print(filter_list(pattern, l))
