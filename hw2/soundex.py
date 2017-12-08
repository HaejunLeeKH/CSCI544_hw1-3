from fst import FST
import string, sys
from fsmutils import composechars, trace


def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('neo_start')
    f1.initial_state = 'start'

    f1.add_state('r_one')
    f1.add_state('r_two')
    f1.add_state('r_three')
    f1.add_state('r_four')
    f1.add_state('r_five')
    f1.add_state('r_six')

    # Set all the final states
    f1.set_final('neo_start')
    f1.set_final('start')

    f1.set_final('r_one')
    f1.set_final('r_two')
    f1.set_final('r_three')
    f1.set_final('r_four')
    f1.set_final('r_five')
    f1.set_final('r_six')

    # set list of characters for change check
    list_1 = ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']
    list_2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z',
              'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']
    list_3 = ['d', 't', 'D', 'T']
    list_4 = ['l', 'L']
    list_5 = ['m', 'n', 'M', 'N']
    list_6 = ['r', 'R']

    # Add the rest of the arcs

    # from start
    # to take first letter also account for occurance check
    # if first letter is vowel, state goes neo_start
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('start', 'r_one', (ch), (ch))
        elif ch in list_2:
            f1.add_arc('start', 'r_two', (ch), (ch))
        elif ch in list_3:
            f1.add_arc('start', 'r_three', (ch), (ch))
        elif ch in list_4:
            f1.add_arc('start', 'r_four', (ch), (ch))
        elif ch in list_5:
            f1.add_arc('start', 'r_five', (ch), (ch))
        elif ch in list_6:
            f1.add_arc('start', 'r_six', (ch), (ch))
        else:
            f1.add_arc('start', 'neo_start', (ch), (ch))

    # case of rule 1-6, move to rule state
    # if vowels found from neo_start, then delete them by staying neo_start
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('neo_start', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('neo_start', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('neo_start', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('neo_start', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('neo_start', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('neo_start', 'r_six', (ch), '6')
        else:
            f1.add_arc('neo_start', 'neo_start', (ch), ())

    # from rule ones
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_one', 'r_one', (ch), ())
        elif ch in list_2:
            f1.add_arc('r_one', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('r_one', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('r_one', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('r_one', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('r_one', 'r_six', (ch), '6')
        else:
            f1.add_arc('r_one', 'r_one', (ch), ())

    # from rule two
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_two', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('r_two', 'r_two', (ch), ())
        elif ch in list_3:
            f1.add_arc('r_two', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('r_two', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('r_two', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('r_two', 'r_six', (ch), '6')
        else:
            f1.add_arc('r_two', 'r_two', (ch), ())

    # from rule three
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_three', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('r_three', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('r_three', 'r_three', (ch), ())
        elif ch in list_4:
            f1.add_arc('r_three', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('r_three', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('r_three', 'r_six', (ch), '6')
        else:
            f1.add_arc('r_three', 'r_three', (ch), ())

    # from rule four
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_four', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('r_four', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('r_four', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('r_four', 'r_four', (ch), ())
        elif ch in list_5:
            f1.add_arc('r_four', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('r_four', 'r_six', (ch), '6')
        else:
            f1.add_arc('r_four', 'r_four', (ch), ())

    # from rule five
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_five', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('r_five', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('r_five', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('r_five', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('r_five', 'r_five', (ch), ())
        elif ch in list_6:
            f1.add_arc('r_five', 'r_six', (ch), '6')
        else:
            f1.add_arc('r_five', 'r_five', (ch), ())

    # from rule six
    for ch in string.letters:
        if ch in list_1:
            f1.add_arc('r_six', 'r_one', (ch), '1')
        elif ch in list_2:
            f1.add_arc('r_six', 'r_two', (ch), '2')
        elif ch in list_3:
            f1.add_arc('r_six', 'r_three', (ch), '3')
        elif ch in list_4:
            f1.add_arc('r_six', 'r_four', (ch), '4')
        elif ch in list_5:
            f1.add_arc('r_six', 'r_five', (ch), '5')
        elif ch in list_6:
            f1.add_arc('r_six', 'r_six', (ch), ())
        else:
            f1.add_arc('r_six', 'r_six', (ch), ())

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?


def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('0')
    f2.initial_state = '0'

    f2.add_state('1')
    f2.set_final('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')

    # Add the arcs
    # if first character is digit, then go to state 2
    # because it will only need 3 arcs
    for letter in string.letters:
        f2.add_arc('0', '1', (letter), (letter))
    for n in range(10):
        f2.add_arc('0', '2', (str(n)), (str(n)))

    for letter in string.letters:
        f2.add_arc('1', '2', (letter), (letter))
    for n in range(10):
        f2.add_arc('1', '2', (str(n)), (str(n)))

    for letter in string.letters:
        f2.add_arc('2', '3', (letter), (letter))
    for n in range(10):
        f2.add_arc('2', '3', (str(n)), (str(n)))

    for letter in string.letters:
        f2.add_arc('3', '4', (letter), (letter))
    for n in range(10):
        f2.add_arc('3', '4', (str(n)), (str(n)))

    for letter in string.letters:
        f2.add_arc('4', '4', (letter), ())
    for n in range(10):
        f2.add_arc('4', '4', (str(n)), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.initial_state = '1'

    f3.add_state('d2')
    f3.add_state('d3')
    f3.add_state('d4')

    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')

    f3.set_final('4')
    f3.set_final('d4')

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '2', (str(number)), (str(number)))
        f3.add_arc('2', '3', (str(number)), (str(number)))
        f3.add_arc('3', '4', (str(number)), (str(number)))

    f3.add_arc('1', 'd2', (), ('0'))
    f3.add_arc('d2', 'd3', (), ('0'))
    f3.add_arc('d3', 'd4', (), ('0'))

    f3.add_arc('2', 'd3', (), ('0'))
    f3.add_arc('3', 'd4', (), ('0'))

    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
