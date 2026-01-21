import streamlit as st
import random

st.set_page_config(page_title="Ancient Fates", layout="centered")

# =====================================================
# INITIAL SETUP
# =====================================================

if "dynasty" not in st.session_state:
    st.session_state.dynasty = []

if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Founder",
        "age": 16,
        "culture": "Roman",
        "title": "Citizen",
        "religion": "Traditional Gods",
        "province": {
            "name": "Latium",
            "stability": 70,
            "wealth": 60,
            "revolt": 10
        },
        "stats": {
            "charisma": 50,
            "fitness": 50,
            "health": 65,
            "intelligence": 50,
            "emotional": 60
        },
        "personality": {
            "ambition": 50,
            "discipline": 50,
            "honor": 50,
            "ruthlessness": 30,
            "spirituality": 40
        },
        "influence": 0,
        "children": [],
        "alive": True,
        "year": 1
    }

p = st.session_state.player

# =====================================================
# UTILITY
# =====================================================

def year_pass():
    p["age"] += 1
    p["year"] += 1

    # province decay
    p["province"]["stability"] -= random.randint(0, 3)
    p["province"]["revolt"] += random.randint(0, 2)

    # emotional decay
    if p["influence"] > 40:
        p["stats"]["emotional"] -= 1

def record_dynasty():
    st.session_state.dynasty.append({
        "name": p["name"],
        "age": p["age"],
        "title": p["title"],
        "influence": p["influence"]
    })

def death_check():
    if p["stats"]["health"] <= 0 or p["age"] > 85:
        p["alive"] = False
        record_dynasty()

# =====================================================
# EVENTS
# =====================================================

def random_event():
    roll = random.random()

    if roll < 0.15:
        st.warning("☠️ A sickness spreads.")
        p["stats"]["health"] -= random.randint(3, 10)

    elif roll < 0.25:
        st.info("🗡 An assassination attempt!")
        if random.random() < 0.5:
            st.error("You were wounded.")
            p["stats"]["health"] -= 8
        else:
            st.success("You survived.")

    elif roll < 0.35:
        st.info("🌾 A good harvest increases wealth.")
        p["province"]["wealth"] += 5

    elif roll < 0.45:
        st.warning("🔥 Unrest grows in the province.")
        p["province"]["revolt"] += 10

# =====================================================
# ACTIONS
# =====================================================

def train():
    p["stats"]["fitness"] += 3
    p["personality"]["discipline"] += 2
    year_pass()
    random_event()

def govern():
    p["province"]["stability"] += 5
    p["influence"] += 2
    year_pass()
    random_event()

def scheme():
    if random.random() < 0.5:
        p["influence"] += 4
        p["personality"]["ruthlessness"] += 3
        st.success("Your intrigue succeeds.")
    else:
        p["stats"]["emotional"] -= 5
        st.error("Your plot is exposed.")
    year_pass()
    random_event()

def war():
    power = p["stats"]["fitness"] + p["stats"]["intelligence"] + p["influence"]
    enemy = random.randint(80, 150)

    if power > enemy:
        st.success("⚔️ You win the war.")
        p["title"] = "Imperial Ruler" if p["culture"] == "Roman" else "High King"
        p["influence"] += 10
        p["province"]["stability"] += 10
    else:
        st.error("💀 Defeat in war.")
        p["stats"]["health"] -= random.randint(10, 25)
        p["province"]["stability"] -= 10

    year_pass()
    random_event()

def council_vote():
    support = p["stats"]["charisma"] + p["influence"]
    oppose = random.randint(60, 140)

    if support > oppose:
        st.success("🏛 Council supports your reforms.")
        p["influence"] += 5
        p["province"]["stability"] += 5
    else:
        st.error("The council rejects you.")
        p["province"]["revolt"] += 10
    year_pass()
    random_event()

def family_time():
    if random.random() < 0.4:
        child = {
            "name": f"Child of {p['name']}",
            "stats": {k: int(v * random.uniform(0.4,0.7)) for k,v in p["stats"].items()},
            "personality": {k: int(v * random.uniform(0.4,0.7)) for k,v in p["personality"].items()}
        }
        p["children"].append(child)
        st.success("👶 A child is born.")
    year_pass()

# =====================================================
# UI
# =====================================================

st.title("🏺 Ancient Fates: Blood & Empire")

if not p["alive"]:
    st.header("⚰️ Your ruler has died.")
    if p["children"]:
        if st.button("Continue as Heir"):
            heir = random.choice(p["children"])
            st.session_state.player = {
                "name": heir["name"],
                "age": 16,
                "culture": p["culture"],
                "title": "Heir",
                "religion": p["religion"],
                "province": p["province"],
                "stats": heir["stats"],
                "personality": heir["personality"],
                "influence": p["influence"] // 2,
                "children": [],
                "alive": True,
                "year": 1
            }
            st.experimental_rerun()
    else:
        st.write("Your dynasty has ended.")
    st.stop()

st.subheader(f"{p['name']} — Age {p['age']} — {p['title']}")

st.write(f"**Province:** {p['province']['name']}")
st.write(f"Stability: {p['province']['stability']} | Revolt Risk: {p['province']['revolt']}")

st.write(f"**Influence:** {p['influence']} | Religion: {p['religion']}")
st.write(f"**Children:** {len(p['children'])}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("⚔ Train"):
        train()
    if st.button("🏛 Govern Province"):
        govern()
    if st.button("🕸 Political Scheme"):
        scheme()

with col2:
    if st.button("⚔ Declare War"):
        war()
    if st.button("🏛 Council Vote"):
        council_vote()
    if st.button("❤️ Family Time"):
        family_time()

death_check()

st.divider()

st.subheader("📜 Dynasty Chronicle")
for d in st.session_state.dynasty:
    st.write(f"{d['name']} — {d['title']} — Age {d['age']}")