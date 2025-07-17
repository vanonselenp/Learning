

import pandas as pd
from src.deck import calculate_card_theme_score, extract_theme_from_deck_name, get_deck_colour


def analyze_deck_theme_coherence_enhanced(cube_df, oracle_df):
    """
    Enhanced version that analyzes deck theme coherence including power/toughness analysis
    Returns detailed analysis of strategy alignment, card synergies, and creature stats
    """
    
    def calculate_theme_score(cards, expected_themes, oracle_df):
        """Calculate how well cards match expected themes"""
        if not expected_themes or expected_themes == ['Unknown']:
            return 0.0, []
        
        theme_matches = []
        total_score = 0
        
        for _, card_row in cards.iterrows():
            card_name = card_row['Name']
            card_type = str(card_row['Type']).lower()
            
            # Find in oracle
            oracle_card = oracle_df[oracle_df['name'] == card_name]
            if oracle_card.empty:
                continue
                
            card_score, matching_themes = calculate_card_theme_score(expected_themes, card_type, oracle_card)
            
            theme_matches.append({
                'card': card_name,
                'score': card_score,
                'themes': matching_themes
            })
            total_score += card_score
        
        avg_score = total_score / len(cards) if len(cards) > 0 else 0
        return avg_score, theme_matches

    
    
    def calculate_creature_stats_coherence(cards, expected_themes, oracle_df):
        """Analyze creature power/toughness distribution and coherence with deck themes"""
        creature_stats = {
            'creature_count': 0,
            'total_power': 0,
            'total_toughness': 0,
            'avg_power': 0,
            'avg_toughness': 0,
            'power_distribution': {},
            'toughness_distribution': {},
            'creature_categories': {
                'small': 0,      # power <= 2
                'medium': 0,     # power 3-4
                'large': 0,      # power >= 5
                'utility': 0,    # low power but high value text
                'evasive': 0     # flying, unblockable, etc.
            },
            'theme_alignment_score': 0,
            'creature_details': []
        }
        
        creatures = []
        
        for _, card_row in cards.iterrows():
            card_name = card_row['Name']
            card_type = str(card_row['Type']).lower()
            
            # Check if it's a creature
            if 'creature' not in card_type:
                continue
            
            # Find in oracle
            oracle_card = oracle_df[oracle_df['name'] == card_name]
            if oracle_card.empty:
                continue
            
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
            
            creature_stats['creature_count'] += 1
            creature_stats['total_power'] += power
            creature_stats['total_toughness'] += toughness
            
            # Power distribution
            try:
                power_key = int(power) if power <= 10 else '10+'
            except (ValueError, TypeError):
                power_key = 0
            creature_stats['power_distribution'][power_key] = creature_stats['power_distribution'].get(power_key, 0) + 1
            
            # Toughness distribution
            try:
                tough_key = int(toughness) if toughness <= 10 else '10+'
            except (ValueError, TypeError):
                tough_key = 0
            creature_stats['toughness_distribution'][tough_key] = creature_stats['toughness_distribution'].get(tough_key, 0) + 1
            
            # Categorize creature
            category = []
            if power <= 2:
                creature_stats['creature_categories']['small'] += 1
                category.append('small')
            elif power <= 4:
                creature_stats['creature_categories']['medium'] += 1
                category.append('medium')
            else:
                creature_stats['creature_categories']['large'] += 1
                category.append('large')
            
            # Check for utility/evasive abilities
            if any(word in oracle_text for word in ['flying', 'unblockable', 'menace', 'trample']):
                creature_stats['creature_categories']['evasive'] += 1
                category.append('evasive')
            
            if any(word in oracle_text for word in ['draw', 'search', 'when', 'enters', 'dies']):
                creature_stats['creature_categories']['utility'] += 1
                category.append('utility')
            
            creature_details = {
                'name': card_name,
                'power': power,
                'toughness': toughness,
                'categories': category,
                'has_evasion': 'evasive' in category,
                'has_utility': 'utility' in category
            }
            creature_stats['creature_details'].append(creature_details)
            creatures.append(creature_details)
        
        # Calculate averages
        if creature_stats['creature_count'] > 0:
            creature_stats['avg_power'] = creature_stats['total_power'] / creature_stats['creature_count']
            creature_stats['avg_toughness'] = creature_stats['total_toughness'] / creature_stats['creature_count']
        
        # Calculate theme alignment for creatures
        theme_alignment_score = 0
        if expected_themes and expected_themes != ['Unknown']:
            for theme in expected_themes:
                if theme == 'Aggro' or theme == 'Beatdown':
                    # Aggro wants low-cost, efficient creatures
                    theme_alignment_score += creature_stats['creature_categories']['small'] * 0.8
                    theme_alignment_score += creature_stats['creature_categories']['evasive'] * 0.9
                elif theme == 'Big Creatures' or theme == 'Stompy':
                    # Big creature themes want high power
                    theme_alignment_score += creature_stats['creature_categories']['large'] * 1.0
                    theme_alignment_score += creature_stats['avg_power'] * 0.2
                elif theme == 'Control':
                    # Control wants utility creatures
                    theme_alignment_score += creature_stats['creature_categories']['utility'] * 0.9
                elif theme == 'Flying':
                    # Flying theme wants evasive creatures
                    flying_count = sum(1 for c in creatures if 'flying' in str(oracle_df[oracle_df['name'] == c['name']].iloc[0]['Oracle Text']).lower())
                    theme_alignment_score += flying_count * 1.0
                elif theme == 'Tokens':
                    # Token themes often want smaller, efficient creatures
                    theme_alignment_score += creature_stats['creature_categories']['small'] * 0.7
                    theme_alignment_score += creature_stats['creature_categories']['utility'] * 0.8
        
        creature_stats['theme_alignment_score'] = theme_alignment_score / max(creature_stats['creature_count'], 1)
        
        return creature_stats
    
    def calculate_color_coherence(cards, deck_colors, oracle_df):
        """Calculate color identity coherence"""
        if not deck_colors:
            return 0.0, []
        
        color_issues = []
        coherent_cards = 0
        total_cards = 0
        
        for _, card_row in cards.iterrows():
            card_name = card_row['Name']
            oracle_card = oracle_df[oracle_df['name'] == card_name]
            
            if oracle_card.empty:
                color_issues.append(f"{card_name}: Not found in oracle")
                continue
            
            card_color = oracle_card.iloc[0]['Color']
            card_category = oracle_card.iloc[0]['Color Category']
            
            total_cards += 1
            
            # Colorless and artifacts are always coherent
            if card_category in ['Colorless', 'Lands'] or pd.isna(card_color):
                coherent_cards += 1
                continue
            
            # Check if card colors fit deck colors
            if isinstance(card_color, str) and isinstance(deck_colors, str):
                card_color_set = set(card_color)
                deck_color_set = set(deck_colors)
                
                if card_color_set.issubset(deck_color_set):
                    coherent_cards += 1
                else:
                    color_issues.append(f"{card_name}: {card_color} doesn't fit {deck_colors}")
        
        coherence_ratio = coherent_cards / total_cards if total_cards > 0 else 0
        return coherence_ratio, color_issues
    
    def calculate_mana_curve_coherence(cards):
        """Calculate mana curve distribution"""
        curve = {}
        for _, card_row in cards.iterrows():
            cmc = card_row.get('CMC', 0)
            if pd.isna(cmc):
                cmc = 0
            try:
                cmc = int(cmc)
            except (ValueError, TypeError):
                cmc = 0
            curve[cmc] = curve.get(cmc, 0) + 1
        
        # Ideal curve depends on strategy, but generally want a good distribution
        total_cards = sum(curve.values())
        if total_cards == 0:
            return 0.0, curve
        
        # Calculate curve score (penalize too many high-cost cards)
        curve_score = 0
        for cmc, count in curve.items():
            if cmc <= 3:
                curve_score += count * 1.0  # Good
            elif cmc <= 5:
                curve_score += count * 0.8  # Okay
            else:
                curve_score += count * 0.4  # Heavy
        
        curve_ratio = curve_score / total_cards
        return curve_ratio, curve
    
    # Analyze each deck
    results = {}
    decks = cube_df.groupby('Tags')
    
    for deck_name, deck_cards in decks:
        # Determine deck colors
        deck_colors = get_deck_colour(deck_name)
        
        # Extract expected themes
        expected_themes = extract_theme_from_deck_name(deck_name)
        
        # Calculate scores
        theme_score, theme_matches = calculate_theme_score(deck_cards, expected_themes, oracle_df)
        color_coherence, color_issues = calculate_color_coherence(deck_cards, deck_colors, oracle_df)
        curve_score, mana_curve = calculate_mana_curve_coherence(deck_cards)
        creature_stats = calculate_creature_stats_coherence(deck_cards, expected_themes, oracle_df)
        
        # Overall coherence score (weighted average including creature stats)
        creature_theme_score = creature_stats['theme_alignment_score'] * 20  # Scale to 0-100
        overall_score = (
            theme_score * 0.4 + 
            color_coherence * 100 * 0.3 + 
            curve_score * 100 * 0.15 + 
            creature_theme_score * 0.15
        )
        
        results[deck_name] = {
            'expected_themes': expected_themes,
            'theme_score': theme_score,
            'theme_matches': theme_matches,
            'color_coherence': color_coherence,
            'color_issues': color_issues,
            'mana_curve_score': curve_score,
            'mana_curve': mana_curve,
            'creature_stats': creature_stats,
            'overall_coherence': overall_score,
            'deck_colors': deck_colors,
            'card_count': len(deck_cards)
        }
    
    return results