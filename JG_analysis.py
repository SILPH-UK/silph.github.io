# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 19:07:28 2025

@author: jemma
"""

import os
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates


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


# Filter the cards with names ending in 'ACESPEC'
acespec_cards = complete_decklists[complete_decklists['Card Name'].str.endswith('ACESPEC')]
# Group by card name and sum the quantities
acespec_summary = acespec_cards.groupby('Card Name')['Quantity'].sum().reset_index()
# Sort by quantity in descending order
acespec_summary_sorted = acespec_summary.sort_values(by='Quantity', ascending=False)
# Export to CSV
output_file_path = os.path.join(current_directory, 'acespec_cards_summary.csv')
acespec_summary_sorted.to_csv(os.path.join(current_directory, 'results', 'acespec_cards_summary.csv'), index=False)


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
    
    
    
#%% decklists over time
# Count number of times each deck type was played at each tournament
# Ensure 'Date' is in datetime format
complete_standings['Date'] = pd.to_datetime(complete_standings['Date'])

# Get overall min and max dates
min_date = complete_standings['Date'].min()
max_date = complete_standings['Date'].max()

# Count number of times each deck type was played at each tournament
deck_trends = complete_standings.groupby(['Date', 'Deck']).size().reset_index(name='Count')

total_decks_per_tournament = complete_standings.groupby('Date').size().reset_index(name='Total Decks')
deck_trends = deck_trends.merge(total_decks_per_tournament, on='Date', how='left')
deck_trends['Percentage'] = (deck_trends['Count'] / deck_trends['Total Decks']) * 100

# Set plot style
sns.set_style("whitegrid")

# Loop through each deck and create a separate graph
for deck in deck_trends['Deck'].unique():
    deck_data = deck_trends[deck_trends['Deck'] == deck]
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    ax1.plot(deck_data['Date'], deck_data['Count'], marker='o', linestyle='-', color='b', label="Number of Players")
    ax2.plot(deck_data['Date'], deck_data['Percentage'], marker='s', linestyle='--', color='r', label="% of Total Decks")
    
    ax1.set_xlabel("Tournament Date")
    ax1.set_ylabel("Number of Players Using Deck", color='b')
    ax2.set_ylabel("Percentage of Total Decks (%)", color='r')
    
    ax1.set_yticks(range(0, max(deck_data['Count']) + 1))  # Ensure only integer values on primary y-axis
    ax2.set_yticks(range(0, 101, 10))  # Ensure percentage scale from 0 to 100 with steps of 10
    
    ax1.set_xlim(min_date, max_date)  # Set x-axis limits to dataset-wide min and max dates
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # Ensure uniform x-axis grid lines every 7 days
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.tick_params(axis='x', rotation=45)
    
    plt.title(f"Popularity of {deck} Over Time")
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.tight_layout()
    
    # Save each plot to a file
    plt.savefig(f"deck_popularity_{deck.replace(' ', '_')}.png")
    plt.show()
