import pandas as pd
from src.consts import theme_keywords, guild_themes

def extract_theme_from_deck_name(deck_name):
    """Extract the main theme from deck name"""
    deck_lower = deck_name.lower()
    themes = []
    
    for theme in theme_keywords.keys():
        if theme.lower() in deck_lower:
            themes.append(theme)
    
    for guild, guild_themes_list in guild_themes.items():
        if guild in deck_lower:
            themes.extend(guild_themes_list)
    
    return list(set(themes)) if themes else ['Unknown']

def get_deck_colour(deck_name):
    deck_colors = None
    if any(combo in deck_name for combo in ['Azorius', 'WU']):
        deck_colors = 'WU'
    elif any(combo in deck_name for combo in ['Dimir', 'UB']):
        deck_colors = 'UB'
    elif any(combo in deck_name for combo in ['Rakdos', 'BR']):
        deck_colors = 'BR'
    elif any(combo in deck_name for combo in ['Gruul', 'RG']):
        deck_colors = 'RG'
    elif any(combo in deck_name for combo in ['Selesnya', 'GW']):
        deck_colors = 'GW'
    elif any(combo in deck_name for combo in ['Orzhov', 'WB']):
        deck_colors = 'WB'
    elif any(combo in deck_name for combo in ['Izzet', 'UR']):
        deck_colors = 'UR'
    elif any(combo in deck_name for combo in ['Golgari', 'BG']):
        deck_colors = 'BG'
    elif any(combo in deck_name for combo in ['Boros', 'RW']):
        deck_colors = 'RW'
    elif any(combo in deck_name for combo in ['Simic', 'UG']):
        deck_colors = 'UG'
    elif 'White' in deck_name:
        deck_colors = 'W'
    elif 'Blue' in deck_name:
        deck_colors = 'U'
    elif 'Black' in deck_name:
        deck_colors = 'B'
    elif 'Red' in deck_name:
        deck_colors = 'R'
    elif 'Green' in deck_name:
        deck_colors = 'G'
    return deck_colors

def get_available_cards_for_deck(deck_name, cube_df, oracle_df, deck_colors):
    """Find all cards that could potentially be added to this deck"""
    
    # Get all cards currently assigned to other decks or unassigned
    assigned_cards = set(cube_df['Name'].tolist())
    
    # Get all cards from oracle that fit the color identity
    available_cards = []
    
    for _, card in oracle_df.iterrows():
        card_name = card['name']
        
        # Skip if already in cube
        if card_name in assigned_cards:
            continue
            
        # Check color compatibility
        if is_card_playable_in_colors(card, deck_colors):
            available_cards.append(card)
    
    # Also include unassigned cards from cube (if any)
    unassigned_cube_cards = cube_df[cube_df['Tags'].isna() | (cube_df['Tags'] == '')]
    for _, card in unassigned_cube_cards.iterrows():
        oracle_card = oracle_df[oracle_df['name'] == card['Name']]
        if not oracle_card.empty:
            available_cards.append(oracle_card.iloc[0])
    
    return available_cards

def is_card_playable_in_colors(card, deck_colors):
    """Check if a card can be played in the given color identity"""
    if not deck_colors:
        return True
    
    card_color = card.get('Color', '')
    card_category = card.get('Color Category', '')
    
    # Colorless cards and artifacts can be played anywhere
    if card_category in ['Colorless', 'Artifacts', 'Lands'] or pd.isna(card_color):
        return True
    
    # Check if card colors fit deck colors
    if isinstance(card_color, str) and isinstance(deck_colors, str):
        card_color_set = set(card_color)
        deck_color_set = set(deck_colors)
        return card_color_set.issubset(deck_color_set)
    
    return False

def calculate_card_theme_score(expected_themes, card_type, oracle_card):
        oracle_text = str(oracle_card.iloc[0]['Oracle Text']).lower()
        card_score = 0
        matching_themes = []
            
            # Check against each expected theme
        for theme in expected_themes:
            if theme in theme_keywords:
                theme_words = theme_keywords[theme]
                matches = sum(1 for word in theme_words if word in oracle_text or word in card_type)
                if matches > 0:
                    card_score += matches
                    matching_themes.append(f"{theme}({matches})")
            if theme == "Big Creatures" and oracle_card.iloc[0]['Type'].startswith('Creature'):
                oracle_row = oracle_card.iloc[0]
                power = oracle_row.get('Power', 0)
                toughness = oracle_row.get('Toughness', 0)
                oracle_text = str(oracle_row['Oracle Text']).lower()
                    
                    # Handle NaN values
                if pd.isna(power):
                    power = 0
                if pd.isna(toughness):
                    toughness = 0
                    
                try:
                    power = float(power)
                except (ValueError, TypeError):
                    power = 0.0
                    
                try:
                    toughness = float(toughness)
                except (ValueError, TypeError):
                    toughness = 0.0
                if int(power) >= 5 or int(toughness) >= 5:
                    card_score += 1
                    matching_themes.append(f"{theme}(5+ power/toughness)")
        return card_score,matching_themes
