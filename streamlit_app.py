import random

class Player:
    def __init__(self):
        self.year = -550  # 550 BC
        self.age = 0
        self.life_stage = "Infancy"
        self.hygiene = 50  # 0-100
        self.health = 100  # 0-100
        self.strength = 50  # 0-100
        self.intelligence = 50  # 0-100
        self.wealth = 100  # Starting coins or something
        self.location = "Athens"  # Starting location, can change
        self.religion = "Greek Polytheism"  # Default
        self.cult_member = False
        self.career_path = None
        self.career_level = 0
        self.education_path = None
        self.education_level = 0
        self.relationships = {
            "Mother": 80,
            "Father": 80
        }
        self.log = ["You are born in 550 BC in Athens."]  # Event log

    def update_life_stage(self):
        if self.age < 5:
            self.life_stage = "Infancy"
        elif self.age < 13:
            self.life_stage = "Childhood"
        elif self.age < 18:
            self.life_stage = "Adolescence"
        elif self.age < 50:
            self.life_stage = "Adulthood"
        else:
            self.life_stage = "Old Age"

    def age_up(self):
        self.age += 1
        self.year += 1
        self.update_life_stage()
        # Age-based effects
        if self.life_stage == "Old Age":
            self.health -= random.randint(1, 5)  # Faster health decay
            self.strength -= random.randint(1, 3)
        # Random events
        events = [
            "A good harvest increases your wealth.",
            "You fall ill, health decreases.",
            "You make a new friend.",
            "Taxes are due, wealth decreases."
        ]
        event = random.choice(events)
        self.log.append(event)
        if "wealth increases" in event:
            self.wealth += 20
        elif "health decreases" in event:
            self.health -= 10
        elif "new friend" in event:
            new_friend = random.choice(["Alexandros", "Helena", "Marcus"])
            self.relationships[new_friend] = 50
        elif "wealth decreases" in event:
            self.wealth -= 10
        # Natural decay
        self.hygiene -= 5
        if self.hygiene < 0:
            self.hygiene = 0
        # Death chance
        death_chance = 0.05 + (self.age / 2000)  # Increases with age, low at young
        if self.life_stage == "Old Age":
            death_chance += 0.1
        if self.health < 20:
            death_chance += 0.2
        if random.random() < death_chance:
            return True  # Game over
        # Promotion chance if in career
        if self.career_path and self.career_level < len(career_paths[self.career_path]) - 1:
            if random.random() < 0.1 + (self.strength + self.intelligence) / 400:  # 10% base + stats
                self.career_level += 1
                self.log.append(f"Promoted in {self.career_path} to {career_paths[self.career_path][self.career_level]}.")
                self.wealth += 50  # Promotion bonus
        return False

career_paths = {
    "Military": ["Recruit", "Legionary", "Centurion", "Tribune", "General"],
    "Philosophy": ["Student", "Disciple", "Philosopher", "Sage"],
    "Merchant": ["Apprentice", "Trader", "Merchant", "Tycoon"],
    "Agriculture": ["Peasant", "Farmer", "Landowner"],
    "Priesthood": ["Acolyte", "Priest", "High Priest"],
    "Artisan": ["Apprentice", "Craftsman", "Master Craftsman"]
}

education_paths = {
    "Basic": ["None", "Literacy", "Arithmetic"],
    "Rhetoric": ["None", "Basic Speaking", "Advanced Rhetoric", "Oratory"],
    "Philosophy": ["None", "Ethics", "Logic", "Metaphysics"],
    "Military": ["None", "Tactics", "Strategy", "Leadership"]
}

def display_bar(value):
    bars = int(value / 10)
    return '|' * bars + '-' * (10 - bars)

def display_status(player):
    year_str = f"{abs(player.year)} BC" if player.year < 0 else f"{player.year} AD"
    career = f"{player.career_path} - {career_paths[player.career_path][player.career_level]}" if player.career_path else "None"
    education = f"{player.education_path} - {education_paths[player.education_path][player.education_level]}" if player.education_path else "None"
    print(f"\n=== Status ===\nYear: {year_str}\nAge: {player.age} ({player.life_stage})\nLocation: {player.location}\nReligion: {player.religion}\nCult Member: {'Yes' if player.cult_member else 'No'}\nCareer: {career}\nEducation: {education}\nWealth: {player.wealth} coins")
    print("\nStats:")
    print(f"Hygiene: {display_bar(player.hygiene)} ({player.hygiene}/100)")
    print(f"Health: {display_bar(player.health)} ({player.health}/100)")
    print(f"Strength: {display_bar(player.strength)} ({player.strength}/100)")
    print(f"Intelligence: {display_bar(player.intelligence)} ({player.intelligence}/100)")

def display_log(player):
    print("\n=== Log ===\n")
    for entry in player.log[-5:]:  # Last 5 events
        print(entry)
    print("\n")

