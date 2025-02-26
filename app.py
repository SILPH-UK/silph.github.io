# -*- coding: utf-8 -*-
"""


@author: jemma
"""

from flask import Flask, render_template, send_file
import os
import pandas as pd
import re
import logging
from pokemontcgsdk import RestClient
from pokemontcgsdk import Card
import sys
from concurrent.futures import ThreadPoolExecutor
RestClient.configure('3c23674e-0a0e-4a9d-8191-43fcbd09f2f4')



app = Flask(__name__)
current_directory = os.getcwd()
logging.basicConfig(level=logging.DEBUG)
sys.stdout = sys.__stdout__  # Ensures direct console printing

@app.route('/')
def index():
    results_path = os.path.join(current_directory, 'results')

    # Regular expression pattern for YYYY-MM-DD format
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    
    # Get sorted list of directories/files
    tournaments = sorted(      
    d for d in os.listdir(results_path)
        if date_pattern.match(d) and os.path.isdir(os.path.join(results_path, d))
        )
    
    return render_template('index.html', tournaments=tournaments)

@app.route('/tournament/<date>')
def tournament(date):
    decklist_dir = os.path.join(current_directory, 'results', date, 'decklists')
    players = [f[:-4] for f in os.listdir(decklist_dir) if f.endswith('.csv')]
    return render_template('tournament.html', date=date, players=players)


def fetch_card_image(index, row):
    """Fetches the image URL for a given card row."""
    ptcgo_code = row['Set Code']
    card_number = row['Set Number']
    card_name = row["Card Name"].replace(' - ACESPEC', '')

    print(f"Details: {card_name}, {ptcgo_code} - {card_number}", flush=True)

    try:
        cards = Card.where(q=f'set.ptcgoCode:{ptcgo_code} number:{int(card_number)}')

        if cards:
            return index, cards[0].images.small  # Return the index and URL

        print(f"Querying: name: {card_name}", flush=True)

        # Search by name for common and uncommon rarities
        common_cards = Card.where(q=f'name:"{card_name}" rarity:"Common"', orderBy='-set.releaseDate')
        uncommon_cards = Card.where(q=f'name:"{card_name}" rarity:"Uncommon"', orderBy='-set.releaseDate')
        if len(common_cards)==0 and len(uncommon_cards)==0:
            rare_cards = Card.where(q=f'name:"{card_name}" rarity:"Rare"', orderBy='-set.releaseDate')
            all_cards = list(common_cards) + list(uncommon_cards) + list(rare_cards)
        else:
            all_cards = list(common_cards) + list(uncommon_cards)
        all_cards.sort(key=lambda card: card.set.releaseDate, reverse=True)

        if all_cards:
            return index, all_cards[0].images.small  # Return first result

        print(f"No results found for: {card_name}")
    except Exception as e:
        print(f"Error fetching card image for {card_name}: {e}")

    # Default image if no match found
    return index, "https://media.istockphoto.com/id/1443562748/photo/cute-ginger-cat.jpg?s=612x612&w=0&k=20&c=vvM97wWz-hMj7DLzfpYRmY2VswTqcFEKkC437hxm3Cg="


def process_decklist(df):
    """Processes the decklist concurrently to fetch images."""
    df['Image URL'] = None  # Default column for image URLs

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust worker count as needed
        futures = {executor.submit(fetch_card_image, index, row): index for index, row in df.iterrows()}

        for future in futures:
            index, image_url = future.result()  # Retrieve results
            df.at[index, 'Image URL'] = image_url  # Update DataFrame

    return df


@app.route('/tournament/<date>/<player>')
def player_deck(date, player):
    decklist_path = os.path.join(current_directory, 'results', date, 'decklists', f'{player}.csv')
    df = pd.read_csv(decklist_path, header=None)
    df.columns = ['Card Name', 'Quantity', 'Card Type', 'Set Code', 'Set Number']
    df['Set Number'] = df['Set Number'].fillna(0).astype(int)

    df = process_decklist(df)  # Process images concurrently

    print(df)
    return render_template('decklist.html', date=date, player=player, decklist=df)

if __name__ == '__main__':
    app.run(debug=True)