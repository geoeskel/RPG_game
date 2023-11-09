import random
import sys

# Define the Character class
class Character:
    def __init__(self, name, health, base_damage, ascii_art):
        self.name = name
        self.health = health
        self.base_damage = base_damage  # Base damage, to be randomized
        self.ascii_art = ascii_art

    def attack(self, other):
        # Randomize damage within a range of 80% to 120% of base damage
        damage_dealt = random.randint(int(self.base_damage * 0.8), int(self.base_damage * 1.2))
        other.health -= damage_dealt
        return damage_dealt

    def is_alive(self):
        return self.health > 0

# Define the NPC class
class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue

    def speak(self):
        print(f"{self.name} says: '{random.choice(self.dialogue)}'")

# Define the Monster class
class Monster(Character):
    def __init__(self, name, health, base_damage, defeat_message, ascii_art):
        super().__init__(name, health, base_damage, ascii_art)
        self.defeat_message = defeat_message

    def display(self):
        print(self.ascii_art)

# Define the Player class
class Player(Character):
    def __init__(self, name, health, base_damage):
        super().__init__(name, health, base_damage, '')

    def choose_action(self, opponent):
        action = input("Do you want to (A)ttack or (R)un away? ").lower()
        if action == "a":
            damage_dealt = self.attack(opponent)
            print(f"You attack the {opponent.name} for {damage_dealt} damage.")
        elif action == "r":
            if random.random() < 0.5:
                print("You managed to escape!")
                return "escaped"
            else:
                print("You failed to escape!")
        else:
            print("Invalid action.")
        return "fight"


# ASCII art for monsters
goblin_ascii = """
    ,      ,
   /(.-""-.)\\
   |\ \/      \/ /|
   | \ / =.  .= \ / |
   \( \   o\/o   / )/
    \_, '-/  \-' ,_/
      /   \__/   \\
      \,___/\___,/
  __/             \__
"""

troll_ascii = """
     /\\  /\\
    //\\\\_//\\\\
    \_         _/
   / *         * \\
  /  \_/   \_/  \
  \__/  \__/ \__/
      \__/\__/
      \_\/_/
      /     \\
     /_'---'\_\\
"""

dragon_ascii = """
                  ______________
   ,===:'.,            `-._
        `:.`---.__         `-._
          `:.     `--.         `.
            \.        `.         `.
    (,,(,    \.         `.   ____,-`.,
 (,'     `/   \.   ,--.___`.'
 ,  ,'  ,--.  `,   \.;'         `
  `{D, {    \  :    \;
    V,,'    /  /    //
    j;;    /  ,' ,-//.    ,---.      ,
    \;'   /  ,' /  _  \  /  _  \   ,'/
          \   `'  / \  `'  / \  `.' /
           `.___,'   `.__,'   `.__,'  
"""

# Define a function to start the game
def start_game():
    characters = [
        Player("Warrior", 120, 15),
        Player("Mage", 100, 20),
        Player("Rogue", 110, 18)
    ]

    npcs = [
        NPC("Old Man", ["The end is near...", "Beware of the dark forest..."]),
        NPC("Merchant", ["I have potions for sale.", "Looking for weapons? I have some."])
    ]

    monsters = [
        Monster("Goblin", 30, 5, "The goblin is defeated!", goblin_ascii),
        Monster("Troll", 50, 10, "The troll won't bother anyone anymore.", troll_ascii),
        # Not including the Dragon here, he will be a separate encounter
    ]

    # The boss Dragon
    dragon = Monster("Dragon", 200, 30, "The dragon is slain! You are victorious!", dragon_ascii)

    print("Welcome to the RPG Text Game!")
    print("Choose your character:")
    for i, character in enumerate(characters):
        print(f"{i + 1}. {character.name} - Health: {character.health}, Damage: {character.base_damage}")

    choice = int(input("Enter the number of your character: "))
    player = characters[choice - 1]
    print(f"You have chosen the {player.name}.")

    encounters_before_boss = 5
    while player.is_alive() and encounters_before_boss > 0:
        encounter = random.choice(npcs + monsters)
        if isinstance(encounter, NPC):
            encounter.speak()
        elif isinstance(encounter, Monster):
            encounter.display()
            print(f"A wild {encounter.name} appears!")
            while encounter.is_alive() and player.is_alive():
                action = player.choose_action(encounter)
                if action == "escaped":
                    break
                if encounter.is_alive():
                    damage_dealt = encounter.attack(player)
                    print(f"The {encounter.name} attacks you for {damage_dealt} damage.")
                else:
                    print(encounter.defeat_message)
                    player.base_damage += 2  # Player gets stronger after defeating a monster
                    player.health += 20
            if not player.is_alive():
                print("You have been defeated! Game Over.")
                sys.exit()
        encounters_before_boss -= 1
        input("Press Enter to continue...")

    if player.is_alive():
        dragon.display()
        print("A massive dragon looms before you, the final challenge!")
        while dragon.is_alive() and player.is_alive():
            action = player.choose_action(dragon)
            if action == "escaped":
                print("There's no escaping the dragon!")
            if dragon.is_alive():
                damage_dealt = dragon.attack(player)
                print(f"The {dragon.name} engulfs you in flames for {damage_dealt} damage.")
            else:
                print(dragon.defeat_message)
                print("You have defeated the mighty dragon and saved the kingdom!")
                break
        if not player.is_alive():
            print("You have been defeated by the dragon! Game Over.")

# Start the game
if __name__ == "__main__":
    start_game()