def relationships_menu(player):
    if player.life_stage in ["Infancy", "Childhood"]:
        print("Too young for complex relationships.")
        return
    while True:
        print("\n=== Relationships ===\n")
        for name, level in player.relationships.items():
            print(f"{name}: {level}/100")
        print("\nOptions: Enter name to interact, or 'back' to return.")
        choice = input("> ").strip()
        if choice.lower() == 'back':
            return
        if choice in player.relationships:
            while True:
                print(f"\nInteracting with {choice}:")
                print("1. Converse (increase relationship)")
                print("2. Argue (decrease relationship)")
                print("3. Fun activity (random effect)")
                print("back")
                action = input("> ").strip()
                if action.lower() == 'back':
                    break
                elif action == '1':
                    player.relationships[choice] += random.randint(5, 15)
                    if player.relationships[choice] > 100:
                        player.relationships[choice] = 100
                    player.log.append(f"Conversed with {choice}, relationship up.")
                elif action == '2':
                    player.relationships[choice] -= random.randint(5, 15)
                    if player.relationships[choice] < 0:
                        player.relationships[choice] = 0
                    player.log.append(f"Argued with {choice}, relationship down.")
                elif action == '3':
                    effect = random.choice(["up", "down"])
                    if effect == "up":
                        player.relationships[choice] += 10
                        player.log.append(f"Fun activity with {choice} went well.")
                    else:
                        player.relationships[choice] -= 10
                        player.log.append(f"Fun activity with {choice} went poorly.")

def travel_menu(player):
    if player.life_stage in ["Infancy"]:
        print("Too young to travel.")
        return
    print("\n=== Travel / Pilgrimage ===\n")
    print("1. Travel to new city (costs 20 wealth)")
    print("2. Go on pilgrimage (increases health/intelligence)")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        cities = ["Rome", "Sparta", "Babylon", "Alexandria"]
        new_city = random.choice(cities)
        player.location = new_city
        player.wealth -= 20
        player.log.append(f"Traveled to {new_city}.")
    elif choice == '2':
        player.health += 10
        player.intelligence += 5
        player.log.append("Went on pilgrimage, feel refreshed.")

def activities_menu(player):
    if player.life_stage in ["Infancy"]:
        print("Too young for activities.")
        return
    print("\n=== Ancient Activities ===\n")
    print("1. Attend festival (fun, relationship chance)")
    print("2. Participate in games (increase strength)")
    print("3. Maintain hygiene (bath)")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        player.log.append("Attended festival.")
        if random.random() < 0.5:
            new_friend = random.choice(["Theodoros", "Sophia"])
            player.relationships[new_friend] = 40
            player.log.append(f"Made a new friend: {new_friend}.")
    elif choice == '2':
        player.strength += 10
        player.log.append("Participated in games, strength increased.")
    elif choice == '3':
        player.hygiene += 20
        if player.hygiene > 100:
            player.hygiene = 100
        player.log.append("Took a bath, hygiene improved.")

def shop_taxes_menu(player):
    if player.life_stage in ["Infancy", "Childhood"]:
        print("Too young for shopping/taxes.")
        return
    print("\n=== Shopping / Taxes ===\n")
    print("1. Shop for items (increase stats)")
    print("2. Pay taxes (mandatory sometimes)")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        print("Buy: 1. Food (health +10, 10 coins), 2. Tools (strength +5, 15 coins)")
        buy = input("> ").strip()
        if buy == '1' and player.wealth >= 10:
            player.health += 10
            player.wealth -= 10
            player.log.append("Bought food.")
        elif buy == '2' and player.wealth >= 15:
            player.strength += 5
            player.wealth -= 15
            player.log.append("Bought tools.")
    elif choice == '2':
        tax = random.randint(5, 20)
        player.wealth -= tax
        player.log.append(f"Paid {tax} in taxes.")

