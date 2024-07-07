import subprocess

def update_repository():
    try:
        # Pull the latest changes from the repository
        subprocess.run(["git", "pull"], check=True)
        print("Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating repository: {e}")
        return False
    return True

def apply_changes():
    try:
        # Run the bot
        subprocess.run(["python3", "main.py"], check=True)
        print("Bot started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting the bot: {e}")
        return False
    return True

def main():
    if update_repository():
        apply_changes()

if __name__ == "__main__":
    main()
