from model.project import Project

import random
import string

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [Project(name=random_string("name", 8)) for i in range(1)]


