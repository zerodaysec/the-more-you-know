import streamlit as st
import json

st.title("Subscription Manager")


# Function to load notes from JSON file
def load_notes():
    with open("/notes.json", "r") as f:
        return json.load(f)


# Function to save notes to JSON file
def save_notes(notes):
    with open("/notes.json", "w") as f:
        json.dump(notes, f, indent=4)


# Load data form notes
notes = load_notes()

# load categories
categories = []
for note in notes:
    for cat in note["categories"]:
        if cat.lower() not in categories:
            categories.append(cat.lower())

categories.sort()
# categories = list(set(categories))


results = {}
for cat in categories:
    cat = cat.lower()
    results[cat] = st.checkbox(cat, key=str(cat))

selected_cats = []
for answer in results:
    if results[answer]:
        selected_cats.append(answer)

selected_cats.sort()
st.write(f"Selected categories are {selected_cats}")