def career_education_menu(player):
    if player.life_stage in ["Infancy", "Childhood"] and player.age < 7:
        print("Too young for career/education.")
        return
    print("\n=== Career / Education ===\n")
    print("1. Education (choose path and advance)")
    print("2. Career (choose path and manage)")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        if not player.education_path:
            print("Choose education path: 1. Basic, 2. Rhetoric, 3. Philosophy, 4. Military")
            path_choice = input("> ").strip()
            paths = ['Basic', 'Rhetoric', 'Philosophy', 'Military']
            if path_choice in ['1', '2', '3', '4']:
                player.education_path = paths[int(path_choice) - 1]
                player.log.append(f"Started education in {player.education_path}.")
        else:
            if player.education_level < len(education_paths[player.education_path]) - 1:
                cost = 10 + player.education_level * 5
                if player.wealth >= cost and random.random() < 0.5 + player.intelligence / 200:
                    player.education_level += 1
                    player.wealth -= cost
                    player.intelligence += 10
                    player.log.append(f"Advanced in {player.education_path} to {education_paths[player.education_path][player.education_level]}.")
                else:
                    player.log.append("Failed to advance in education.")
    elif choice == '2':
        if player.age < 18:
            print("Too young for career.")
            return
        if not player.career_path:
            print("Choose career path: 1. Military, 2. Philosophy, 3. Merchant, 4. Agriculture, 5. Priesthood, 6. Artisan")
            path_choice = input("> ").strip()
            paths = list(career_paths.keys())
            if path_choice in ['1', '2', '3', '4', '5', '6']:
                player.career_path = paths[int(path_choice) - 1]
                player.log.append(f"Started career in {player.career_path} as {career_paths[player.career_path][0]}.")
        else:
            print(f"Current career: {player.career_path} - {career_paths[player.career_path][player.career_level]}")
            print("1. Work (earn wealth)")
            print("2. Seek promotion (if eligible)")
            action = input("> ").strip()
            if action == '1':
                earnings = 10 + player.career_level * 5 + player.strength / 10 if "Military" in player.career_path else player.intelligence / 10
                player.wealth += int(earnings)
                player.log.append(f"Worked, earned {int(earnings)} coins.")
            elif action == '2':
                if player.career_level < len(career_paths[player.career_path]) - 1:
                    if random.random() < 0.2 + (player.strength + player.intelligence) / 300:
                        player.career_level += 1
                        player.log.append(f"Promoted to {career_paths[player.career_path][player.career_level]}.")
                    else:
                        player.log.append("Promotion denied.")

def options_menu(player):
    print("\n=== Options ===\n")
    print("1. Exercise (strength +)")
    print("2. Hunting (strength/health)")
    print("3. Go to grove (relax)")
    print("4. Visit medicine man (health +)")
    print("5. Visit Druid/Temple (religion)")
    print("6. Change religion/join cult")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        player.strength += 5
        player.log.append("Exercised.")
    elif choice == '2':
        player.strength += 5
        if random.random() < 0.2:
            player.health -= 10
            player.log.append("Hunting injury.")
        else:
            player.log.append("Successful hunt.")
    elif choice == '3':
        player.health += 5
        player.log.append("Relaxed in the grove.")
    elif choice == '4':
        player.health += 10
        player.log.append("Visited medicine man.")
    elif choice == '5':
        player.health += 5
        player.log.append("Visited temple/Druid.")
    elif choice == '6':
        religions = ["Greek Polytheism", "Roman Polytheism", "Celtic Druidism", "Mystery Cult"]
        player.religion = random.choice(religions)
        if player.religion == "Mystery Cult":
            player.cult_member = True
        player.log.append(f"Changed to {player.religion}.")

def combat_menu(player):
    if player.life_stage in ["Infancy", "Childhood", "Old Age"]:
        print("Not suitable for combat.")
        return
    print("\n=== Combat ===\n")
    print("1. Train (increase strength)")
    print("2. Fight bandit (risk/reward)")
    print("3. Join battle (if in military)")
    print("back")
    choice = input("> ").strip()
    if choice == '1':
        player.strength += random.randint(5, 10)
        player.log.append("Trained in combat.")
    elif choice == '2':
        success_chance = player.strength / 100
        if random.random() < success_chance:
            player.wealth += random.randint(20, 50)
            player.log.append("Defeated bandit, gained wealth.")
        else:
            player.health -= random.randint(10, 30)
            player.wealth -= random.randint(5, 20)
            player.log.append("Lost to bandit, injured and lost wealth.")
    elif choice == '3':
        if player.career_path == "Military":
            success_chance = (player.strength + player.career_level * 10) / 100
            if random.random() < success_chance:
                player.wealth += 100
                player.strength += 5
                player.log.append("Victorious in battle.")
            else:
                player.health -= 20
                player.log.append("Defeated in battle, injured.")
        else:
            print("Not in military career.")

def main():
    player = Player()
    while player.health > 0:
        display_log(player)
        display_status(player)
        print("\n=== Main Menu ===\n1. Relationships\n2. Travel/Pilgrimage\n3. Activities\n4. Shop/Taxes\n5. Career/Education\n6. Options\n7. Combat\n8. Age Up\n9. Quit")
        choice = input("> ").strip()
        if choice == '1':
            relationships_menu(player)
        elif choice == '2':
            travel_menu(player)
        elif choice == '3':
            activities_menu(player)
        elif choice == '4':
            shop_taxes_menu(player)
        elif choice == '5':
            career_education_menu(player)
        elif choice == '6':
            options_menu(player)
        elif choice == '7':
            combat_menu(player)
        elif choice == '8':
            if player.age_up():
                print("You have died. Game over.")
                break
        elif choice == '9':
            break
    print("Game ended.")

if __name__ == "__main__":
    main()