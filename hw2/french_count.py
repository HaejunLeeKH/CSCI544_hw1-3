import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.set_final('start')
    f.initial_state = 'start'

    f.add_state('second_digit')
    f.add_state('ones')
    f.add_state('100s')
    f.add_state('100s_done')
    f.add_state('100s_done_zero')
    f.add_state('100s_done_zero_zero')
    f.add_state('tens')
    f.add_state('seventeen_head')
    f.add_state('seventeen_tail')
    f.add_state('eighteen_head')
    f.add_state('eighteen_tail')
    f.add_state('nineteen_head')
    f.add_state('nineteen_tail')
    f.add_state('20s')
    f.add_state('et_and')
    f.add_state('et_tail')
    f.add_state('30s')
    f.add_state('40s')
    f.add_state('50s')
    f.add_state('60s')
    f.add_state('70s')
    f.add_state('71s')
    f.add_state('71s_tail')
    f.add_state('77s')
    f.add_state('77s_tail')
    f.add_state('78s')
    f.add_state('78s_tail')
    f.add_state('79s')
    f.add_state('79s_tail')
    f.add_state('80s')
    f.add_state('80s_tail')
    f.add_state('90s')
    f.add_state('90s_tail')
    f.add_state('97s')
    f.add_state('97s_tail')
    f.add_state('98s')
    f.add_state('98s_tail')
    f.add_state('99s')
    f.add_state('99s_tail')


    f.set_final('ones')
    f.set_final('100s_done_zero')
    f.set_final('tens')
    f.set_final('seventeen_tail')
    f.set_final('eighteen_tail')
    f.set_final('nineteen_tail')
    f.set_final('20s')
    f.set_final('et_tail')
    f.set_final('30s')
    f.set_final('40s')
    f.set_final('50s')
    f.set_final('60s')
    f.set_final('70s')
    f.set_final('71s_tail')
    f.set_final('77s_tail')
    f.set_final('78s_tail')
    f.set_final('79s_tail')
    f.set_final('80s_tail')
    f.set_final('90s_tail')
    f.set_final('97s_tail')
    f.set_final('98s_tail')
    f.set_final('99s_tail')




    f.add_arc('start', 'second_digit', [str(0)], [])
    f.add_arc('second_digit', 'ones', [str(0)], [])
    # arcs for 1s
    for ii in xrange(10):
        f.add_arc('ones', 'ones', [str(ii)], [kFRENCH_TRANS[ii]])

    # arcs for 200,300,400,500,600,700,800,900
    # 100 - Cent
    # 101 - Cent un
    for ii in xrange(1, 10):
        f.add_arc('start', '100s', [str(ii)], [kFRENCH_TRANS[ii]])
    f.add_arc('100s', '100s_done', [], [kFRENCH_TRANS[100]])
    f.add_arc('start', '100s_done', [str(1)], [kFRENCH_TRANS[100]])

    # if 1st digit is not zero, 2nd digit is zero, come to this state
    f.add_arc('100s_done', '100s_done_zero', [str(0)], [])
    # else, from 100s_done, go to 10~99 states

    # SHOULD ADD MORE CODE FOR GOING 10~99 FROM 100S CASE

    # if 3rd digit is zero, then finish here
    f.add_arc('100s_done_zero', '100s_done_zero', [str(0)], [])
    # 1-9, go to ones
    for ii in xrange(1, 10):
        f.add_arc('100s_done_zero', 'ones', [str(ii)], [kFRENCH_TRANS[ii]])


    # second digit is not zero

    # 10s
    f.add_arc('second_digit', 'tens', [str(1)], [])
    # 10~16
    for ii in xrange(0,7):
        f.add_arc('tens', 'tens', [str(ii)], [kFRENCH_TRANS[10+ii]])
    # 17
    f.add_arc('tens', 'seventeen_head', [str(7)], [kFRENCH_TRANS[10]])
    f.add_arc('seventeen_head', 'seventeen_tail', [], [kFRENCH_TRANS[7]])
    # 18
    f.add_arc('tens', 'eighteen_head', [str(8)], [kFRENCH_TRANS[10]])
    f.add_arc('eighteen_head', 'eighteen_tail', [], [kFRENCH_TRANS[8]])
    # 19
    f.add_arc('tens', 'nineteen_head', [str(9)], [kFRENCH_TRANS[10]])
    f.add_arc('nineteen_head', 'nineteen_tail', [], [kFRENCH_TRANS[9]])

    # 20s
    f.add_arc('second_digit', '20s', [str(2)], [kFRENCH_TRANS[20]])
    # 20
    f.add_arc('20s', '20s', [str(0)], [])
    # 21
    f.add_arc('20s', 'et_and', [str(1)], [kFRENCH_AND])
    # add french and, add 1
    # this part will be used for 21, 31, 41, 51, 61, 71, too
    f.add_arc('et_and', 'et_tail', [], [kFRENCH_TRANS[1]])
    # f.add_arc('et_tail', 'et_finish', [], [])
    # 22~29
    for ii in xrange(2,10):
        f.add_arc('20s', '20s', [str(ii)], [kFRENCH_TRANS[ii]])

    # 30s
    f.add_arc('second_digit', '30s', [str(3)], [kFRENCH_TRANS[30]])
    # 30
    f.add_arc('30s', '30s', [str(0)], [])
    # 31. adding 1 after french and is done from 20s part
    f.add_arc('30s', 'et_and', [str(1)], [kFRENCH_AND])
    # 32~39
    for ii in xrange(2, 10):
        f.add_arc('30s', '30s', [str(ii)], [kFRENCH_TRANS[ii]])

    # 40s
    f.add_arc('second_digit', '40s', [str(4)], [kFRENCH_TRANS[40]])
    # 40
    f.add_arc('40s', '40s', [str(0)], [])
    # 41. adding 1 after french and is done from 20s part
    f.add_arc('40s', 'et_and', [str(1)], [kFRENCH_AND])
    # 42~49
    for ii in xrange(2, 10):
        f.add_arc('40s', '40s', [str(ii)], [kFRENCH_TRANS[ii]])

    # 50s
    f.add_arc('second_digit', '50s', [str(5)], [kFRENCH_TRANS[50]])
    # 50
    f.add_arc('50s', '50s', [str(0)], [])
    # 51. adding 1 after french and is done from 20s part
    f.add_arc('50s', 'et_and', [str(1)], [kFRENCH_AND])
    # 52~59
    for ii in xrange(2, 10):
        f.add_arc('50s', '50s', [str(ii)], [kFRENCH_TRANS[ii]])

    # 60s
    f.add_arc('second_digit', '60s', [str(6)], [kFRENCH_TRANS[60]])
    # 60
    f.add_arc('60s', '60s', [str(0)], [])
    # 61. adding 1 after french and is done from 20s part
    f.add_arc('60s', 'et_and', [str(1)], [kFRENCH_AND])
    # 62~69
    for ii in xrange(2, 10):
        f.add_arc('60s', '60s', [str(ii)], [kFRENCH_TRANS[ii]])

    # 70s
    # 70~ = 60, 10~, thus, put 60 first
    f.add_arc('second_digit', '70s', [str(7)], [kFRENCH_TRANS[60]])
    # 70
    f.add_arc('70s', '70s', [str(0)], [kFRENCH_TRANS[10]])
    # 71
    f.add_arc('70s', '71s', [str(1)], [kFRENCH_AND])
    f.add_arc('71s', '71s_tail', [], [kFRENCH_TRANS[11]])
    # 72~76
    for ii in xrange(2,7):
        f.add_arc('70s', '70s', [str(ii)], [kFRENCH_TRANS[10+ii]])
    # 77
    f.add_arc('70s', '77s', [str(7)], [kFRENCH_TRANS[10]])
    f.add_arc('77s', '77s_tail', [], [kFRENCH_TRANS[7]])
    # 78
    f.add_arc('70s', '78s', [str(8)], [kFRENCH_TRANS[10]])
    f.add_arc('78s', '78s_tail', [], [kFRENCH_TRANS[8]])
    # 79
    f.add_arc('70s', '79s', [str(9)], [kFRENCH_TRANS[10]])
    f.add_arc('79s', '79s_tail', [], [kFRENCH_TRANS[9]])

    # 80. 80 = 4,20
    f.add_arc('second_digit', '80s', [str(8)], [kFRENCH_TRANS[4]])
    f.add_arc('80s', '80s_tail', [], [kFRENCH_TRANS[20]])
    f.add_arc('80s_tail', '80s_tail', [str(0)], [])
    for ii in xrange(1,10):
        f.add_arc('80s_tail', '80s_tail', [str(ii)], [kFRENCH_TRANS[ii]])

    # 90. 90 = 4,20,10
    f.add_arc('second_digit', '90s', [str(9)], [kFRENCH_TRANS[4]])
    f.add_arc('90s', '90s_tail', [], [kFRENCH_TRANS[20]])
    # 90~96
    for ii in xrange(0,7):
        f.add_arc('90s_tail', '90s_tail', [str(ii)], [kFRENCH_TRANS[10+ii]])
    # 97
    f.add_arc('90s_tail', '97s', [str(7)], [kFRENCH_TRANS[10]])
    f.add_arc('97s', '97s_tail', [], [kFRENCH_TRANS[7]])
    # 98
    f.add_arc('90s_tail', '98s', [str(8)], [kFRENCH_TRANS[10]])
    f.add_arc('98s', '98s_tail', [], [kFRENCH_TRANS[8]])
    # 99
    f.add_arc('90s_tail', '99s', [str(9)], [kFRENCH_TRANS[10]])
    f.add_arc('99s', '99s_tail', [], [kFRENCH_TRANS[9]])

    # connecting 100s to 10s case
    # for example, for 111, after dealing with 100,
    # should go to 10s state
    f.add_arc('100s_done', 'tens', [str(1)], [])
    f.add_arc('100s_done', '20s', [str(2)], [kFRENCH_TRANS[20]])
    f.add_arc('100s_done', '30s', [str(3)], [kFRENCH_TRANS[30]])
    f.add_arc('100s_done', '40s', [str(4)], [kFRENCH_TRANS[40]])
    f.add_arc('100s_done', '50s', [str(5)], [kFRENCH_TRANS[50]])
    f.add_arc('100s_done', '60s', [str(6)], [kFRENCH_TRANS[60]])
    f.add_arc('100s_done', '70s', [str(7)], [kFRENCH_TRANS[60]])
    f.add_arc('100s_done', '80s', [str(8)], [kFRENCH_TRANS[4]])
    f.add_arc('80s', '80s_tail', [], [kFRENCH_TRANS[20]])
    f.add_arc('100s_done', '90s', [str(9)], [kFRENCH_TRANS[4]])
    f.add_arc('90s', '90s_tail', [], [kFRENCH_TRANS[20]])

    return f


if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
