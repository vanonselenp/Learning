import pandas as pd
from src.deck import calculate_card_theme_score, extract_theme_from_deck_name, get_deck_colour, is_card_playable_in_colors
from src.consts import theme_keywords
from IPython.display import Markdown, display


def display_coherence_analysis_enhanced(coherence_results, top_n=5):
    """Display enhanced coherence analysis results including creature stats"""
    
    # Sort decks by overall coherence score
    sorted_decks = sorted(coherence_results.items(), 
                         key=lambda x: x[1]['overall_coherence'], 
                         reverse=True)
    
    display(Markdown("# Enhanced Deck Theme Coherence Analysis"))
    
    # Overall summary
    avg_coherence = sum(r['overall_coherence'] for r in coherence_results.values()) / len(coherence_results)
    display(Markdown(f"**Average Coherence Score: {avg_coherence:.1f}/100**"))
    
    # Top performing decks
    display(Markdown(f"## Top {top_n} Most Coherent Decks"))
    for i, (deck_name, analysis) in enumerate(sorted_decks[:top_n]):
        display(Markdown(f"### {i+1}. {deck_name}"))
        display(Markdown(f"- **Overall Score: {analysis['overall_coherence']:.1f}/100**"))
        display(Markdown(f"- **Expected Themes:** {', '.join(analysis['expected_themes'])}"))
        display(Markdown(f"- **Theme Match Score:** {analysis['theme_score']:.1f}"))
        display(Markdown(f"- **Color Coherence:** {analysis['color_coherence']:.1%}"))
        display(Markdown(f"- **Mana Curve Score:** {analysis['mana_curve_score']:.1%}"))
        
        # Creature stats
        creature_stats = analysis['creature_stats']
        display(Markdown(f"- **Creature Count:** {creature_stats['creature_count']} ({creature_stats['creature_count']/analysis['card_count']:.1%} of deck)"))
        if creature_stats['creature_count'] > 0:
            display(Markdown(f"- **Avg Power/Toughness:** {creature_stats['avg_power']:.1f}/{creature_stats['avg_toughness']:.1f}"))
            display(Markdown(f"- **Creature Mix:** Small: {creature_stats['creature_categories']['small']}, Medium: {creature_stats['creature_categories']['medium']}, Large: {creature_stats['creature_categories']['large']}"))
            display(Markdown(f"- **Creature Theme Alignment:** {creature_stats['theme_alignment_score']:.1f}"))
        
        if analysis['color_issues']:
            display(Markdown(f"- **Color Issues:** {len(analysis['color_issues'])} cards"))
    
    # Bottom performing decks
    display(Markdown(f"## Bottom {top_n} Least Coherent Decks"))
    for i, (deck_name, analysis) in enumerate(sorted_decks[-top_n:]):
        display(Markdown(f"### {len(sorted_decks)-top_n+i+1}. {deck_name}"))
        display(Markdown(f"- **Overall Score: {analysis['overall_coherence']:.1f}/100**"))
        display(Markdown(f"- **Expected Themes:** {', '.join(analysis['expected_themes'])}"))
        display(Markdown(f"- **Theme Match Score:** {analysis['theme_score']:.1f}"))
        display(Markdown(f"- **Color Coherence:** {analysis['color_coherence']:.1%}"))
        
        # Creature stats
        creature_stats = analysis['creature_stats']
        if creature_stats['creature_count'] > 0:
            display(Markdown(f"- **Avg Power/Toughness:** {creature_stats['avg_power']:.1f}/{creature_stats['avg_toughness']:.1f}"))
            display(Markdown(f"- **Creature Theme Alignment:** {creature_stats['theme_alignment_score']:.1f}"))
        
        if analysis['color_issues']:
            display(Markdown(f"- **Color Issues:** {analysis['color_issues'][:3]}"))


