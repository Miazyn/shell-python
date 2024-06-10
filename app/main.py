import sys
import os
import subprocess

def main():
    while True: 
        sys.stdout.write("$ ")
        sys.stdout.flush()

        PATH = os.environ.get("PATH")
        cwd = os.getcwd()
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
        elif command == 'pwd':
            print(f"{cwd}")
        elif command.startswith('cd '):
            new_directory = command[3:].strip()
            if new_directory.startswith('.'):
                full_path = os.path.join(cwd, new_directory)
                try:
                   os.chdir(full_path)
                except FileNotFoundError:
                    print(f"cd: {full_path}: No such file or directory")
            elif new_directory.startswith('~'):
                home_directory = os.path.expanduser("~")
                os.chdir(home_directory)

            else:
                try:
                    os.chdir(new_directory)
                except FileNotFoundError:
                    print(f"cd: {new_directory}: No such file or directory")
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
