import os
import subprocess
import readline

# Function for auto completion
def complete(text, state):
    options = [cmd for cmd in os.listdir('.') if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def main():

    while True:

        try:

            # Display a simple prompt
            command = input("myshell> ")

            # Handle empty commands
            command = command.strip()
            if not command:
                continue

            command = command.lower()

            # Exit the shell
            if command in ['exit', 'quit']:
                break

            # Execute the command on default Linux shell
            subprocess.run(command, shell=True)

        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to leave the shell.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":

    main()