def analyze_specific_deck_enhanced(deck_name, cube_df, oracle_df, coherence_results):
    """Enhanced deck analysis including creature statistics"""
    
    if deck_name not in coherence_results:
        print(f"Deck '{deck_name}' not found!")
        return
    
    deck_data = coherence_results[deck_name]
    deck_cards = cube_df[cube_df['Tags'] == deck_name]
    creature_stats = deck_data['creature_stats']
    
    display(Markdown(f"# Enhanced Analysis: {deck_name}"))
    display(Markdown(f"**Overall Coherence Score: {deck_data['overall_coherence']:.1f}/100**"))
    
    # Theme analysis
    display(Markdown("## Theme Analysis"))
    display(Markdown(f"**Expected Themes:** {', '.join(deck_data['expected_themes'])}"))
    display(Markdown(f"**Theme Match Score:** {deck_data['theme_score']:.1f}"))
    
    # Creature Statistics
    display(Markdown("## Creature Statistics"))
    display(Markdown(f"**Total Creatures:** {creature_stats['creature_count']} ({creature_stats['creature_count']/deck_data['card_count']:.1%} of deck)"))
    
    if creature_stats['creature_count'] > 0:
        display(Markdown(f"**Average Power/Toughness:** {creature_stats['avg_power']:.1f}/{creature_stats['avg_toughness']:.1f}"))
        display(Markdown(f"**Total Power/Toughness:** {creature_stats['total_power']:.0f}/{creature_stats['total_toughness']:.0f}"))
        display(Markdown(f"**Creature Theme Alignment Score:** {creature_stats['theme_alignment_score']:.1f}"))
        
        # Creature categories
        display(Markdown("### Creature Categories:"))
        display(Markdown(f"- **Small (≤2 power):** {creature_stats['creature_categories']['small']} creatures"))
        display(Markdown(f"- **Medium (3-4 power):** {creature_stats['creature_categories']['medium']} creatures"))
        display(Markdown(f"- **Large (≥5 power):** {creature_stats['creature_categories']['large']} creatures"))
        display(Markdown(f"- **Evasive abilities:** {creature_stats['creature_categories']['evasive']} creatures"))
        display(Markdown(f"- **Utility abilities:** {creature_stats['creature_categories']['utility']} creatures"))
        
        # Power distribution
        if creature_stats['power_distribution']:
            power_dist = ", ".join([f"{k}: {v}" for k, v in sorted(creature_stats['power_distribution'].items())])
            display(Markdown(f"**Power Distribution:** {power_dist}"))
        
        # Show individual creatures
        if creature_stats['creature_details']:
            display(Markdown("### Creature Details:"))
            for creature in creature_stats['creature_details'][:10]:  # Show first 10
                categories_str = ", ".join(creature['categories']) if creature['categories'] else "basic"
                display(Markdown(f"- **{creature['name']}** ({creature['power']:.0f}/{creature['toughness']:.0f}) - {categories_str}"))
    
    # Color coherence
    display(Markdown("## Color Analysis"))
    display(Markdown(f"**Deck Colors:** {deck_data['deck_colors']}"))
    display(Markdown(f"**Color Coherence:** {deck_data['color_coherence']:.1%}"))
    
    if deck_data['color_issues']:
        display(Markdown("### Color Issues:"))
        for issue in deck_data['color_issues'][:5]:
            display(Markdown(f"- {issue}"))
    
    # Mana curve
    display(Markdown("## Mana Curve Analysis"))
    display(Markdown(f"**Mana Curve Score:** {deck_data['mana_curve_score']:.1%}"))
    
    curve_display = []
    for cmc in sorted(deck_data['mana_curve'].keys()):
        count = deck_data['mana_curve'][cmc]
        curve_display.append(f"CMC {cmc}: {count} cards")
    
    display(Markdown("**Curve Distribution:**"))
    for item in curve_display:
        display(Markdown(f"- {item}"))
    
    # Enhanced recommendations including creature analysis
    display(Markdown("## Improvement Recommendations"))
    
    recommendations = []
    
    if deck_data['theme_score'] < 2.0:
        recommendations.append("🎯 **Theme Focus**: Consider adding more cards that directly support the deck's themes")
    
    if deck_data['color_coherence'] < 0.9:
        recommendations.append("🎨 **Color Issues**: Some cards don't fit the color identity - consider replacements")
    
    if deck_data['mana_curve_score'] < 0.8:
        recommendations.append("⚡ **Mana Curve**: Consider adjusting the mana curve for better balance")
    
    # Creature-specific recommendations
    if creature_stats['creature_count'] > 0:
        if creature_stats['theme_alignment_score'] < 1.0:
            recommendations.append("👹 **Creature Synergy**: Creature stats don't align well with deck themes")
        
        expected_themes = deck_data['expected_themes']
        if 'Aggro' in expected_themes and creature_stats['creature_categories']['large'] > creature_stats['creature_categories']['small']:
            recommendations.append("⚡ **Aggro Focus**: Consider more small, efficient creatures for aggro strategy")
        
        if 'Big Creatures' in expected_themes and creature_stats['avg_power'] < 4:
            recommendations.append("💪 **Big Creatures**: Average creature power is low for a big creatures theme")
        
        if 'Flying' in expected_themes and creature_stats['creature_categories']['evasive'] < creature_stats['creature_count'] * 0.5:
            recommendations.append("🕊️ **Flying Theme**: Consider more creatures with flying or evasion")
    
    # Check for missing card types
    creature_count = creature_stats['creature_count']
    spell_count = len(deck_cards) - creature_count
    
    if creature_count < 4:
        recommendations.append("👹 **Creatures**: Consider adding more creatures for board presence")
    elif creature_count > 10:
        recommendations.append("📜 **Spells**: Consider adding more non-creature spells for versatility")
    
    if not recommendations:
        recommendations.append("✅ **Excellent Balance**: Deck shows great coherence across all metrics including creature synergy!")
    
    for rec in recommendations:
        display(Markdown(f"- {rec}"))


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
                
            card_score, matching_themes = calculate_card_theme_score(oracle_card.iloc[0], expected_themes)
            
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
            theme_score * 0.6 + 
            color_coherence * 0.1 + 
            curve_score * 0.15 + 
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
            'overall_coherence': overall_score,  # Scale to 0-100
            'deck_colors': deck_colors,
            'card_count': len(deck_cards)
        }
    
    return results
