import streamlit as st
import random
import time

class Player:
    def __init__(self, name):
        self.name = name
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
        self.log = [f"{name} is born in 550 BC in Athens."]  # Event log
        
        # Random parents' profession and class
        professions = ["Farmer", "Soldier", "Merchant", "Artisan", "Priest", "Scholar"]
        classes = ["Peasant", "Citizen", "Noble", "Slave"]
        self.mother_profession = random.choice(professions)
        self.mother_class = random.choice(classes)
        self.father_profession = random.choice(professions)
        self.father_class = random.choice(classes)
        self.log.append(f"Mother: {self.mother_class} {self.mother_profession}")
        self.log.append(f"Father: {self.father_class} {self.father_profession}")

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

def main():
    st.title("Ancient World RPG Simulator")
    
    if 'player' not in st.session_state:
        with st.form(key='start_form'):
            name = st.text_input("Enter your name:", "Player")
            submit = st.form_submit_button("Start Game")
            if submit:
                st.session_state.player = Player(name)
                st.session_state.current_menu = 'main'
                st.session_state.sub_menu = None
                st.session_state.game_over = False
                st.rerun()
        return

    player = st.session_state.player
    if st.session_state.game_over:
        st.write("You have died. Game over.")
        if st.button("Restart"):
            del st.session_state.player
            st.rerun()
        return

    # Display Log
    st.subheader("Log")
    for entry in player.log[-5:]:
        st.write(entry)

    # Display Status
    st.subheader("Status")
    year_str = f"{abs(player.year)} BC" if player.year < 0 else f"{player.year} AD"
    career = f"{player.career_path} - {career_paths[player.career_path][player.career_level]}" if player.career_path else "None"
    education = f"{player.education_path} - {education_paths[player.education_path][player.education_level]}" if player.education_path else "None"
    st.write(f"Name: {player.name}")
    st.write(f"Year: {year_str}")
    st.write(f"Age: {player.age} ({player.life_stage})")
    st.write(f"Location: {player.location}")
    st.write(f"Religion: {player.religion}")
    st.write(f"Cult Member: {'Yes' if player.cult_member else 'No'}")
    st.write(f"Career: {career}")
    st.write(f"Education: {education}")
    st.write(f"Wealth: {player.wealth} coins")
    st.write("Stats:")
    st.write(f"Hygiene: {display_bar(player.hygiene)} ({player.hygiene}/100)")
    st.write(f"Health: {display_bar(player.health)} ({player.health}/100)")
    st.write(f"Strength: {display_bar(player.strength)} ({player.strength}/100)")
    st.write(f"Intelligence: {display_bar(player.intelligence)} ({player.intelligence}/100)")
    st.write(f"Parents:")
    st.write(f"Mother: {player.mother_class} {player.mother_profession}")
    st.write(f"Father: {player.father_class} {player.father_profession}")

    # Main Menu
    st.subheader("Main Menu")
    menu_options = [
        "Relationships", "Travel/Pilgrimage", "Activities", "Shop/Taxes",
        "Career/Education", "Options", "Combat", "Age Up"
    ]
    for option in menu_options:
        if st.button(option):
            st.session_state.current_menu = option.lower().replace("/", "_")
            st.session_state.sub_menu = None
            st.rerun()

    if st.button("Quit"):
        st.session_state.game_over = True
        st.rerun()

    # Handle Menus
    current_menu = st.session_state.current_menu

    if current_menu == 'relationships':
        relationships_menu(player)
    elif current_menu == 'travel_pilgrimage':
        travel_menu(player)
    elif current_menu == 'activities':
        activities_menu(player)
    elif current_menu == 'shop_taxes':
        shop_taxes_menu(player)
    elif current_menu == 'career_education':
        career_education_menu(player)
    elif current_menu == 'options':
        options_menu(player)
    elif current_menu == 'combat':
        combat_menu(player)
    elif current_menu == 'age_up':
        if player.age_up():
            st.session_state.game_over = True
        st.session_state.current_menu = 'main'
        st.rerun()

def back_to_main():
    if st.button("Back"):
        st.session_state.current_menu = 'main'
        st.session_state.sub_menu = None
        st.rerun()

