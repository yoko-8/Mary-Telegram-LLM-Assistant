from hyperdb import HyperDB

past_memories = [
    "USER: Hey Mary! It's been a bit. How are you?",
    "ASSISTANT: Good! Have you checked out any new games lately?",
    "USER: Sure have. I'm playing one called Armored Core 6. Have you heard about it?",
    "ASSISTANT: Nope, not yet. But I'm always open to trying new games!",
    "USER: Have you been playing anything new?",
    "ASSISTANT: Yeah, actually! I discovered this game called Flower, where you control the wind through a beautiful "
    "garden. It was so peaceful and calming.",
]

brain = HyperDB(past_memories)

brain.add_documents(
    [
        "USER: Just playing some videogames. I'm playing Genshin Impact. I want to get Lady Furina soon!",
        "ASSISTANT: That's great, boss! It's always important to rest.",
        "USER: Thanks! Aw shoot, I just realized I've run out of watermelon."
        " I need to buy some the next time I go grocery shopping.",
        "ASSISTANT: Sounds good! Do you want to go back to playing videogames?",
        "USER: Yup!"
    ]
)

brain.save("memory_pickles/mary_memories.pickle.gz")
