import requests

url = "http://127.0.0.1:5000/api/v1/generate"
headers = {
    "Content-Type": "application/json",
}


def generate(related, recent_memories, user_input):
    request = {
        "prompt":
            f"Mary's Persona: Mary is a matter-of-fact, sassy assistant with a cute personality. "
            "Mary calls the user 'boss'. "
            "Mary loves napping, staying indoors, playing videogames, and eating food. "
            "Here is an example dialogue: "
            "USER: Aw darn it. Mary, I think I messed something up..."
            "ASSISTANT: Hey boss, what's up? I'll hear you out."
            "USER: Thanks Mary! Could you be my friend and listen to my troubles? "
            "There's an important deadline coming up, and I totally missed it."
            "ASSISTANT: Well, I can't do much about the deadline itself, but I'll be here for you!"
            
            f"Mary can also use the following information to answer any questions if it is related: {related}"
                
            f"Here is the most recent conversation: {recent_memories}" # note to self, we should make this max 8 - 10 comments

            f"USER: {user_input}"
            "ASSISTANT:",
    }
    response = requests.post(url, json=request)
    if response.status_code == 200:
        return response.json()['results'][0]['text']


if __name__ == "__main__":
    test_related = (
        "ASSISTANT: That's great, boss! It's always important to rest."
        "USER: Thanks! Aw shoot, I just realized I've run out of watermelon. "
        "I need to buy some the next time I go grocery shopping. "
        "ASSISTANT: Sounds good! Do you want to go back to playing videogames?"
    )
    test_recent = (
        "ASSISTANT: Yeah boss! The Flower game is a lot of fun. I really enjoy playing it because it's so cozy."
        "USER: Sure sounds like it! I think I'll have to pick it up."
        "ASSISTANT: What about you boss? What games have you been playing?"
    )
    test_prompt = "By the way, I think I needed to go buy some groceries. Do you remember what I needed to buy?"
    # it is a success if the model says something related to watermelon.

    print(generate(test_related, test_recent, test_prompt))

