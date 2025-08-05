#!/bin/bash

# Configuration
WATCH_FOLDER="/Users/pokemon/TOM_DATA/data/reports"  # Folder to monitor
DESTINATION_FOLDER="/Users/pokemon/GitHUb/silph.github.io"  # Where to copy files (should be a Git repo)
FILE_PREFIX="processed_"  # Prefix to add to renamed files
LOG_FILE="$HOME/Documents/file_monitor.log"

# Git Configuration
GIT_ENABLED=true  # Set to false to disable Git operations
COMMIT_MESSAGE="Auto-update pairings.html"  # Default commit message
GIT_BRANCH="main"  # Branch to push to (change to "master" if needed)

# Create directories if they don't exist
mkdir -p "$WATCH_FOLDER"
mkdir -p "$DESTINATION_FOLDER"

# Function to push to Git
git_push() {
    local file_path="$1"
    local original_filename="$2"
    
    if [[ "$GIT_ENABLED" != true ]]; then
        return
    fi
    
    # Change to the destination directory
    cd "$DESTINATION_FOLDER" || {
        log_message "ERROR: Cannot change to destination directory for Git operations"
        return 1
    }
    
    # Check if this is a Git repository
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        log_message "ERROR: Destination folder is not a Git repository"
        echo "Error: $DESTINATION_FOLDER is not a Git repository"
        echo "Run: cd '$DESTINATION_FOLDER' && git init && git remote add origin <your-repo-url>"
        return 1
    fi
    
    # Add the file to Git
    if git add "pairings.html"; then
        log_message "GIT: Added pairings.html to staging"
    else
        log_message "ERROR: Failed to add pairings.html to Git"
        return 1
    fi
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        log_message "GIT: No changes to commit"
        return 0
    fi
    
    # Create commit message with timestamp and original filename
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local commit_msg="$COMMIT_MESSAGE - $timestamp (from: $original_filename)"
    
    # Commit the changes
    if git commit -m "$commit_msg"; then
        log_message "GIT: Committed changes - $commit_msg"
    else
        log_message "ERROR: Failed to commit changes"
        return 1
    fi
    
    # Push to remote repository
    if git push origin "$GIT_BRANCH"; then
        log_message "GIT: Successfully pushed to origin/$GIT_BRANCH"
        echo "Git: Pushed to GitHub successfully"
    else
        log_message "ERROR: Failed to push to origin/$GIT_BRANCH"
        echo "Git: Failed to push to GitHub (check network/credentials)"
        return 1
    fi
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
    
    # Always rename to pairings.html (overwrite if exists)
    local new_filename="pairings.html"
    local destination_path="${DESTINATION_FOLDER}/${new_filename}"
    
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