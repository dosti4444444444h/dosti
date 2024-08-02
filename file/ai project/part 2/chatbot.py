import json
from textblob import TextBlob

class SimpleChatBot:
    def __init__(self, json_file='chatbot_data.json', sentiment_file='sentiment_data.json'):
        self.json_file = json_file
        self.sentiment_file = sentiment_file
        self.data = self.load_data()
        self.sentiment_data = self.load_sentiment_data()

    def load_data(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"pairs": []}

    def load_sentiment_data(self):
        try:
            with open(self.sentiment_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": []}

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def save_sentiment_data(self):
        with open(self.sentiment_file, 'w') as file:
            json.dump(self.sentiment_data, file, indent=4)

    def add_pair(self, prompt, response):
        self.data["pairs"].append({"prompt": prompt, "response": response})
        self.save_data()

    def re_add_pairs(self, prompt, new_response=None, delete=False):
        for pair in self.data["pairs"]:
            if pair["prompt"] == prompt:
                if delete:
                    self.data["pairs"].remove(pair)
                elif new_response:
                    pair["response"] = new_response
                self.save_data()
                return True
        return False

    def get_response(self, prompt):
        for pair in self.data["pairs"]:
            if pair["prompt"].lower() in prompt.lower():
                return pair["response"]
        return "I don't understand that."

    def interactively_add_pair(self):
        prompt = input("Enter the new prompt: ")
        response = input("Enter the response: ")
        self.add_pair(prompt, response)
        print(f"Added pair: '{prompt}' -> '{response}'")

    def interactively_rewrite_pair(self):
        if not self.data["pairs"]:
            print("No pairs available to rewrite.")
            return
        
        print("Available prompts:")
        for i, pair in enumerate(self.data["pairs"], 1):
            print(f"{i}. {pair['prompt']}")
        
        prompt = input("Enter the exact prompt of the pair you want to rewrite: ")
        new_response = input("Enter the new response: ")
        
        if self.re_add_pairs(prompt, new_response):
            print(f"Rewritten pair: '{prompt}' -> '{new_response}'")
        else:
            print(f"No pair found with the prompt '{prompt}'")

    def interactively_delete_pair(self):
        if not self.data["pairs"]:
            print("No pairs available to delete.")
            return

        print("Available prompts:")
        for i, pair in enumerate(self.data["pairs"], 1):
            print(f"{i}. {pair['prompt']}")
        
        prompt = input("Enter the exact prompt of the pair you want to delete: ")
        
        if self.re_add_pairs(prompt, delete=True):
            print(f"Deleted pair with prompt '{prompt}'")
        else:
            print(f"No pair found with the prompt '{prompt}'")

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "happy"
        elif analysis.sentiment.polarity < 0:
            return "sad"
        else:
            return "neutral"

    def interactively_analyze_sentiment(self):
        user_name = input("Enter your name: ")
        text = input("Tell me something about yourself: ")
        sentiment = self.analyze_sentiment(text)
        print(f"Based on what you wrote, you seem to be {sentiment}.")

        # Check if user already exists
        user_found = False
        for user in self.sentiment_data["users"]:
            if user["name"] == user_name:
                user["entries"].append({"text": text, "sentiment": sentiment})
                user_found = True
                break

        # If user does not exist, create a new entry
        if not user_found:
            new_user = {
                "name": user_name,
                "entries": [{"text": text, "sentiment": sentiment}]
            }
            self.sentiment_data["users"].append(new_user)
        
        self.save_sentiment_data()

    def sentiment_output(self):
        user_name = input("Enter the name to view sentiment output: ")
        
        for user in self.sentiment_data["users"]:
            if user["name"] == user_name:
                total_entries = len(user["entries"])
                if total_entries == 0:
                    print(f"No sentiment data available for {user_name}.")
                    return
                
                happy_count = sum(1 for entry in user["entries"] if entry["sentiment"] == "happy")
                sad_count = sum(1 for entry in user["entries"] if entry["sentiment"] == "sad")
                neutral_count = sum(1 for entry in user["entries"] if entry["sentiment"] == "neutral")
                
                print(f"Sentiment analysis for {user_name}:")
                print(f"Happy: {happy_count} ({happy_count / total_entries * 100:.2f}%)")
                print(f"Sad: {sad_count} ({sad_count / total_entries * 100:.2f}%)")
                print(f"Neutral: {neutral_count} ({neutral_count / total_entries * 100:.2f}%)")
                return
        
        print(f"No data found for user '{user_name}'.")

if __name__ == "__main__":
    bot = SimpleChatBot()

    print("Welcome to the Simple ChatBot! Type 'exit' to stop.")
    print("Type 'add' to add a new pair, 'rewrite' to modify an existing pair, 'delete' to remove a pair, 'sentiment' to analyze sentiment, 'sentiment output' to view sentiment ratios, or just chat!")

    user_input = input("You: ")
    while user_input.lower() != "exit":
        if user_input.lower() == "add":
            bot.interactively_add_pair()
        elif user_input.lower() == "rewrite":
            bot.interactively_rewrite_pair()
        elif user_input.lower() == "delete":
            bot.interactively_delete_pair()
        elif user_input.lower() == "sentiment":
            bot.interactively_analyze_sentiment()
        elif user_input.lower() == "sentiment output":
            bot.sentiment_output()
        else:
            print("Bot:", bot.get_response(user_input))
        
        user_input = input("You: ")

    print("Goodbye!")
