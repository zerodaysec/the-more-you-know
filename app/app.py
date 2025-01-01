import streamlit as st
import json
import pandas as pd


# Function to load notes from JSON file
def load_notes():
    with open("/notes.json", "r") as f:
        return json.load(f)


# Function to save notes to JSON file
def save_notes(notes):
    with open("/notes.json", "w") as f:
        json.dump(notes, f, indent=4)


# Load notes
notes = load_notes()

# Create a DataFrame from the notes
df = pd.DataFrame(notes)

# Create a map of category to icon
category_icon_map = {
    # "AWS": ":aws:",
    # "Azure": ":azure:",
    # "GCP": ":gcp:",
    "cloud": ":cloud:",
    "DevOps": ":hammer_and_wrench:",
    "security": ":shield:",
    "rss-feed": ":newspaper:",
    "podcast": ":microphone:",
    "video": ":video_camera:",
    "community": ":people_holding_hands:",
    # "code": ":code:",
    "TEST": ":science:",
    "architecture": ":building_construction:",
}

for note in notes:
    for cat in note["categories"]:
        if cat.lower() not in category_icon_map:
            category_icon_map[cat.lower()] = ":question:"

# Page selection
page = st.sidebar.selectbox("Choose a page", ["Home", "Add Entry"])

if page == "Home":
    notes = load_notes()
    # Sidebar for category selection
    st.sidebar.header("Filter by Categories")
    selected_categories = st.sidebar.multiselect(
        "Select categories",
        options=list(category_icon_map.keys()),
        default=list(category_icon_map.keys()),
    )

    # Filter notes based on selected categories
    filtered_notes = [
        note
        for note in notes
        if any(cat in note["categories"] for cat in selected_categories)
    ]

    # Display filtered notes as tiles (3x wide)
    tiles = []
    for note in filtered_notes:
        icons = " ".join([category_icon_map.get(cat, "") for cat in note["categories"]])
        tile_content = f"### {icons} {note['title']}\n"
        tile_content += f"[{note['link']}]({note['link']})\n"
        tile_content += f"{note['description']}\n"
        tiles.append(tile_content)

    # Create 3x wide grid
    for i in range(0, len(tiles), 3):
        col1, col2, col3 = st.columns(3)
        if i < len(tiles):
            col1.markdown(tiles[i])
        if i + 1 < len(tiles):
            col2.markdown(tiles[i + 1])
        if i + 2 < len(tiles):
            col3.markdown(tiles[i + 2])

    # Display filtered notes as a table, each category on its own row
    st.write("### Filtered Notes Table")
    for index, row in df.iterrows():
        if any(cat in row["categories"] for cat in selected_categories):
            st.write(f"## {row['title']}")
            st.markdown(f" - {row['link']}")
            st.markdown(f" - {row['description']}")
            st.markdown(f" - {row['categories']}")

elif page == "Add Entry":
    notes = load_notes()
    st.header("Add a New Entry")

    # Form to add a new entry
    with st.form(key="add_entry_form"):
        new_title = st.text_input("Title")
        new_link = st.text_input("Link")
        new_description = st.text_area("Description")
        existing_categories = list(category_icon_map.keys())
        selected_categories = st.multiselect("Select Categories", existing_categories)
        new_category = st.text_input("Or add a new category")

        # Add new category if entered
        if new_category:
            selected_categories.append(new_category)

        submit_button = st.form_submit_button("Add Entry")

        if submit_button:
            new_entry = {
                "title": new_title,
                "link": new_link,
                "description": new_description,
                "categories": selected_categories,
            }
            notes.append(new_entry)
            save_notes(notes)
            st.success("Entry added successfully!")
