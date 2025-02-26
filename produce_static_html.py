# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 21:29:47 2025

@author: jemma
"""

import os
import pandas as pd
import re
import logging
from jinja2 import Environment, FileSystemLoader
from pokemontcgsdk import RestClient, Card
from concurrent.futures import ThreadPoolExecutor

# Configure API key
RestClient.configure('3c23674e-0a0e-4a9d-8191-43fcbd09f2f4')

# Paths
current_directory = os.getcwd()
results_path = os.path.join(current_directory, 'results')
output_dir = os.path.join(current_directory, 'static_site')

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Jinja2 setup
env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
tournament_template = env.get_template('tournament.html')
decklist_template = env.get_template('decklist.html')

# Regex for YYYY-MM-DD format
date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def fetch_card_image(index, row):
    """Fetches the image URL for a given card row."""
    ptcgo_code = row['Set Code']
    card_number = row['Set Number']
    card_name = row["Card Name"].replace(' - ACESPEC', '')
    

    try:
        try:
             cards = Card.where(q=f'set.ptcgoCode:{ptcgo_code} number:{int(card_number)}')
        except Exception as e:
            cards = Card.where(q=f'set.ptcgoCode:{ptcgo_code} number:{str(card_number)}')
            
        #card_number_str = str(card_number)  # Ensure it's a string
        #card_number_query = f'number:{int(card_number_str)}' if card_number_str.isdigit() else f'number:"{card_number_str}"'
        #cards = Card.where(q=f'set.ptcgoCode:{ptcgo_code} {card_number_query}')
            
        if cards:
            #print(cards[0].images.small)
            return index, cards[0].images.small  
        
        common_cards = Card.where(q=f'name:"{card_name}" rarity:"Common"', orderBy='-set.releaseDate')
        uncommon_cards = Card.where(q=f'name:"{card_name}" rarity:"Uncommon"', orderBy='-set.releaseDate')

        if len(common_cards) == 0 and len(uncommon_cards) == 0:
            rare_cards = Card.where(q=f'name:"{card_name}" rarity:"Rare"', orderBy='-set.releaseDate')
            all_cards = list(common_cards) + list(uncommon_cards) + list(rare_cards)
        else:
            all_cards = list(common_cards) + list(uncommon_cards)
        
        all_cards.sort(key=lambda card: card.set.releaseDate, reverse=True)

        if all_cards:
            #print( all_cards[0].images.small )
            return index, all_cards[0].images.small  
    
        card_name = row["Card Name"].lower().replace('ké', 'k*').replace(' 3.0','').lower()
        
        Card.where(q=f'name:"{card_name}"', orderBy='-set.releaseDate')
        if cards:
            #print(cards[0].images.small)
            return index, cards[0].images.small  
        print(card_name)
            
    except Exception as e:
        print(f"Error fetching card image for {card_name}: {e}")

    return index, "https://media.istockphoto.com/id/1443562748/photo/cute-ginger-cat.jpg?s=612x612&w=0&k=20&c=vvM97wWz-hMj7DLzfpYRmY2VswTqcFEKkC437hxm3Cg="


def process_decklist(df):
    """Processes the decklist to fetch card images."""
    df['Image URL'] = None  

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_card_image, index, row): index for index, row in df.iterrows()}

        for future in futures:
            index, image_url = future.result()
            df.at[index, 'Image URL'] = image_url  

    return df


def generate_index():
    """Generates the main index page listing all tournaments."""
    tournaments = sorted(
        d for d in os.listdir(results_path)
        if date_pattern.match(d) and os.path.isdir(os.path.join(results_path, d))
    )

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(index_template.render(tournaments=tournaments, path=os.getcwd()))
    print(f"Generated: {output_path}")


def generate_tournament_pages():
    """Generates tournament pages listing all decklists."""
    tournaments = sorted(
        d for d in os.listdir(results_path)
        if date_pattern.match(d) and os.path.isdir(os.path.join(results_path, d))
    )

    for date in tournaments:
        decklist_dir = os.path.join(results_path, date, 'decklists')
        os.makedirs(os.path.join(output_dir, date), exist_ok=True)

        players = [f[:-4] for f in os.listdir(decklist_dir) if f.endswith('.csv')]

        output_path = os.path.join(output_dir, date, "index.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tournament_template.render(date=date, players=players, path=os.getcwd()))
        print(f"Generated: {output_path}")


def generate_decklist_pages():
    """Generates individual decklist pages for each player."""
    tournaments = sorted(
        d for d in os.listdir(results_path)
        if date_pattern.match(d) and os.path.isdir(os.path.join(results_path, d))
    )

    for date in tournaments:
        decklist_dir = os.path.join(results_path, date, 'decklists')
        for player_file in os.listdir(decklist_dir):
            if not player_file.endswith('.csv'):
                continue

            player = player_file[:-4]  
            decklist_path = os.path.join(decklist_dir, player_file)
            df = pd.read_csv(decklist_path, header=None)
            df.columns = ['Card Name', 'Quantity', 'Card Type', 'Set Code', 'Set Number']
            

            df['Set Number'] = df['Set Number'].fillna(0)
            df = process_decklist(df)
            df['Set Number'] = pd.to_numeric(df['Set Number'], errors='coerce').fillna(0).astype(int).astype(str)
            df.loc[df['Set Number'] == '0', 'Set Number'] = ''  # Replace '0' with an empty string
            df['Set Code'] = df['Set Code'].fillna('')            
            player_output_dir = os.path.join(output_dir, date)
            os.makedirs(player_output_dir, exist_ok=True)

            output_path = os.path.join(player_output_dir, f"{player}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(decklist_template.render(date=date, player=player, decklist=df))
            print(f"Generated: {output_path}")


if __name__ == '__main__':
    generate_index()
    generate_tournament_pages()
    generate_decklist_pages()