def relationships_menu(player):
    if player.life_stage in ["Infancy", "Childhood"]:
        st.write("Too young for complex relationships.")
        back_to_main()
        return
    st.subheader("Relationships")
    for name, level in player.relationships.items():
        st.write(f"{name}: {level}/100")
    
    selected_person = st.selectbox("Select person to interact:", list(player.relationships.keys()) + ["Back"])
    if selected_person == "Back":
        st.session_state.current_menu = 'main'
        st.rerun()
        return
    if selected_person:
        st.write(f"Interacting with {selected_person}:")
        action = st.selectbox("Choose action:", ["Converse (increase relationship)", "Argue (decrease relationship)", "Fun activity (random effect)", "Back"])
        if action == "Converse (increase relationship)":
            player.relationships[selected_person] += random.randint(5, 15)
            if player.relationships[selected_person] > 100:
                player.relationships[selected_person] = 100
            player.log.append(f"Conversed with {selected_person}, relationship up.")
            st.rerun()
        elif action == "Argue (decrease relationship)":
            player.relationships[selected_person] -= random.randint(5, 15)
            if player.relationships[selected_person] < 0:
                player.relationships[selected_person] = 0
            player.log.append(f"Argued with {selected_person}, relationship down.")
            st.rerun()
        elif action == "Fun activity (random effect)":
            effect = random.choice(["up", "down"])
            if effect == "up":
                player.relationships[selected_person] += 10
                player.log.append(f"Fun activity with {selected_person} went well.")
            else:
                player.relationships[selected_person] -= 10
                player.log.append(f"Fun activity with {selected_person} went poorly.")
            st.rerun()
        elif action == "Back":
            back_to_main()

def travel_menu(player):
    if player.life_stage in ["Infancy"]:
        st.write("Too young to travel.")
        back_to_main()
        return
    st.subheader("Travel / Pilgrimage")
    action = st.selectbox("Choose:", ["Travel to new city (costs 20 wealth)", "Go on pilgrimage (increases health/intelligence)", "Back"])
    if action == "Travel to new city (costs 20 wealth)":
        if player.wealth >= 20:
            cities = ["Rome", "Sparta", "Babylon", "Alexandria"]
            new_city = random.choice(cities)
            player.location = new_city
            player.wealth -= 20
            player.log.append(f"Traveled to {new_city}.")
            st.rerun()
        else:
            st.write("Not enough wealth.")
    elif action == "Go on pilgrimage (increases health/intelligence)":
        player.health += 10
        player.intelligence += 5
        player.log.append("Went on pilgrimage, feel refreshed.")
        st.rerun()
    elif action == "Back":
        back_to_main()

def activities_menu(player):
    if player.life_stage in ["Infancy"]:
        st.write("Too young for activities.")
        back_to_main()
        return
    st.subheader("Ancient Activities")
    action = st.selectbox("Choose:", ["Attend festival (fun, relationship chance)", "Participate in games (increase strength)", "Maintain hygiene (bath)", "Back"])
    if action == "Attend festival (fun, relationship chance)":
        player.log.append("Attended festival.")
        if random.random() < 0.5:
            new_friend = random.choice(["Theodoros", "Sophia"])
            player.relationships[new_friend] = 40
            player.log.append(f"Made a new friend: {new_friend}.")
        st.rerun()
    elif action == "Participate in games (increase strength)":
        player.strength += 10
        player.log.append("Participated in games, strength increased.")
        st.rerun()
    elif action == "Maintain hygiene (bath)":
        player.hygiene += 20
        if player.hygiene > 100:
            player.hygiene = 100
        player.log.append("Took a bath, hygiene improved.")
        st.rerun()
    elif action == "Back":
        back_to_main()

def shop_taxes_menu(player):
    if player.life_stage in ["Infancy", "Childhood"]:
        st.write("Too young for shopping/taxes.")
        back_to_main()
        return
    st.subheader("Shopping / Taxes")
    action = st.selectbox("Choose:", ["Shop for items (increase stats)", "Pay taxes (mandatory sometimes)", "Back"])
    if action == "Shop for items (increase stats)":
        buy_option = st.selectbox("Buy:", ["Food (health +10, 10 coins)", "Tools (strength +5, 15 coins)", "Back"])
        if buy_option == "Food (health +10, 10 coins)":
            if player.wealth >= 10:
                player.health += 10
                player.wealth -= 10
                player.log.append("Bought food.")
                st.rerun()
            else:
                st.write("Not enough wealth.")
        elif buy_option == "Tools (strength +5, 15 coins)":
            if player.wealth >= 15:
                player.strength += 5
                player.wealth -= 15
                player.log.append("Bought tools.")
                st.rerun()
            else:
                st.write("Not enough wealth