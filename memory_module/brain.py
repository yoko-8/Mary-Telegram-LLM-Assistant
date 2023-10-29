import os
from hyperdb import HyperDB
from datetime import datetime

memories = []
brain = HyperDB(memories)

current_dir = os.path.dirname(__file__)
brain.load(os.path.join(current_dir, "memory_pickles/mary_memories.pickle.gz"))


def remember_memories(query):
    return brain.query(query)


def add_memories(user, bot):
    brain.add_documents([
        "User: " + user,
        "Mary: " + bot,
    ])


def save_memories():
    brain.save("memory_pickles/mary_memories.pickle.gz")
