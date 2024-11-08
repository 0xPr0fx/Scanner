import re

# Define tokens for C code scanning
tokens = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),  # Single-line and multi-line comments
    ('KEYWORD', r'\b(?:int|float|char|if|else|while|for|return|void|struct|typedef|const)\b'),  # C keywords
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),  # Variable names, functions, etc.
    ('NUMBER', r'\b\d+(\.\d+)?\b'),  # Numbers (integer or decimal)
    ('OPERATOR', r'[+\-*/%=!<>&|]'),  # Operators
    ('PUNCTUATION', r'[;,\(\){}]'),  # Punctuation characters
    ('STRING', r'"([^"\\]|\\.)*"'),  # String literals
    ('WHITESPACE', r'\s+'),  # Spaces, tabs, and newlines (ignored)
]

# Compile regex patterns for each token type
combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
pattern_compiler = re.compile(combined_pattern)

def parse_code(c_code):
    parsed_tokens = []
    line_number = 1
    line_start_pos = 0

    # Iterate over each match found by the pattern compiler
    for match in pattern_compiler.finditer(c_code):
        token_type = match.lastgroup
        token_value = match.group()
        column_position = match.start() - line_start_pos

        # Ignore whitespace and comments but track newlines for line numbers
        if token_type == 'WHITESPACE':
            if '\n' in token_value:
                line_number += token_value.count('\n')
                line_start_pos = match.end()
            continue
        elif token_type == 'COMMENT':
            continue

        # Append token info as a tuple
        parsed_tokens.append((token_type, token_value, line_number, column_position))

    return parsed_tokens

def prompt_user():
    print("Welcome to the Enhanced C Code Scanner!")
    print("Select an input method:")
    print("1. Directly enter your C code")
    print("2. Load C code from a file")

    choice = input("Enter option (1 or 2): ")
    if choice == '1':
        print("\nType in your C code (type 'END' to stop):")
        code_lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            code_lines.append(line)
        user_code = "\n".join(code_lines)

    elif choice == '2':
        file_name = input("Enter the file path: ")
        try:
            with open(file_name, 'r') as file:
                user_code = file.read()
        except FileNotFoundError:
            print("Error: Could not find the specified file.")
            return None

    else:
        print("Invalid selection. Exiting.")
        return None

    return user_code

def display_tokens(parsed_tokens):
    print("\nTokens Identified:")
    for token in parsed_tokens:
        print(f"Type: {token[0]}, Value: '{token[1]}', Line: {token[2]}, Column: {token[3]}")

def main():
    c_code = prompt_user()
    if c_code:
        tokens_found = parse_code(c_code)
        display_tokens(tokens_found)

if __name__ == "__main__":
    main()
