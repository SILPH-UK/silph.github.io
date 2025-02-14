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

# Process directories with dd-mm-yyyy naming
for item in files_in_results:
    item_path = os.path.join(results_directory, item)
    
    # Check if the item is a directory and matches the dd-mm-yyyy pattern
    if os.path.isdir(item_path) and len(item.split('-')) == 3:
        day, month, year = item.split('-')
        if day.isdigit() and month.isdigit() and year.isdigit():            
            if os.path.exists(os.path.join(item_path, 'standings.csv')):                
                standings = pd.read_csv(os.path.join(item_path, 'standings.csv'), header=None)              
                standings.columns = ['Rank', 'Player', 'Deck', 'Total Points', 'Won', 'Lost', 'Draw']
                standings['Date'] = f"{day}-{month}-{year}"
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
        
    
    complete_standings.groupby('Player')['Total Points'].max()\
    .reset_index()\
    .sort_values(by='Total Points', ascending=False)\
    .to_csv(os.path.join(current_directory, 'results', 'top_players_to_date.csv'), index=False)


    complete_standings.groupby('Deck')['Total Points'].max()\
    .reset_index()\
    .sort_values(by='Total Points', ascending=False)\
    .to_csv(os.path.join(current_directory, 'results', 'best_performing_decks_to_date_by_points.csv'), index=False)

    
    merged_df.groupby(['Deck', 'Card Name'])['Quantity'].mean().reset_index()\
        .sort_values(by=['Deck', 'Quantity'], ascending=[True, False])\
        .to_csv(os.path.join(current_directory, 'results', 'card_popularity_by_deck.csv'), index=False)
    average_cards_by_decktype=merged_df.groupby(['Deck', 'Card Name'])['Quantity'].mean().reset_index()\
        .sort_values(by=['Card Name', 'Quantity'], ascending=[True, False])

    
    
else:
    print("No decklist data to process.")
    
    
    
    