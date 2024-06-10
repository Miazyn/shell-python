import sys


def main():
    while True: 
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()

        if command == 'exit 0':
            sys.exit(0)
        elif command.startswith('echo '):
            print(command[5: ])
        elif command.startswith('type '):
            shell_command = command[5: ]
            if shell_command in ['echo', 'type', 'exit']:
                print(f"{shell_command} is a shell builtin")
            else:
                found = False
                for path in os.environment.get('PATH', '').split(':'):
                    executable_path = os.path.join(path, shell_command)
                    if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
                        print(f"{shell_command} is {executable_path}")
                        found = True
                        break
                if not found:
                    print(f"{shell_command} not found")
        else:
            sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
