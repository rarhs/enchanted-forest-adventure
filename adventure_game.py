import anthropic
import json

client = anthropic.Anthropic()

class GameState:
    def __init__(self):
        self.location = "forest entrance"
        self.inventory = []
        self.health = 100
        self.score = 0
        self.objective = "Find the ancient artifact hidden in the forest."

    def to_dict(self):
        return {
            "location": self.location,
            "inventory": self.inventory,
            "health": self.health,
            "score": self.score,
            "objective": self.objective
        }

    def update(self, new_state_dict):
        self.location = new_state_dict.get("location", self.location)
        self.inventory = new_state_dict.get("inventory", self.inventory)
        self.health = new_state_dict.get("health", self.health)
        self.score = new_state_dict.get("score", self.score)
        self.objective = new_state_dict.get("objective", self.objective)

def generate_response(prompt, game_state):
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\nCurrent game state:\n{json.dumps(game_state.to_dict(), indent=2)}"
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"An error occurred while generating response: {e}")
        return "I'm sorry, I couldn't process that. Please try again."

def play_game():
    print("Welcome to the Enchanted Forest Adventure!")
    print("Your objective: Find the ancient artifact hidden in the forest.")
    print("Commands: 'look', 'inventory', 'health', 'score', 'quit'")
    print("Or type any action you want to perform.")
    
    game_state = GameState()
    
    while True:
        print(f"\nLocation: {game_state.location}")
        action = input("> ").strip().lower()
        
        if action == "quit":
            print("Thanks for playing!")
            break
        elif action == "inventory":
            print(f"Inventory: {', '.join(game_state.inventory) if game_state.inventory else 'Empty'}")
            continue
        elif action == "health":
            print(f"Health: {game_state.health}")
            continue
        elif action == "score":
            print(f"Score: {game_state.score}")
            continue
        
        prompt = f"""
        The player is in a text adventure game set in an enchanted forest. Their current action is: '{action}'.
        Based on the current game state and the player's action, provide a brief, engaging response describing what happens next.
        Then, update the game state to reflect any changes. Your response should be in the following JSON format:

        {{
            "response": "Your narrative response here",
            "new_state": {{
                "location": "new location if changed",
                "inventory": ["item1", "item2"],
                "health": new_health_value,
                "score": new_score_value,
                "objective": "updated objective if changed"
            }}
        }}

        Ensure that the "new_state" object contains all fields, even if they haven't changed.
        Be creative but consistent with previous responses. The game should be challenging but fair.
        """
        
        response = generate_response(prompt, game_state)
        
        try:
            response_data = json.loads(response)
            print(response_data["response"])
            game_state.update(response_data["new_state"])
        except json.JSONDecodeError:
            print("There was an error processing the game state. The adventure continues...")
            print(response)

if __name__ == "__main__":
    play_game()