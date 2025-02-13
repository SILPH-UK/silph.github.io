# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 19:07:28 2025

@author: jemma
"""

import os
import pandas as pd 



#%% Load Results
current_directory = os.getcwd()
results_directory = os.path.join(current_directory, 'results')

all_standings = []
all_decklists = []

files_in_results = os.listdir(results_directory)

# Process directories with yyyy-mm-dd naming
for item in files_in_results:
    item_path = os.path.join(results_directory, item)
    
    # Check if the item is a directory and matches the yyyy-mm-dd pattern
    if os.path.isdir(item_path) and len(item.split('-')) == 3:
        year, month, day = item.split('-')
        if year.isdigit() and month.isdigit() and day.isdigit():            
            if os.path.exists(os.path.join(item_path, 'standings.csv')):                
                standings = pd.read_csv(os.path.join(item_path, 'standings.csv'), header=None)              
                standings.columns = ['Rank', 'Player', 'Deck', 'Total Points', 'Won', 'Lost', 'Draw']
                standings['Date'] = f"{year}-{month}-{day}"
                all_standings.append(standings)
                del standings
            else:
                print(f"'standings.csv' not found in {item_path}.")
                
    decklist_path = os.path.join(item_path,"decklists")
    if os.path.isdir(decklist_path):
        print(f"Processing decklists in {decklist_path}")
        
        decklist_files = [f for f in os.listdir(decklist_path) if f.lower().endswith('.csv')]
        
        for decklist_file in decklist_files:
            decklist_file_path = os.path.join(decklist_path, decklist_file)
            
            try:
                decklist_df = pd.read_csv(decklist_file_path, header=None)
                decklist_df.columns = ['Card Name', 'Quantity', 'Card Type', 'Set Code', 'Set Number']
                decklist_df['Player'] = str(decklist_file)[0:len(str(decklist_file))-4]
                decklist_df['Date'] = f"{day}-{month}-{year}"
                
                all_decklists.append(decklist_df)
                del decklist_df
            except Exception as e:
                print(f"Error reading {decklist_file_path}: {e}")

        
        
# Combine all standings DataFrames into a single DataFrame
if all_standings:
    complete_standings = pd.concat(all_standings, ignore_index=True).reset_index()
    print(f"Combined standings DataFrame created with {len(complete_standings)} rows.")
else:
    complete_standings = pd.DataFrame()  # Create an empty DataFrame if no data was found
    print("No standings data found.")


# Combine all decklists DataFrames into one DataFrame
if all_decklists:
    complete_decklists = pd.concat(all_decklists, ignore_index=True).reset_index()
    print(f"Combined decklists DataFrame created with {len(complete_decklists)} rows.")
else:
    complete_decklists = pd.DataFrame() 
    print("No decklists data found.")

del decklist_path, day, month, year
del decklist_files
complete_decklists['Player'] = complete_decklists['Player'].str.replace('-', ' ', regex=False)
complete_standings['Player'] = complete_standings['Player'].str.replace('-', ' ', regex=False)
#print(complete_standings)
#print(complete_decklists)



merged_df = pd.merge(complete_decklists, complete_standings[['Player', 'Deck']], left_on='Player',right_on='Player', how='left')
#print(merged_df)

#%% Process results
if not complete_decklists.empty:
     
   
    combined_df = (complete_decklists.groupby(['Date', 'Card Name'])['Quantity']
                   .sum()
                   .reset_index()
                   .sort_values(by=['Date', 'Quantity'], ascending=[True, False])
                   .merge(complete_decklists.groupby('Date')['Player']
                          .nunique()
                          .reset_index()
                          .rename(columns={'Player': 'Total Decks'}), on='Date', how='left'))
    combined_df['Average In Deck'] = combined_df['Quantity'] / combined_df['Total Decks']
    combined_df.to_csv(os.path.join(current_directory, 'results', 'most_used_cards_by_date.csv'), index=False)
        
    # Convert 'Won' and 'Draw' to numeric
    complete_standings['Won'] = pd.to_numeric(complete_standings['Won'], errors='coerce')
    complete_standings['Draw'] = pd.to_numeric(complete_standings['Draw'], errors='coerce')

    # Calculate the custom score: 3 points per win, 1 point per draw
    complete_standings['Custom Points'] = (complete_standings['Won'] * 3) + (complete_standings['Draw'])

    # Group by player and aggregate wins, draws, and total points
    player_summary = complete_standings.groupby('Player').agg(
        Wins=('Won', 'sum'),
        Draws=('Draw', 'sum'),
        Total=('Custom Points', 'sum')
    ).reset_index()

    # Sort by total custom points
    player_summary = player_summary.sort_values(by='Total', ascending=False)

    # Save the results to a CSV
    player_summary.to_csv(os.path.join(current_directory, 'results', 'top_players_with_wins_draws_points.csv'), index=False)


    # Group by deck and aggregate wins, draws, and total points
    deck_summary = complete_standings.groupby('Deck').agg(
        Wins=('Won', 'sum'),
        Draws=('Draw', 'sum'),
        Total=('Custom Points', 'sum')
    ).reset_index()

    # Sort by total custom points
    deck_summary = deck_summary.sort_values(by='Total', ascending=False)

    # Save the results to a CSV
    deck_summary.to_csv(os.path.join(current_directory, 'results', 'top_decks_with_wins_draws_points.csv'), index=False)


    complete_standings.groupby('Deck')['Custom Points'].sum()\
        .reset_index()\
        .sort_values(by='Custom Points', ascending=False)\
        .to_csv(os.path.join(current_directory, 'results', 'best_performing_decks_to_date_by_points.csv'), index=False)

    
    merged_df.groupby(['Deck', 'Card Name'])['Quantity'].mean().reset_index()\
        .sort_values(by=['Deck', 'Quantity'], ascending=[True, False])\
        .to_csv(os.path.join(current_directory, 'results', 'card_popularity_by_deck.csv'), index=False)
    average_cards_by_decktype=merged_df.groupby(['Deck', 'Card Name'])['Quantity'].mean().reset_index()\
        .sort_values(by=['Card Name', 'Quantity'], ascending=[True, False])

    
    
else:
    print("No decklist data to process.")
    
    
    
    