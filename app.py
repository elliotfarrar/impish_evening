import streamlit as st
from st_clickable_images import clickable_images
from collections import Counter
from PIL import Image
import pandas as pd
import numpy as np
import random
import base64
import time



########## STREAMLIT ##########

# Installation
# conda create --name ii python==3.11.3
# pip install streamlit==1.47.0
# pip install st-clickable-images==0.0.3

# Set streamlit display settings
st.set_page_config(page_title='II', layout='wide')

# Set title
title_col, team_col = st.columns([3,1])
title_col.markdown(f"<div style='height: 10px;'></div>", unsafe_allow_html=True)
title_col.markdown("<h1 style='font-size:35px;'>📺 An Impish Evening 😈</h1>",unsafe_allow_html=True)
st.markdown("---")

# Create containers
team_setup = st.container()
team_order = st.container()
questions_section = st.container()



########## UTILITIES ##########

# Set a default sidebar width if not already set
if "sidebar_width" not in st.session_state:
    st.session_state["sidebar_width"] = 350

# Set custom sidebar width
st.markdown(
    f"""
    <style>
        [data-testid="stSidebar"] {{
            min-width: {st.session_state["sidebar_width"]}px;
            max-width: {st.session_state["sidebar_width"]}px;
            width: {st.session_state["sidebar_width"]}px;
        }}
        [data-testid="stSidebarContent"] {{
            padding-right: 1rem;
            padding-left: 1rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered bold text
def center_text(text, font_size="1.2", spacing=30):
    st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: {font_size}em;'>{text}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='height: {spacing}px;'></div>", unsafe_allow_html=True)

# Centered image
def center_image(image_url, width=100, spacing=30):
    st.markdown(f"<div style='text-align: center;'><img src='{image_url}' style='max-width: {width}%; height: auto;'></div>",unsafe_allow_html=True)
    st.markdown(f"<div style='height: {spacing}px;'></div>", unsafe_allow_html=True)

# Custom-sized info/error/success boxes
def centered_box(msg, box_type="success", height=55):
    """
    Displays a Streamlit-style notification (success, error, info) with centered text.

    Parameters:
        msg (str): The message to display.
        box_type (str): 'success', 'error', or 'info'.
        height (int): Height of the box in pixels.
    """

    # Define colour schemes
    colors = {
        "success": {
            "bg": "#dff0d8",  # Light green
            "fg": "#3c763d",  # Dark green
            "emoji": ""
        },
        "error": {
            "bg": "#f8d7da",  # Light red
            "fg": "#721c24",  # Dark red
            "emoji": ""
        },
        "info": {
            "bg": "#d1ecf1",  # Light blue
            "fg": "#0c5460",  # Dark blue
            "emoji": ""
        }
    }

    # Set style
    style = colors.get(box_type, colors["info"])
   
    # Render the box
    st.markdown(
        f"""
        <div style="
            background-color:{style['bg']};
            color:{style['fg']};
            padding:16px;
            border-radius:8px;
            text-align:center;
            font-weight:500;
            margin-bottom:12px;
            height:{height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        ">
            {style['emoji']} {msg}
        </div>
        """,
        unsafe_allow_html=True
    )

def hex_to_rgba(hex_color, alpha=0.7):
    """Makes a hex colour slightly translucent."""
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    rgb = tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'

def show_local_image(image_path, caption=None, use_container_width=True):
    """
    Display a local image in a Streamlit app.

    Args:
        image_path (str): Path to the local image file.
        caption (str, optional): Caption for the image.
        use_column_width (bool, optional): Whether to use the column width.
    """
    image = Image.open(image_path)
    st.image(image, use_container_width=use_container_width)

# Emoji options
emoji_options = [
    "😀", "😃", "😄", "😁", "😆", "🥹", "😂", "🤣", "😊", "😇",
    "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😚", "🥰",
    "😋", "😜", "😝", "😛", "🤑", "🤗", "🤭", "🤫", "🤔", "🤐",
    "🤨", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "🥺",
    "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶",
    "😱", "😨", "😰", "😥", "😓", "🫠", "😶", "😐", "🤑", "😑",
    "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤",
    "😪", "😵", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🥳",
    "🥸", "😎", "🤓", "🧐", "👻", "💀", "👽", "👾", "🤖", "🎃",
    "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🐶",
    "🐱", "🐭", "🐹", "🐰", "🦊", "🦝", "🐻", "🐼", "🦄", "🐴",
    "🐮", "🐷", "🐸", "🐵", "🙈", "🙉", "🙊", "🐔", "🐧", "🐦",
    "🐤", "🐣", "🦆", "🦉", "🦅", "🦇", "🐺", "🐗", "🐴", "🐢",
    "🐍", "🦎", "🐙", "🦑", "🦐", "🦀", "🐡", "🐠", "🐟", "🐬",
    "🐳", "🐋", "🦭", "🐊", "🐆", "🦓", "🦍", "🦧", "🦣", "🦌",
    "🦬", "🦏", "🦛", "🐘", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂",
    "🐄", "🐎", "🐖", "🐏", "🐑", "🐐", "🦙", "🦥", "🦦", "🦨",
    "🦡", "🐁", "🐀", "🐇", "🦔", "🐉", "🐲", "🌵", "🎄", "🌲",
    "🌳", "🌴", "☘️", "🍀", "🌿", "🍃", "🍂", "🍁", "🍄", "🌾",
    "🌺", "🌻", "🌹", "🌷", "🪷", "🌼", "🌞", "🌝", "🌚", "🌛",
    "🌜", "🌙", "🌎", "🌍", "🌏", "💐", "🍄", "🌸", "🏵️", "🪷",
    "🏆", "🥇", "🥈", "🥉", "🏅", "🎖️", "🎗️", "🏵️", "🎯", "🎲",
    "♟️", "🎮", "🎰", "🧩", "🎭", "🃏", "🎴", "🀄", "🎨", "🖌️",
    "🖍️", "🖊️", "🖋️", "✏️", "📝", "📒", "📚", "📖", "📓", "📔",
    "📕", "📗", "📘", "📙", "📙", "📰", "🗞️", "🔖", "🏷️", "💼",
    "🗂️", "🗃️", "🗄️", "📅", "📆", "🗓️", "⏰", "⏳", "⌛", "⏲️",
    "⏱️", "🕰️", "🔒", "🔓", "🔏", "🔐", "🔑", "🗝️", "🔨", "🪓",
    "🧰", "🔧", "🪛", "🔩", "⚒️", "🛠️", "🗡️", "⚔️", "🔫", "🏹",
    "🛡️", "🔬", "🔭", "📡", "💉", "🩸", "🧬", "🦠", "🩺", "💊",
    "🚗", "🚕", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐", "🛻",
    "🚚", "🚛", "🚜", "🚲", "🛴", "🛹", "🏍️", "🛵", "🚨", "🚔",
    "🚍", "🚞", "🚠", "🚡", "🚟", "🚃", "🚋", "🚝", "🚄", "🚅",
    "🚆", "🚇", "🚈", "🚉", "✈️", "🛫", "🛬", "🛩️", "💺", "🚀",
    "🛸", "🚁", "🛶", "⛵", "🚤", "🛥️", "🛳️", "⛴️", "🚢", "🚦",
    "🚧", "🛑", "🔰", "🏁", "🚩", "🎌", "🏴‍☠️", "🏳️", "🏳️‍🌈", "🏳️‍⚧️",
]

# Set RNG seed
#random.seed(10)

# Set delay times
loading_delay = 0.5 # delay when loading questions #3
pre_question_delay = 1 # delay before the question #1
pre_answer_delay = 2 # delay before the first answer #2
answer_delay = 1 # delay for subsequent answer #1




########## QUESTIONS ##########

# Define the questions, categories, answers and images

# 1. Manually enter questions
q_array = [
    ["What is 2+2?", "GBBO", "4", "5", "6", "7"],
    ["Pick a very long answer!", "Long", "Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello Hello", "5", "6", "7"],
    ["What is the capital of France?", "Geography", "Paris", "London", "Berlin", "Rome"],
    ["What color do you get by mixing red and blue?", "Art", "Purple", "Green", "Orange", "Yellow"],
    ["How many continents are there?", "Geography", "7", "6", "5", "8"],
    ["Which planet is closest to the sun?", "Science", "Mercury", "Venus", "Earth", "Mars"],
    ["Select a Mastermind scroll!", "Mastermind", "", "", "", ""],
    ["Significant of 22nd September?", "Mastermind", "", "", "", ""],
]
df = pd.DataFrame(q_array, columns=["Question", "Category", "A1", "A2", "A3", "A4"])

# 2. Load a .csv of questions
df = pd.read_csv('questions.csv')

# Adds a column 'index' with unique identifiers.  
# These will be used to track question usage.
df.reset_index(inplace=True)  

# Get the total number of questions
num_questions = len(df)

# 1. Load images from the web:
# category_image_mapping = {
#     "Maths": "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
#     "Long": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=700",
#     "Geography": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700",
#     "Art": "https://images.unsplash.com/photo-1494526585095-c41746248156?w=700",
#     "Science": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=700",
#     "Mastermind": "https://images.unsplash.com/photo-1518773553398-650c184e0bb3?w=700",
# }

# 2. Specify local images
category_image_mapping = {
    "GBBO": "./images/GBBO.png",
    "TOTP": "./images/TOTP.png",
    "Art Attack": "./images/art_attack.png",
    "A Question of Sport": "./images/question_of_sport.png",
    "Brainiac": "./images/brainiac.png",
    "Location Location Location": "./images/location.png",
    "MAFS": "./images/static_screen.png",
    "Our Planet": "./images/our_planet.png",
    "Richard Osman's House of Games": "./images/house_of_games.png",
    "QI": "./images/QI.png",
    "Time Team": "./images/time_team.png",
    "Mastermind": "./images/mastermind.png",
    "Supernatural": "./images/supernatural.png",
    "Watchdog": "./images/watchdog.png",
    "Grand Designs": "./images/grand_designs.png",
}

# Encode them with base64
for category, path in category_image_mapping.items():
    with open(path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    category_image_mapping[category] = f"data:image/jpeg;base64,{encoded}"




########## TEAM SETUP ##########

# Initialize session state for team locking
if "teams_locked" not in st.session_state:
    st.session_state["teams_locked"] = False

with team_setup:

    if not st.session_state["teams_locked"]:

        # Set custom button size
        st.markdown(f"""
            <style>
            div[data-testid="stButton"] button {{
                height: 50px;
            }}
            </style>
            """,
            unsafe_allow_html=True)

        # Section to track scores
        st.subheader("Team Setup")

        # Select number of teams
        st.session_state["num_teams"] = st.number_input(
            "How many teams are playing?",
            min_value=1, max_value=4, value=2, step=1,
            disabled=st.session_state["teams_locked"],
        )

    # Initialize team data
    team_data = []

    # Create a column for each team
    team_cols = st.columns(st.session_state["num_teams"])

    # Iterate over the number of teams
    for i in range(st.session_state["num_teams"]):
        with team_cols[i]:

            # If teams are not locked, allow setting team names and colors
            if not st.session_state["teams_locked"]:

                # Set the team name
                name = st.text_input(
                    f"Team {i+1} Name:",
                    value=f"Team {chr(65+i)}",
                    key=f"select_team_name_{i}",
                    disabled=st.session_state["teams_locked"],
                    placeholder="Pick a team name!",
                    max_chars=20,
                )
                if not name:
                    name = "Placeholder"
                st.session_state[f"team_name_{i}"] = name

                tcol1, tcol2 = st.columns(2)

                # Set the team color
                st.session_state[f"team_colour_{i}"] = tcol1.color_picker(
                    f"Team {i+1} Colour:", "#6fa3ef",
                    key=f"select_team_colour_{i}",
                    disabled=st.session_state["teams_locked"],
                )

                # Set the team emoji
                st.session_state[f"team_emoji_{i}"] = tcol2.selectbox(
                    f"Team {i+1} Emoji:",
                    emoji_options,
                    index=i % len(emoji_options), # Give each team a different default
                    key=f"select_team_emoji_{i}",
                    disabled=st.session_state["teams_locked"],
                    )

                # Initialize score and lifelines
                if f"team_score_{i}" not in st.session_state:
                    st.session_state[f"team_score_{i}"] = 0
                if f"team_lifelines_{i}" not in st.session_state:
                    st.session_state[f"team_lifelines_{i}"] = 3

            # Define all team data in a dictionary
            team_data.append({
                "name": st.session_state[f"team_name_{i}"],
                "colour": st.session_state[f"team_colour_{i}"],
                "emoji": st.session_state[f"team_emoji_{i}"],
                "score": st.session_state[f"team_score_{i}"],
                "lifelines": st.session_state[f"team_lifelines_{i}"],
                })

    # Create a button to lock the teams
    if not st.session_state["teams_locked"]:
        if st.button("🔐 Lock Teams", use_container_width=True):
            st.session_state["teams_locked"] = True
            st.rerun()




########## TEAM ORDER ##########

# Initialize session state for team order set
if "team_order_confirmed" not in st.session_state:
    st.session_state["team_order_confirmed"] = False

with team_order:

    if st.session_state["teams_locked"] and not st.session_state["team_order_confirmed"]:
       
        # Set custom button size
        st.markdown(f"""
            <style>
            div[data-testid="stButton"] button {{
                height: 50px;
            }}
            </style>
            """,
            unsafe_allow_html=True)

        # Get the team names and number of teams
        team_names = [team["name"] for team in team_data]
        num_teams = st.session_state["num_teams"]

        # Ensure team order is initialized
        if "team_order" not in st.session_state or len(st.session_state["team_order"]) != num_teams:
            st.session_state["team_order"] = team_names.copy()

        # Set the default order
        team_order = st.session_state["team_order"]
        new_order = []
        used_names = set()

        # Select team order
        st.markdown("#### 🔀 Select Team Order")
        for slot in range(num_teams):
            available = [name for name in team_names if name not in used_names]
            selected = st.selectbox(
                f"Team at position {slot+1}:",
                options=available,
                index=0,
                key=f"team_order_select_{slot}",
            )
            new_order.append(selected)
            used_names.add(selected)

        # Only allow confirm if all slots are filled and no duplicates
        can_confirm = len(new_order) == num_teams and len(set(new_order)) == num_teams
        if can_confirm and not st.session_state["team_order_confirmed"]:
            if st.button("✅ Confirm Team Order", use_container_width=True):
                st.session_state["team_order"] = new_order
                st.session_state["team_order_confirmed"] = True
                st.rerun()
        elif st.session_state["team_order_confirmed"]:
            st.success("Team order confirmed! You can select a question.")
        else:
            st.warning("Fill all team slots with unique teams, then confirm to proceed.")

# Initialize a counter session state. We update this counter every time a question
# is answered and use it as the clickable images key. This forces the clickable images
# to be re-rendered after each question, resetting the default back to -1 and only
# including the relevant images. We also use it to cycle through the team order.
if "click_counter" not in st.session_state:
    st.session_state["click_counter"] = 0

# Show current team data
if st.session_state["team_order_confirmed"]:

    # Get the current team and their emoji and colour
    team_to_play = st.session_state["team_order"][st.session_state["click_counter"] % st.session_state["num_teams"]]
    team_emoji = next((team["emoji"] for team in team_data if team["name"] == team_to_play), "")
    team_colour = next((team["colour"] for team in team_data if team["name"] == team_to_play), "#000000")
    trans_colour = hex_to_rgba(team_colour, 0.5)

    # Render a card showing the current user
    with team_col:
        if num_questions != st.session_state["click_counter"]:
            st.markdown(
                    f"""
                    <div style='text-align: right;'>
                        <div style="
                            display: inline-block;
                            font-size: 18px;
                            font-weight: bold;
                            background-color: {trans_colour};
                            border-radius: 8px;
                            padding: 10px 18px;
                            margin-top: 32px;">
                            {team_to_play} to play! {team_emoji}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                       
else:
    team_to_play = None





########## SCOREBOARD ##########

# Create a sidebar
with st.sidebar:

    if not st.session_state["teams_locked"]:
        st.markdown("## 🏆 Scoreboard   🔓")

    else:
        st.markdown("## 🏆 Scoreboard   🔐")


        # Define the container for the cards
        cards = st.container()

        # Allow scores and lifelines to be adjusted
        st.markdown("## Adjust Scores & Lifelines")
        for i, team in enumerate(team_data):
            st.markdown(f"<small style='color: #888;'>{team['emoji']} <b>{team['name']}</b></small>", unsafe_allow_html=True)
            col1, col2 = st.columns([2, 2])
            with col1:
                score = st.number_input(
                    f"{team['name']} score",
                    min_value=0, max_value=999,
                    value=team["score"],
                    key=f"set_team_score_{i}",
                    label_visibility="collapsed",
                )
            with col2:
                lifelines = st.number_input(
                    f"{team['name']} lifelines",
                    min_value=0, max_value=3,
                    value=team["lifelines"],
                    key=f"set_team_lifelines_{i}",
                    label_visibility="collapsed",
                )

            # Update the dictionary
            team_data[i]["score"] = score
            team_data[i]["lifelines"] = lifelines

        st.markdown("---")

        # Sort the teams by scores
        sorted_teams = sorted(team_data, key=lambda t: t["score"], reverse=True)
        num_teams = len(sorted_teams)

        # Set styles for the cards
        normal_bg = "#f9f9f9" # Gold background for 1st place
        gold_bg = "#fffbe6" # Standard for others

        with cards:

            # Iterate through the teams
            for i, team in enumerate(sorted_teams):

                # Indicate the team to play (unless we've used all the questions)
                to_play = "⭐" if team["name"] == team_to_play and num_questions != st.session_state["click_counter"] else ""

                # Default to normal background and no medal
                medal = ""
                bg = normal_bg

                # Assign medals for top 3
                if i == 0:
                    medal = "🥇"
                    bg = gold_bg
                elif i == 1:
                    medal = "🥈"
                elif i == 2 and num_teams > 2:
                    medal = "🥉"

                # Give a spoon to last place, regardless of how many teams
                if i == num_teams - 1 and num_teams > 1:
                    medal = "🥄"

                # Use dots illustrate remaining lifelines
                max_lifelines = 3
                lifelines = team['lifelines']
                filled_dot = '<span style="color:#d32f2f;font-size:22px;">&#9679;</span>' # Filled red dot
                empty_dot = '<span style="color:#ddd;font-size:22px;">&#9675;</span>' # Empty dot
                dots = filled_dot * lifelines + empty_dot * (max_lifelines - lifelines)
           
                # Illustrate the card
                st.markdown(
                    f"""
                    <div style="
                        border-left: 12px solid {team['colour']};
                        background: {bg};
                        padding: 12px;
                        margin-bottom: 10px;
                        border-radius:8px;
                        box-shadow: 1px 1px 2px #eee;
                        width: 95%;
                        max-width: 97%;
                        min-width: 200px;
                    ">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <span style="font-size: 24px;">{medal}</span>
                            <strong style="flex: 1; text-align: left; font-size: 18px; margin: 0 10px;">
                                {team['name']} {to_play}
                            </strong>
                            <span style="font-size: 24px;">{team['emoji']}</span>
                            <span style="font-size:22px; color:#444; margin-left:10px;">{dots}</span>
                        </div>
                        <span style="font-size:25px;color:#2a5">{team['score']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")

        # Save previous sidebar width for comparison
        if "sidebar_width_prev" not in st.session_state:
            st.session_state["sidebar_width_prev"] = st.session_state["sidebar_width"]

        # Allow new width to be selected
        new_width = st.slider(
            "Sidebar Width (px)",
            min_value=200,
            max_value=500,
            value=st.session_state["sidebar_width"],
            step=10,
        )

        # Use st.rerun to get instant feedback on sidebar width change
        if new_width != st.session_state["sidebar_width_prev"]:
            st.session_state["sidebar_width"] = new_width
            st.session_state["sidebar_width_prev"] = new_width
            st.rerun()

   



########## QUESTIONS ##########

# Track which indexes (questions) have been used in a session state list
if "used_indices" not in st.session_state:
    st.session_state["used_indices"] = []

# Initialize the current question index
if "current_q_idx" not in st.session_state:
    st.session_state["current_q_idx"] = None

# Initialize session states to lock category once selected
if "category_locked" not in st.session_state:
    st.session_state["category_locked"] = False
if "selected_category_idx" not in st.session_state:
    st.session_state["selected_category_idx"] = None

# Initialize session states to ensure delays aren't repeated
if "questions_delayed" not in st.session_state:
    st.session_state["questions_delayed"] = False

# Set category selection to none by default
selected_idx = None
selected_category = None


with questions_section:

    # Mark if all questions have been answered
    if num_questions == st.session_state["click_counter"]:
        center_text(f"⛔ TV Licence Expired!", font_size=1.5)
        show_local_image("images/static_screen.png")

    if st.session_state["teams_locked"] and st.session_state["team_order_confirmed"] and num_questions != st.session_state["click_counter"]:

        # Get a list of the used question indexes
        used_indices = st.session_state.get("used_indices", [])

        # Filter the DataFrame to only unused questions
        unused_df = df[~df["index"].isin(used_indices)]

        # Warn if dataframe is empty (should not trigger)
        if unused_df.empty:
            center_text(f"⛔ TV Licence Expired!", font_size=1.5)
            show_local_image("images/static_screen.png")

        # Get the unused categories
        unused_categories = list(unused_df["Category"].unique())

        # Get the category images
        category_images = {cat: category_image_mapping[cat] for cat in unused_categories if cat in category_image_mapping}

        # Count the remaining questions per category
        category_counts = Counter(unused_df["Category"])

        # Create display labels for each category showing the number of remaining questions
        category_labels = [f"{cat} ({category_counts[cat]})" for cat in category_counts]

        if not st.session_state["category_locked"] and not unused_df.empty:

            # Prompt category selection (centered)
            center_text(f"📱TV Guide:", font_size=1.5)

            # Render clickable images to select the category
            # Github: https://github.com/vivien000/st-clickable-images
            clicked = clickable_images(
                list(category_images.values()),
                titles=category_labels,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},
                key=f"clickable_images_{st.session_state['click_counter']}",
            )

            # # https://github.com/vivien000/st-clickable-images
            # images = []
            # for file in ["ether.png"]:
            #     with open(file, "rb") as image:
            #         encoded = base64.b64encode(image.read()).decode()
            #         images.append(f"data:image/jpeg;base64,{encoded}")
            # clicked = clickable_images(
            #     images,
            #     titles=[f"Image #{str(i)}" for i in range(len(images))],
            #     div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            #     img_style={"margin": "5px", "height": "200px"},
            # )

            # Prompt a rerun if an image is clicked
            if clicked > -1:
                st.session_state["selected_category_idx"] = clicked
                st.session_state["category_locked"] = True

                # Randonly chose a fun loading animation
                result = random.choice(["Spinner", "Progress"])

                # Spinner
                if result == "Spinner":
                    _, central_col, _ = st.columns([3,1,3])
                    with central_col:
                        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Gray_circles_rotate.gif", width=90)
                        st.markdown("<div style='font-size:1.5em;font-weight:bold;'>Tuning in...</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        time.sleep(loading_delay)
            
                # Progress bar
                if result == "Progress":
                    st.markdown("<div style='font-size:1.5em;font-weight:bold;'>Tuning in...</div>", unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i+1)
                        time.sleep(loading_delay/100)

                st.rerun()

        else:

            # Display selection status
            if st.session_state["category_locked"]:
                selected_idx = st.session_state["selected_category_idx"]
                selected_category = unused_categories[selected_idx]
                selected_image = category_images[selected_category]
                center_text(f"📺 You selected: {selected_category}!")
                center_image(selected_image, width=40)

        # Display a message if no category is selected (default state)
        if not selected_category:
            pass

        else:


            # Get all questions in the selected category that haven't been used before
            available_df = df[(df["Category"] == selected_category) & (~df["index"].isin(st.session_state["used_indices"]))]

            # Ensure there are questions available in the selected category
            if not available_df.empty:

                # Pick a random question from those available, only once per round
                if st.session_state["current_q_idx"] is None:
                    st.session_state["current_q_idx"] = random.choice(available_df["index"].tolist())

                    # Reset per-question state
                    selected_row = available_df[available_df["index"] == st.session_state["current_q_idx"]].iloc[0]
                    q_prompt = selected_row["Question"]

                    # Remove old shuffle/visibility state
                    keys_to_remove = [
                        f"{q_prompt}_shuffled",
                        f"{q_prompt}_visible_btns",
                        f"{q_prompt}_last_answered",
                    ]
                    for k in list(st.session_state.keys()):
                        if k.startswith(f"{q_prompt}_reveal_step_"):
                            del st.session_state[k]
                    for k in keys_to_remove:
                        if k in st.session_state:
                            del st.session_state[k]

                    # Reset global flags
                    st.session_state["answered_this_question"] = False
                    st.session_state["correct"] = None

                # Select the question row corresponding to that index
                selected_row = available_df[available_df["index"] == st.session_state["current_q_idx"]].iloc[0]

                # Collect the prompt and category
                q_prompt = selected_row["Question"]
                category = selected_row["Category"]

                # Collect the answers from the 4 option columns
                answers = [
                    selected_row["A1"],
                    selected_row["A2"],
                    selected_row["A3"],
                    selected_row["A4"],
                ]

                # Assume the first answer is the correct one
                true_answer = answers[0]

                # Shuffle answers only once and store in session state
                shuffle_key = f"{q_prompt}_shuffled"
                if shuffle_key not in st.session_state:
                    st.session_state[shuffle_key] = random.sample(answers, k=len(answers))
                shuffled_answers = st.session_state[shuffle_key]

                # Track visible buttons for this question
                visible_btns_key = f"{q_prompt}_visible_btns"
                if visible_btns_key not in st.session_state:
                    st.session_state[visible_btns_key] = 1  # Start with 1 button visible
                visible_btns = st.session_state[visible_btns_key]

                # Set the height of the buttons and boxes based on the length of the answers
                max_answer_length = max(len(str(ans)) for ans in answers)
                box_height = max(max_answer_length*0.55, 55)

                # Set the height of the buttons
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stButton"] button {{
                        height: {box_height}px;
                        padding: 15px 20px 15px 20px;
                        font-size: 18px;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Define the question container
                st.markdown("---")
                q_container = st.container()

                with q_container:

                    # Write the question (centered)
                    if not st.session_state['questions_delayed']:
                        time.sleep(pre_question_delay)
                    center_text(q_prompt, font_size=1.8)
                    if not st.session_state['questions_delayed']:
                        time.sleep(pre_answer_delay)

                    # Mark the delays as used in session state
                    st.session_state['questions_delayed'] = True

                    # Initialize result
                    result = None

                    # Initialize session state for selected answer state
                    selected_key = f"{q_prompt}_selected"
                    if selected_key not in st.session_state:
                        st.session_state[selected_key] = None

                    # Initialize session state for revealing answer
                    if "reveal_answer" not in st.session_state:
                        st.session_state["reveal_answer"] = False

                    # If answers are defined
                    if all(answers):

                        # Create columns to show buttons
                        cols = st.columns(2)

                        # Before any answer is selected, render buttons for available answers
                        if st.session_state[selected_key] is None and not st.session_state["reveal_answer"]:
                            for i in range(visible_btns):
                                ans = shuffled_answers[i]
                                with cols[i % 2]:
                                    if st.button(
                                        str(ans),
                                        use_container_width=True,
                                        key=f"{q_prompt}_{i}",
                                    ):
                                        st.session_state[selected_key] = ans
                                        st.session_state["answered_this_question"] = True

                                        # Determine whether the selected answer was correct
                                        st.session_state["correct"] = (ans == true_answer)
                                        st.rerun()

                        # If answer is selected and reveal answer button is clicked, show feedback
                        elif st.session_state["reveal_answer"]:
                            for i, ans in enumerate(shuffled_answers):
                                with cols[i % 2]:
                                    
                                    # Show the selected answer (right or wrong)
                                    if ans == st.session_state[selected_key]:
                                        if ans == true_answer:
                                            centered_box(f"✅ {ans}", "success", box_height)
                                        else:
                                            centered_box(f"❌ {ans}", "error", box_height)

                                    # Show the correct answer (if not selected)
                                    elif (
                                        st.session_state[selected_key] != true_answer
                                        and ans == true_answer
                                    ):
                                        centered_box(f"✅ {ans}", "success", box_height)

                                    # Show all other answers
                                    else:
                                        st.button(str(ans), disabled=True, use_container_width=True, key=f"{q_prompt}_{i}_post_answer")

                        # If an answer is selected, show the selected answer
                        else:
                            for i, ans in enumerate(shuffled_answers):
                                with cols[i % 2]:
                                    
                                    # Show the selected answer (right or wrong)
                                    if ans == st.session_state[selected_key]:
                                        if ans == true_answer:
                                            centered_box(f"✅ {ans}", "success", box_height)
                                        else:
                                            centered_box(f"❌ {ans}", "error", box_height)

                                    # Show all other answers
                                    else:
                                        st.button(str(ans), disabled=True, use_container_width=True, key=f"{q_prompt}_{i}_post_answer")
                                        
                        # Automatically reveal next button after delay
                        if visible_btns < len(shuffled_answers):
                            # Avoid sleeping on all reruns; only do so the first time a new button should appear
                            # To prevent infinite loops, use a flag for each button reveal step
                            reveal_step_key = f"{q_prompt}_reveal_step_{visible_btns}"
                            if reveal_step_key not in st.session_state:
                                time.sleep(answer_delay)
                                st.session_state[visible_btns_key] += 1
                                st.session_state[reveal_step_key] = True
                                st.rerun()

                        # Determine if answer was correct or not
                        if result:
                            if result == true_answer:
                                st.session_state["correct"] = True
                            else:
                                st.session_state["correct"] = False
        
                            # Mark question as answered
                            st.session_state["answered_this_question"] = True


                    # If no answers are defined, we have a manual question.
                    else:
                        # Mark question as answered automatically to prompt next question button
                        st.session_state["answered_this_question"] = True


                    # Cleanup section for after all questions
                    st.markdown("---")
                    clean_1, clean_2 = st.columns(2)

                    # Create a "Next Question" button after the question is answered  
                    if st.session_state.get("answered_this_question") and "current_q_idx" in st.session_state:

                        # Reveal the correct answer if answered incorrectly
                        if st.session_state["correct"] is False:
                            if clean_1.button("👁️ Reveal Answer",
                                use_container_width=True,
                                disabled=st.session_state["reveal_answer"],
                                ):
                                st.session_state["reveal_answer"] = True
                                #st.info(f"The correct answer is: **{true_answer}**")
                                st.rerun()

                        else:
                            clean_1, clean_2, _ = st.columns([1,10,1])

                        # Create a "Next Question" button after the question is answered  
                        if clean_2.button("➡️ Next Question ", use_container_width=True):

                            # Add the current index to the list of used questions
                            st.session_state["used_indices"].append(st.session_state["current_q_idx"])

                            # Clean up per-question session states
                            keys_to_remove = [
                                f"{q_prompt}_shuffled",
                                f"{q_prompt}_visible_btns",
                                f"{q_prompt}_last_answered",
                            ]
                            for k in list(st.session_state.keys()):
                                if k.startswith(f"{q_prompt}_reveal_step_"):
                                    del st.session_state[k]
                            for k in keys_to_remove:
                                if k in st.session_state:
                                    del st.session_state[k]
            
                            # Global flags
                            st.session_state["answered_this_question"] = False
                            st.session_state["correct"] = None
                            st.session_state["current_q_idx"] = None
                            st.session_state["reveal_answer"] = False
                            st.session_state["click_counter"] += 1
                            st.session_state["category_locked"] = False
                            st.session_state["selected_category_idx"] = None
                            st.session_state['questions_delayed'] = False
                            st.rerun()

            # Warn if no questions are left in the selected category
            else:
                st.warning("No questions left in this category!")


## TODO:
# FULL TEST OF ALL QUESTIONS
# PUSH TO GIT AND DEPLOY: https://blog.streamlit.io/host-your-streamlit-app-for-free/

## Extra TODO:
# Decoration, streamlit style, colours, art, icons, theme (DO YOU HAVE A TV LICENCE?)
# Watch dog tag. Can we add images for certain questions?