#!/usr/bin/env python3
"""
Secrets Lies Here
Author: Harsh Kumar Singh
Course: Computer Science - Python Programming
Description: A simple command-line diary application that lets a user write 
and read daily entries. Uses exception handling and file I/O operations.
"""

import os
import shutil
from datetime import datetime


class PersonalDiary:
    """
    Class to manage the diary file, backups, and menu actions.
    """

    def __init__(self, diary_file="diary.txt", backup_file="diary_backup.txt"):
        self.diary_file = diary_file
        self.backup_file = backup_file

    def create_backup(self):
        """
        Creates a backup copy of the diary file on startup if it exists.
        """
        try:
            # check if file exists before copying to prevent FileNotFoundError
            if os.path.exists(self.diary_file):
                # shutil copy is used to copy the file contents to backup file
                shutil.copy(self.diary_file, self.backup_file)
                print(f"Backup synchronized to '{self.backup_file}' successfully.")
            else:
                print("Welcome! No existing diary file found. A new one will be created.")
        
        # handle permission errors (e.g., if file is locked or open elsewhere)
        except PermissionError:
            print("Warning: Could not create backup because the file is locked.")
        # catch general I/O exceptions
        except IOError as e:
            print(f"Error copying backup: {e}")
        # catch any other unexpected exceptions to prevent crash
        except Exception as e:
            print(f"Unexpected error during backup: {e}")

    def write_entry(self):
        """
        Appends a new entry with date, time, and custom body text to the file.
        """
        try:
            # Get date and validate format
            date_str = input("\nEnter date (YYYY-MM-DD) [Leave blank for today]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return

        if date_str == "":
            entry_date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                # validation: strptime throws ValueError if the input doesn't match format
                datetime.strptime(date_str, "%Y-%m-%d")
                entry_date = date_str
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
                return

        # Prompt user to input multi-line thoughts
        print("Write your entry. Type 'SAVE' on a new line and press Enter when finished:")
        lines = []
        try:
            while True:
                line = input()
                if line.strip().upper() == "SAVE":
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            # catch EOF/Interrupt gracefully so it stops reading input without crashing
            pass

        if len(lines) == 0:
            print("Entry is empty. Nothing saved.")
            return
        
        content = "\n".join(lines)

        # open in append mode ('a') to add content to the end of file
        try:
            with open(self.diary_file, "a", encoding="utf-8") as file:
                file.write(f"\n==================================================\n")
                file.write(f"📅 Date: {entry_date}\n")
                file.write(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n")
                file.write(f"==================================================\n")
                file.write(content + "\n")
            print("\nSuccess: Entry saved to your diary!")
        
        # error handling for file system issues
        except PermissionError:
            print("\nError: Permission denied. Cannot write to file.")
        except IOError as e:
            print(f"\nError writing to diary file: {e}")

    def read_entries(self):
        """
        Reads and prints the entire diary file contents.
        """
        try:
            # open file in read mode
            with open(self.diary_file, "r", encoding="utf-8") as file:
                content = file.read()
            
            if content.strip() == "":
                print("\nDiary file is currently empty.")
                return

            print("\n==================== YOUR DIARY ====================")
            print(content.strip())
            print("====================================================")
        
        # handle exception when file does not exist yet
        except FileNotFoundError:
            print("\nError: No diary file exists yet. Try writing a new entry first.")
        except PermissionError:
            print("\nError: Permission denied. Cannot read file.")
        except IOError as e:
            print(f"\nError reading from file: {e}")

    def clear_all(self):
        """
        Deletes the main diary file and backup file after user confirmation.
        """
        try:
            confirm = input("\nAre you sure you want to delete all entries? (yes/no): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return

        if confirm != "yes":
            print("Delete operation cancelled.")
            return

        # remove main file
        try:
            if os.path.exists(self.diary_file):
                os.remove(self.diary_file)
                print(f"Diary file '{self.diary_file}' has been deleted.")
            else:
                print("Diary file does not exist.")
        except PermissionError:
            print("Error: Permission denied. Cannot delete file.")
        except OSError as e:
            print(f"OS Error deleting file: {e}")

        # remove backup file
        try:
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
                print(f"Backup file '{self.backup_file}' has been deleted.")
        except OSError as e:
            print(f"Error deleting backup file: {e}")

    def run(self):
        """
        Primary console loop for managing user interaction.
        """
        print("========================================")
        print("         My Secret Personal Diary       ")
        print("========================================")
        
        # run backup routine on start
        self.create_backup()

        try:
            while True:
                print("\n--- MAIN MENU ---")
                print("1. Write a new entry")
                print("2. Read all entries")
                print("3. Delete diary files")
                print("4. Exit")
                
                choice = input("\nEnter choice (1-4): ").strip()
                
                if choice == "1":
                    self.write_entry()
                elif choice == "2":
                    self.read_entries()
                elif choice == "3":
                    self.clear_all()
                elif choice == "4":
                    print("\nGoodbye!\n")
                    break
                else:
                    print("Invalid option. Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting application. Goodbye!\n")


if __name__ == "__main__":
    # Create object instance and start application
    app = PersonalDiary()
    app.run()
