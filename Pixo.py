"""
Copyright 2026 Art Beqiri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import os
import re
import sys

info = "Pixo Programming Language v1.0 - (April 2026 - June 2026, Kosovo)"

instruction = "Type 'help' for more information or type 'exit' to quit."

print(f"{info}")
print(f"{instruction}\n")

print_command = "print"
let_command = "let"
ask_command = "ask"
save_character = "->"
exit_command = "exit"
if_command = "if"
function_command = "func"
run_function_command = "run function"
run_file_command = "run file"
end_command = "end"
forever_command = "forever"
help_command = "help"
clear_command = "clear"
end_character = ":"
comment_command = "#"

commands = [print_command, let_command, ask_command, exit_command, if_command, function_command, run_function_command, run_file_command, forever_command, help_command, clear_command, comment_command]

variables = {
    "true": True,
    "false": False
}

functions = {}

def print_function(code):
    parts = code.split(maxsplit=1)

    if not parts or parts[0] != print_command:
        return

    string = parts[1] if len(parts) > 1 else ""
    string = string.strip()

    if not string:
        print(f"Syntax Error in '{code}': There was no value to print!")
        return

    if string.strip() == '"' or string.strip() == "'":
        print(f"Syntax Error: Unclosed quotes in '{code}'.")
        return
    
    if string.startswith('"') and string.endswith("'") or string.startswith("'") and string.endswith('"'):
        print(f"Syntax Error in '{code}': Cannot print a string with different quotes!")
        return

    if any(op in string for op in ["+", "-", "*", "/", "**", "%"]):

        if not re.match(r'^[0-9a-zA-Z_+\-*/%()\s\'."]+$', string):
            print(f"Security Error in '{code}': Invalid characters!")
            return

        try:
            result = eval(string, {"__builtins__": None}, variables)
            print(result)
            return
        
        except Exception as e:
            print(f"Error in '{code}': {e}")
            return
        
    starts_with_quote = string.startswith(('"', "'"))
    ends_with_quote = string.endswith(('"', "'"))

    if starts_with_quote or ends_with_quote:
        if starts_with_quote and ends_with_quote:
            print(string[1:-1])
        else:
            print(f"Syntax Error: Unclosed quotes in '{code}'.")
        return

    if string.isdigit():
        print(string)
        return

    if string in variables:
        print(variables[string])
        return

    else:
        print(f"Syntax Error: Unclosed quotes in '{code}'.")
        return

def let_function(code):
    if "=" not in code:
        print(f"Syntax Error in '{code}': Missing '='!")
        return

    try:
        left, right = code[len(let_command):].split("=", 1)

        var_name = left.strip()
        value = right.strip()

        if not var_name:
            print(f"Name Error in '{code}': No variable name!")
            return

        if not var_name.isidentifier():
            print(f"Name Error in '{code}': Invalid variable name!")
            return

        if value == "":
            print(f"Syntax Error in '{code}': No value given!")
            return

        if (
            "+" not in value
            and "*" not in value
            and (value.startswith(("'", '"')) or value.endswith(("'", '"')))
        ):
            if value.startswith(("'", '"')) != value.endswith(("'", '"')):
                print(f"Syntax Error in '{code}': Unclosed quotes!")
                return

            if (value.startswith('"') and value.endswith("'")) or (
                value.startswith("'") and value.endswith('"')
            ):
                print(f"Syntax Error in '{code}': Mismatched quotes!")
                return

            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                if len(value) >= 2:
                    variables[var_name] = value[1:-1]
                    return
                else:
                    print(f"Syntax Error in '{code}': Malformed quotes!")
                    return

        if value in variables:
            variables[var_name] = variables[value]
            return

        try:
            variables[var_name] = int(value)
            return

        except ValueError:
            pass

        try:
            variables[var_name] = float(value)
            return

        except ValueError:
            pass


        result = None

        if any(op in value for op in ["+", "-", "*", "/", "**", "%"]):

            if not re.match(r'^[0-9a-zA-Z_+\-*/%()\s\'."]+$', value):
                print(f"Security Error in '{code}': Invalid characters!")
                return

            result = eval(value, {"__builtins__": None}, variables)
        else:
            print(f"Syntax Error in '{code}': Failed to parse value expression.")
            return

        if isinstance(result, (int, float, str, bool)):
            variables[var_name] = result
            return

        print(f"Type Error in '{code}': Unsupported value type!")

    except Exception as e:
        print(f"Error in '{code}': {e}")

def ask_function(code):
    parts = code.split(maxsplit=1)

    if not parts or parts[0] != ask_command:
        return

    string = parts[1] if len(parts) > 1 else ""
    string = string.strip()

    if "->" in string:
        ask_parts = string.split("->", 1)
        prompt_content = ask_parts[0].strip()
        var_name = ask_parts[1].strip()

    else:
        prompt_content = string
        var_name = None

    if len(prompt_content) == 1 and prompt_content in ('"', "'"):
        print(f"Syntax Error: Unclosed quotes in '{code}'.")
        return

    starts_with_quote = prompt_content.startswith(('"', "'"))
    ends_with_quote = prompt_content.endswith(('"', "'"))

    if string.strip() == '"' or string.strip() == "'":
        print(f"Syntax Error: Unclosed quotes in '{code}'.")
        return
    
    if string.startswith('"') and string.endswith("'") or string.startswith("'") and string.endswith('"'):
        print(f"Syntax Error in '{code}': Cannot print a string with different quotes!")
        return

    if starts_with_quote != ends_with_quote:
        print(f"Syntax Error: Unclosed quotes in '{code}'")
        return

    display_prompt = prompt_content
    if starts_with_quote and ends_with_quote:
        display_prompt = prompt_content[1:-1]

    if not display_prompt and not var_name:
        print(f"Syntax Error: '{ask_command}' needs a prompt or a variable!")
        return

    if prompt_content in variables:
        user_response = input(variables[prompt_content])
    else:
        user_response = input(display_prompt)

    if var_name:
        if var_name.isidentifier():
            try:
                variables[var_name] = int(user_response)

            except ValueError:
                try:
                    variables[var_name] = float(user_response)

                except ValueError:
                    variables[var_name] = str(user_response)

        else:
            print(f"Name Error: '{var_name}' is not a valid variable name!")
    else:
        print(f"'{user_response}'")

def if_function(code, lines_source=None, current_index=None):
    condition_str = code[len(if_command):].strip()
    if condition_str.endswith(end_character):
        condition_str = condition_str[:-1].strip()

    try:
        is_true = eval(condition_str, {"__builtins__": None}, variables)

    except Exception as e:
        print(f"Error in '{condition_str}': {e}")
        return current_index + 1 if current_index is not None else None

    if_block = []
    nested_depth = 0

    if lines_source is not None and current_index is not None:
        pointer = current_index + 1

        while pointer < len(lines_source) and pointer != end_command:
            line = lines_source[pointer].strip()

            if line.startswith(if_command): nested_depth += 1
            if line == end_command:
                if nested_depth > 0: nested_depth -= 1
                else:
                    break

            if_block.append(line)
            pointer += 1
        next_line = pointer + 1

    else:
        while True:
            line = input("...     ").strip()

            if line.startswith(if_command): nested_depth += 1
            if line == end_command:
                if nested_depth > 0: nested_depth -= 1
                else:
                    break

            if_block.append(line)
        next_line = None

    if is_true:
        for block_line in if_block:
            execute_line(block_line)
            
    return next_line

def function(code):
    if not (code.startswith(function_command) and code.endswith(end_character)):
        return

    func_name = code[len(function_command):-1].strip()

    if not func_name:
        print(f"Name Error in '{code}': Cannot create a function without a name!")
        return

    if not func_name.isidentifier():
        print(f"Name Error in '{code}': Invalid function name!")
        return

    function_lines = []

    while True:
        line = input("...    ").strip()

        if line == end_command:
            break

        function_lines.append(line)

    functions[func_name] = function_lines

def forever_function(code):
    if code.strip() == f"{forever_command}{end_character}":
        loop_lines = []

        print("\n<-- Loop started: Type 'end' to run forever. -->\n")

        while True:
            line = input("...    ").strip()
            if line == end_command:
                break
            loop_lines.append(line)

        if not loop_lines:
            return

        print("\n<-- Running Loop: Press Ctrl + C to stop -->\n")

        try:
            while True:
                for line in loop_lines:
                    if not line:
                        continue

                    parts = line.split()
                    command = parts[0]
                    
                    if command == print_command:
                        print_function(line)

                    elif command == let_command:
                        let_function(line)

                    elif command == ask_command:
                        ask_function(line)

        except KeyboardInterrupt:
            print("\n<-- Loop Stopped -->\n")

def run_function(code):
    function_name = code[len(run_function_command):-1].strip()

    if function_name in functions:
        function_lines = functions[function_name]

        i = 0
        while i < len(function_lines):
            function_line = function_lines[i]

            if function_line == f"{forever_command}{end_character}":
                loop_lines = []
                i += 1

                while i < len(function_lines) and function_lines[i] != end_command:
                    loop_lines.append(function_lines[i])
                    i += 1
                        
                if loop_lines:
                    print(f"\n<-- Running Loop from '{function_name}': Press Ctrl + C to stop -->\n")
                    try:
                        while True:
                            for loop_line in loop_lines:
                                execute_line(loop_line)
                    except KeyboardInterrupt:
                        print("\n<-- Loop Stopped -->\n")

                i += 1

            elif function_line.startswith(if_command):
                i = if_function(function_line, function_lines, i)
                    
            else:
                execute_line(function_line)
                i += 1

def run_file(code):
    file_name = code[len(run_file_command):-1].strip()
    try:
        with open(f"{file_name}.pixo", "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            
            i = 0
            while i < len(lines):
                line = lines[i]

                if line == f"{forever_command}{end_character}":
                    loop_lines = []
                    i += 1

                    while i < len(lines) and lines[i] != end_command:
                        loop_lines.append(lines[i])
                        i += 1
                    
                    if loop_lines:
                        print(f"\n<-- Running Loop from '{file_name}': Press Ctrl + C to stop -->\n")
                        try:
                            while True:
                                for loop_line in loop_lines:
                                    execute_line(loop_line)
                        except KeyboardInterrupt:
                            print("\n<-- Loop Stopped -->\n")

                    i += 1

                elif line.startswith(if_command):
                    i = if_function(line, lines, i)
                
                else:
                    execute_line(line)
                    i += 1

    except FileNotFoundError:
        print(f"File or Function Error: '{file_name}' was not found!")

def help_function(code):
    if code == help_command:
        print("\n<-- Pixo Programming Language Help Menu -->\n")
        print(f" --> '{let_command} (name) = (value)' - Creates a variable (it also supports math expressions).")
        print(f" --> '{print_command} (message / variable)' - Prints a message or variable to the console.")
        print(f" --> '{ask_command} \"(message)\" {save_character} (variable)' - Gets the user input and saves it, if '{save_character}' is used.")
        print(f" --> '{if_command} x > 5' - Starts an '{if_command}' block. In this example, if x is larger than 5, it will execute code inside that block. If not, it will just continue.")
        print(f" --> '{function_command} (name){end_character}' - Creates a new function which is saved in memory and that can be executed later when needed.")
        print(f" --> '{forever_command}{end_character}' - Starts a loop. Press 'Ctrl + C' to stop the loop. If you want to run the loop, type 'end' and press 'Enter' on your keyboard.")
        print(f" --> '{run_function_command} (name of function){end_character}' - Runs a function.")
        print(f" --> '{run_file_command} (name of file){end_character}' - Runs a '.pixo' file.")
        print(f" --> '{comment_command} (text)' - Adds a comment which is ignored by Pixo Programming Language.")
        print(f" --> '{clear_command}' - Clears the screen.")
        print(f" --> '{exit_command}' - Closes Pixo Programming Language.\n")

def clear_function(code):
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{info}")
    print(f"{instruction}\n")

def exit_function(code):
    if code == exit_command:
        sys.exit()

def execute_line(code):
    code = code.strip()

    if not code or code.startswith(comment_command):
        return

    parts = code.split()
    command = parts[0]

    if command == print_command:
        print_function(code)

    elif command == let_command:
        let_function(code)

    elif command == ask_command:
        ask_function(code)

    elif code.startswith(if_command):
        if_function(code)

    elif code.startswith(function_command) and code.endswith(end_character):
        function(code)

    elif code.strip() == f"{forever_command}{end_character}":
        forever_function(code)

    elif code.startswith(run_function_command) and code.endswith(end_character):
        run_function(code)
    
    elif code.startswith(run_file_command) and code.endswith(end_character):
        run_file(code)

    elif code == help_command:
        help_function(code)

    elif code == clear_command:
        clear_function(code)

    elif code == exit_command:
        exit_function(code)

    else:
        print(f"Syntax Error: Unknown syntax '{code}'.")
        return

def main():
    while True:
        code = input("Pixo > ").strip()

        if not code:
            continue

        execute_line(code)

if __name__ == '__main__':
    main()
