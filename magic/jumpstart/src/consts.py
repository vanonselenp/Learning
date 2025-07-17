TOTAL_CARDS = 13

# Define theme keywords and strategies for different deck archetypes
theme_keywords = { 
    'Aggro': ['haste', 'attack', 'damage', 'creature', 'power', 'quick', 'rush', 'fast'],
    'Control': ['counter', 'destroy', 'exile', 'draw', 'instant', 'sorcery', 'tap', 'return'],
    'Midrange': ['creature', 'value', 'versatile', 'balanced', 'enters', 'when', 'draw', 'search', '+1/+1', 'counter', 'sacrifice', 'dies', 'token', 'adapt', 'evolve', 'outlast', 'kicker', 'vigilance', 'trample', 'treasure', 'mana'],
    'Ramp': ['mana', 'land', 'search', 'big', 'expensive', 'cost', 'ritual'],
    'Tempo': ['bounce', 'counter', 'flying', 'cheap', 'efficient', 'flash', 'tap', 'return', 'untap', 'scry', 'cycling', 'ninjutsu', 'draw', 'when', 'enters', 'kicker'],
    'Graveyard': ['graveyard', 'discard', 'mill', 'return', 'flashback', 'delve'],
    'Sacrifice': ['sacrifice', 'dies', 'death', 'token', 'creature', 'enters'],
    'Tokens': ['token', 'create', 'populate', 'convoke', '1/1', 'creature'],
    'Equipment': ['equipment', 'attach', 'equipped', 'artifact', '+1/+1', 'power'],
    'Flying': ['flying', 'fly', 'air', 'evasion', 'bird', 'spirit'],
    'Burn': ['damage', 'burn', 'lightning', 'shock', 'fire', 'direct'],
    'Artifacts': ['artifact', 'colorless', 'construct', 'equipment', 'vehicle'],
    'Red Artifacts': ['artifact', 'energy', 'servo', 'golem', 'sacrifice an artifact', 'unearth', 'improvise', 'metalcraft', 'treasure', 'scrap', 'gremlin', 'artificer', 'construct'],
    'Big Creatures': ['power', 'toughness', '5', '6', '7', 'large', 'trample'],
    'Small Creatures': ['1', '2', '3', 'haste', 'prowess', 'menace', 'first strike', 'double strike', 'deathtouch', 'lifelink', 'vigilance', 'reach', 'flash', 'goblin', 'human', 'soldier', 'warrior', 'rogue', 'monk', 'scout', 'enters the battlefield', 'when', 'etb'],
    'Card Draw': ['draw', 'card', 'hand', 'library', 'cantrip', 'scry'],
    'Stompy': ['trample', 'power', 'force', 'creature', 'big', 'green'],
    'Beatdown': ['attack', 'damage', 'creature', 'aggressive', 'power']
}

# Color identity synergies
color_synergies = {
    'W': ['vigilance', 'lifelink', 'protection', 'prevent', 'equipment', 'soldier', 'knight'],
    'U': ['draw', 'counter', 'flying', 'scry', 'bounce', 'wizard', 'merfolk'],
    'B': ['destroy', 'discard', 'graveyard', 'sacrifice', 'zombie', 'vampire'],
    'R': ['damage', 'haste', 'sacrifice', 'goblin', 'warrior', 'burn'],
    'G': ['mana', 'ramp', 'trample', 'elf', 'beast', 'large']
}

# Also check for guild names and convert to strategies
guild_themes = {
    'azorius': ['Control', 'Flying'],
    'dimir': ['Control', 'Graveyard'],
    'rakdos': ['Aggro', 'Sacrifice'],
    'gruul': ['Aggro', 'Big Creatures'],
    'selesnya': ['Tokens', 'Midrange'],
    'orzhov': ['Control', 'Sacrifice'],
    'izzet': ['Control', 'Burn'],
    'golgari': ['Graveyard', 'Sacrifice'],
    'boros': ['Aggro', 'Equipment'],
    'simic': ['Ramp', 'Card Draw']
}