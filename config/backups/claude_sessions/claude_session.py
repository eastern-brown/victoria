#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from claude_tracker import create_tracker

def print_usage():
    print("""
Usage:
    python3 config/backups/claude_sessions/claude_session.py <command> [args]

Commands:
    start "description"  - Start a new session with description
    list                - List all available sessions
    restore session_id  - Restore to a previous session
    
Example:
    python3 config/backups/claude_sessions/claude_session.py start "Working on memory handler"
    python3 config/backups/claude_sessions/claude_session.py list
    python3 config/backups/claude_sessions/claude_session.py restore session_20241214_050321
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    tracker = create_tracker()
    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            description = input("Enter session description: ")
        else:
            description = sys.argv[2]
        
        session_id, files = tracker.start_session(description)
        print(f"\nStarted session: {session_id}")
        print(f"Description: {description}")
        print(f"Backed up {len(files)} files")
        print("Ready to work with Claude!")

    elif command == "list":
        sessions = tracker.list_sessions()
        if not sessions:
            print("No sessions found")
            return
            
        print("\nAvailable sessions:")
        for session in sessions:
            print(f"\nID: {session['id']}")
            print(f"Description: {session['description']}")
            print(f"Time: {session['timestamp']}")
            print(f"Files: {len(session['files'])} files backed up")

    elif command == "restore":
        if len(sys.argv) < 3:
            print("Error: Please provide a session ID to restore")
            return
            
        session_id = sys.argv[2]
        try:
            files = tracker.restore_session(session_id)
            print(f"\nRestored {len(files)} files from session {session_id}")
            print("Workspace restored to previous state!")
        except ValueError as e:
            print(f"Error: {str(e)}")

    else:
        print(f"Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()