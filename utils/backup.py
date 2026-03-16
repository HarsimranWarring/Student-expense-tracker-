import os
import shutil
from datetime import datetime

class BackupManager:
    def __init__(self, backup_location):
        self.backup_location = backup_location

    def create_backup(self, source):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f'backup_{timestamp}'
        backup_path = os.path.join(self.backup_location, backup_filename)
        if not os.path.exists(self.backup_location):
            os.makedirs(self.backup_location)
        shutil.copytree(source, backup_path)
        print(f'Backup created at: {backup_path}')

    def restore_backup(self, backup_filename, target):
        backup_path = os.path.join(self.backup_location, backup_filename)
        if os.path.exists(backup_path):
            shutil.copytree(backup_path, target)
            print(f'Backup restored from: {backup_path}')
        else:
            print(f'Backup not found: {backup_path}')
