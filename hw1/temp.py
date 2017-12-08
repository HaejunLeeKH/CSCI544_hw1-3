import unittest
from limerick import LimerickDetector

def main():
    ld = LimerickDetector()

    e = """An exceedingly fat friend of mine,
    When asked at what hour he'd dine,
    Replied, "At eleven,
    At three, five, and seven,
    And eight and a quarter past nine"""

    test = """There once was a young lady named bright

Whose speed was much faster than light
She set out one day
In a relative way
And returned on the previous night.
    """

    t1="""can't
    I'll
    you'd
    pant
    you're
    """

    t2 = """can't There once was a young lady named bright

    I'll Whose speed was, much faster than light
    you'd She set out one day
    pant In a relative way
    you're And returned onthe previous,night.
        """

    my = """An exceptionally fat knowledge set of machine learning
That is not an easy thing to be done like turning
People, they believe in books,
but you need more for cooks.
Only way to do is keep going for wisdom earning"""

    s=[]
    print ld.is_limerick(e)
    # print True

    # print ld.rhymes("learning", "earning")
    print ld.rhymes("learning", "turning")

    # print ld.num_syllables("dangle"), 2, ld.guess_syllables('dangle'), 'dangle'
    # print ld.num_syllables("dog"), 1, ld.guess_syllables('dog'), 'dog'
    # print ld.num_syllables("asdf"), 1, ld.guess_syllables('asdf'), 'asdf'
    # print ld.num_syllables("letter"), 2, ld.guess_syllables('letter'), 'letter'
    # print ld.num_syllables("washington"), 3, ld.guess_syllables('washington'), 'washington'
    # print ld.num_syllables("dock"), 1, ld.guess_syllables('dock'), 'dock'
    # print ld.num_syllables("dangle"), 2, ld.guess_syllables('dangle'), 'dangle'
    # print ld.num_syllables("thrive"), 1, ld.guess_syllables('thrive'), 'thrive'
    # print ld.num_syllables("fly"), 1, ld.guess_syllables('fly'), 'fly'
    # print ld.num_syllables("placate"), 2, ld.guess_syllables('placate'), 'placate'
    # print ld.num_syllables("renege"), 2, ld.guess_syllables('renege'), 'renege'
    # print ld.num_syllables("reluctant"), 2, ld.guess_syllables('reluctant'), 'reluctant'
    # print ld.rhymes("anatomical", "She")




if __name__ == '__main__':
  main()