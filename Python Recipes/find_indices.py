def get_index(haystack, needle):
    return haystack.index(needle)

def get_all_indicies(haystack, needle):
    return [i for i, x in enumerate(haystack) if x == needle]
