import string
import random


def generate_id():
    # this is for a really weird bug
    # when using mongodb directly is generate a ObjectID()
    # but wekan seems to be generating a string instead
    # and some part of the code expect the id to be a string and not a objectID
    # so I need to generate string ids myself :|
    return "".join([random.SystemRandom().choice(list(set(string.hexdigits.lower()))) for x in range(17)])


def get(collection, query):
    return list(collection.find(query))[0]


def get_none(collection, query):
    result = list(collection.find(query))
    return result[0] if result else None


def get_by_id(collection, id):
    return get(collection, {"_id": id})
