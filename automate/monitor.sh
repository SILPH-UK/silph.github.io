#!/bin/bash

# Configuration
WATCH_FOLDER="$HOME/Documents/WatchFolder"  # Folder to monitor
DESTINATION_FOLDER="$HOME/Documents/Destination"  # Where to copy files
FILE_PREFIX="processed_"  # Prefix to add to renamed files
LOG_FILE="$HOME/Documents/file_monitor.log"

# Create directories if they don't exist
mkdir -p "$WATCH_FOLDER"
mkdir -p "$DESTINATION_FOLDER"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOG_FILE"
}

# Function to process a file
process_file() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    local extension="${filename##*.}"
    local basename="${filename%.*}"
    
    # Skip hidden files and temporary files
    if [[ "$filename" == .* ]] || [[ "$filename" == *~ ]]; then
        return
    fi
    
    # Only process files ending in pairings.html or standings.html
    if [[ "$filename" != *"pairings.html" ]] && [[ "$filename" != *"standings.html" ]]; then
        log_message "SKIPPED: '$filename' - does not match required pattern"
        return
    fi
    
    # Wait a moment to ensure file is fully written
    sleep 1
    
    # Check if file still exists (in case it was moved/deleted)
    if [[ ! -f "$file_path" ]]; then
        return
    fi
    
    # Create new filename with prefix
    local new_filename="${FILE_PREFIX}${basename}.${extension}"
    local destination_path="${DESTINATION_FOLDER}/${new_filename}"
    
    # Handle filename conflicts by adding a number
    local counter=1
    while [[ -f "$destination_path" ]]; do
        new_filename="${FILE_PREFIX}${basename}_${counter}.${extension}"
        destination_path="${DESTINATION_FOLDER}/${new_filename}"
        ((counter++))
    done
    
    # Copy the file (keeping original in place)
    if cp "$file_path" "$destination_path"; then
        log_message "SUCCESS: Copied '$filename' to '$new_filename' (original kept in source)"
        echo "File processed: $filename -> $new_filename (original preserved)"
    else
        log_message "ERROR: Failed to copy '$filename'"
        echo "Error copying file: $filename"
    fi
}

# Main monitoring function using fswatch
monitor_folder() {
    log_message "Starting file monitor for: $WATCH_FOLDER"
    echo "Monitoring $WATCH_FOLDER for new files..."
    echo "Press Ctrl+C to stop"
    
    # Use fswatch to monitor the folder (only HTML files)
    fswatch -0 -e ".*" -i ".*pairings\\.html$" -i ".*standings\\.html$" "$WATCH_FOLDER" | while IFS= read -r -d '' file; do
        # Only process regular files that were created or modified
        if [[ -f "$file" ]]; then
            process_file "$file"
        fi
    done
}

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo "fswatch is not installed. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install fswatch
    else
        echo "Homebrew not found. Please install fswatch manually:"
        echo "brew install fswatch"
        exit 1
    fi
fi

# Start monitoring
monitor_folder