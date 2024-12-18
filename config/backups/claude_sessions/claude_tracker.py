# /home/ernsttulle/ivanka/config/backups/claude_sessions/claude_tracker.py

import os
import json
from datetime import datetime
import shutil

class ClaudeSessionTracker:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.sessions_dir = os.path.join(project_dir, 'config/backups/claude_sessions/sessions')
        self.metadata_file = os.path.join(self.sessions_dir, 'sessions.json')
        self.setup_directories()
        self.load_metadata()

    def setup_directories(self):
        os.makedirs(self.sessions_dir, exist_ok=True)

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {'sessions': []}
            self.save_metadata()

    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def start_session(self, description=""):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_id = f"session_{timestamp}"
        session_dir = os.path.join(self.sessions_dir, session_id)

        # Create session directory
        os.makedirs(session_dir, exist_ok=True)

        # Copy only Python files and other important files
        backed_up_files = []
        for item in os.listdir(self.project_dir):
            if item.startswith('.') or item == '__pycache__' or item == 'backups':
                continue

            src = os.path.join(self.project_dir, item)
            dst = os.path.join(session_dir, item)

            if os.path.isfile(src):
                try:
                    shutil.copy2(src, dst)
                    backed_up_files.append(item)
                except Exception as e:
                    print(f"Warning: Could not copy {item}: {str(e)}")

        # Record session
        session_data = {
            'id': session_id,
            'timestamp': timestamp,
            'description': description,
            'files': backed_up_files,
            'active': True
        }

        self.metadata['sessions'].append(session_data)
        self.save_metadata()

        return session_id, backed_up_files

    def restore_session(self, session_id):
        session_dir = os.path.join(self.sessions_dir, session_id)
        if not os.path.exists(session_dir):
            raise ValueError(f"Session {session_id} not found")

        # Backup current state first
        backup_id, _ = self.start_session("Auto-backup before restore")

        # Restore files from session
        restored_files = []
        for item in os.listdir(session_dir):
            src = os.path.join(session_dir, item)
            dst = os.path.join(self.project_dir, item)

            if os.path.isfile(src):
                try:
                    shutil.copy2(src, dst)
                    restored_files.append(item)
                except Exception as e:
                    print(f"Warning: Could not restore {item}: {str(e)}")

        return restored_files

    def list_sessions(self):
        return self.metadata['sessions']

    def get_session(self, session_id):
        for session in self.metadata['sessions']:
            if session['id'] == session_id:
                return session
        return None

def create_tracker(project_dir="."):
    return ClaudeSessionTracker(project_dir)