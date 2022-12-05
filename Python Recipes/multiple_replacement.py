class Xlator(dict):
    """ Pronounced translator. All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys(  ))))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._make_regex(  ).sub(self, text)

# example
text = "This is [a] te:st"
adict = {" ": "_", "[": '', "]": '', ":", ''}

xlat = Xlator(adict)
print(xlat.xlat(text))
