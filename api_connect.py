import requests

# you can pretty much ignore this script. It didn't work out very well.
# I'm keeping it here mostly just in case it ever matters, *shrug emoji*

url = "http://127.0.0.1:5000/api/v1/chat"
headers = {
    "Content-Type": "application/json",
}
request_body = {
    "user_input": "Hey Mary, what groceries did I say I needed to buy?",
    "max_new_tokens": 250,
    "auto_max_new_tokens": False,
    "max_tokens_second": 0,
    "history": {"internal": [],
                "visible": []},
    "mode": "chat",
    "character": "Mary",
    "instruction_template": "Vicuna-v1.1",
    "your_name": "Fox",

    "regenerate": False,
    "_continue": False,
    "chat_instruct_command": "Continue the chat dialogue below. Write a single reply for the character 'Mary'.\n\n<|prompt|>",

    "preset": "None",
    "do_sample": True,
    "temperature": 0.35,
    "top_p": 0.1,
    "typical_p": 1,
    "epsilon_cutoff": 0,
    "eta_cutoff": 0,
    "tfs": 1,
    "top_a": 0,
    "repetition_penalty": 1.18,
    "repetition_penalty_range": 0,
    "top_k": 40,
    "min_length": 0,
    "no_repeat_ngram_size": 0,
    "num_beams": 1,
    "penalty_alpha": 0,
    "length_penalty": 1,
    "early_stopping": False,
    "mirostat_mode": 0,
    "mirostat_tau": 5,
    "mirostat_eta": 0.1,
    "guidance_scale": 1,
    "negative_prompt": "",

    "seed": -1,
    "add_bos_token": True,
    "truncation_length": 2048,
    "ban_eos_token": False,
    "custom_token_bans": "",
    "skip_special_tokens": True,
    "stopping_strings": []
}


def query_api():
    response = requests.post(url, json=request_body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    answer = query_api()
    print(answer)
