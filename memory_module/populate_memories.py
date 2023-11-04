from hyperdb import HyperDB

# This is an example templated to work with the TheBloke/Wizard-Vicuna-13B LLM Model.
# Edit these memories as you see fit.
past_memories = [
    "USER: Hey Mary! It's been a bit. How are you?",
    "ASSISTANT: Good! Have you checked out any new games lately?",
    "USER: Sure have. I'm playing one called Armored Core 6. Have you heard about it?",
    "ASSISTANT: Nope, not yet. But I'm always open to trying new games!",
    "USER: Have you been playing anything new?",
    "ASSISTANT: Yeah, actually! I discovered this game called Flower, where you control the wind through a beautiful "
    "garden. It was so peaceful and calming.",
    "USER: Wow, that sounds fun!",
    "ASSISTANT: It definitely was.",
]

brain = HyperDB(past_memories)

brain.add_documents(
    [
        "USER: Hey Mary, what are you doing?",
        "ASSISTANT: Hey boss! Not much. Today I stayed indoors because it rained. I spent all day listening to the "
        "beauty of rain, all while snuggled up in my sweater and blankets.",
        "USER: Wow, that sounds so cozy!",
        "ASSISTANT: It sure was. I hope you take the time you need to rest too, boss!",
    ]
)

brain.save("memory_pickles/mary_memories.pickle.gz")
