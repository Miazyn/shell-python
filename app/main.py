import sys
import os
import subprocess

def main():
    while True: 
        sys.stdout.write("$ ")
        sys.stdout.flush()

        PATH = os.environ.get("PATH")
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
                paths = PATH.split(':')
                for path in paths:
                    executable_path = os.path.join(path, shell_command)
                    if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
                        print(f"{shell_command} is {executable_path}")
                        found = True
                        break
                if not found:
                    print(f"{shell_command} not found")
        else:
            command_parts = command[0:].split()

            program = command_parts[0]
            arguments = command_parts[1:]

            found = False
            paths = PATH.split(':')
            for path in paths:
                executable_path = os.path.join(path, program)
                if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
                    command_output = subprocess.run([executable_path] + arguments, capture_output=True, text=True)
                    print(command_output.stdout, end='')
                    found = True
                    break
            if not found:   
                sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
