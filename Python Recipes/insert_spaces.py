def insert_spaces(text, char="="):
    """ text is a \""" string of multiple lines """
    text_lines = text.split("\n")
    # find char
    equal_positions = list(map(lambda x: x.find(char), text_lines))
    end_position = max(equal_positions)
    num_spaces = list(map(lambda x: end_position-x, equal_positions))
    # add spaces between start and end positions
    formatted_text = list(map(lambda x, eq_pos, num_eqs: x[:eq_pos] + ' '*num_eqs + x[eq_pos:], text_lines, equal_positions, num_spaces))
    print('\n'.join(formatted_text))


insert_spaces("""
zero = 0
one = 1
three = 3
twentyseven = 27
              """)

insert_spaces("""
zero : 0
one : 1
three : 3
twentyseven : 27
              """, char=":")
