class GrammarParser:
    COLORS = {
        'HEADER': "\033[95m",
        'OKBLUE': "\033[94m",
        'OKGREEN': "\033[92m",
        'WARNING': "\033[93m",
        'FAIL': "\033[91m",
        'ENDC': "\033[0m",
    }

    def __init__(self):
        self.rules = {}
        self.input_string = ""
        self.current_pos = 0
        self.parse_tree = []

    def display_in_color(self, message, color):
        print(f"{self.COLORS[color]}{message}{self.COLORS['ENDC']}")

    def get_grammar_input(self):
        """Prompt user for grammar input."""
        self.rules.clear()
        self.display_in_color("\nEnter Grammar Rules", 'HEADER')
        non_terminals = ['S', 'B']
        
        for nt in non_terminals:
            self.rules[nt] = []
            for i in range(1, 3):
                rule = input(f"Enter rule {i} for non-terminal '{nt}' (use capital letters for non-terminals): ").strip()
                self.rules[nt].append(rule)

    def is_grammar_simple(self):
        """Check if grammar has any invalid features."""
        for nt, rules in self.rules.items():
            for rule in rules:
                if rule.startswith(nt):
                    self.display_in_color(f"Grammar isn't simple: Left recursion in '{nt}'", 'WARNING')
                    return False
                if rule == "":
                    self.display_in_color(f"Grammar isn't simple: Epsilon rule found in '{nt}'", 'WARNING')
                    return False
                
            starting_symbols = [rule[0] for rule in rules if rule]
            if len(starting_symbols) != len(set(starting_symbols)):
                self.display_in_color(f"Grammar isn't simple: Duplicate starting symbols in '{nt}'", 'WARNING')
                return False

        self.display_in_color("Grammar is simple.", 'OKGREEN')
        return True

    def parse_input(self, input_str):
        """Parse the input string using the grammar rules."""
        self.input_string = list(input_str)
        self.current_pos = 0
        self.parse_tree = []
        self.display_in_color(f"Input String: {self.input_string}", 'OKBLUE')

        if self.match_non_terminal('S', self.parse_tree) and self.current_pos == len(self.input_string):
            self.display_in_color("Input string is accepted.", 'OKGREEN')
            self.display_parse_tree(self.parse_tree, "")
        else:
            self.display_in_color("Input string is rejected.", 'FAIL')

    def match_non_terminal(self, non_terminal, tree_node):
        """Attempt to match a non-terminal to input using the rules."""
        if non_terminal not in self.rules:
            return False

        for rule in self.rules[non_terminal]:
            saved_pos = self.current_pos
            sub_tree = []

            if self.apply_rule(rule, sub_tree):
                tree_node.append((non_terminal, rule, sub_tree))
                return True
            else:
                self.current_pos = saved_pos

        return False

    def apply_rule(self, rule, sub_tree):
        """Apply a grammar rule to the input."""
        for symbol in rule:
            if symbol.isupper():  # Non-terminal
                if not self.match_non_terminal(symbol, sub_tree):
                    return False
            else:  # Terminal
                if self.current_pos < len(self.input_string) and self.input_string[self.current_pos] == symbol:
                    sub_tree.append(symbol)
                    self.current_pos += 1
                else:
                    return False
        return True

    def display_parse_tree(self, tree, indent):
        """Display the parse tree."""
        for node in tree:
            if isinstance(node, tuple):  # Non-terminal
                print(f"{indent}{node[0]} -> {node[1]}")
                self.display_parse_tree(node[2], indent + "    |")
            else:  # Terminal
                print(f"{indent}    |-- {node}")

    def menu(self):
        """Main menu loop."""
        while True:
            self.get_grammar_input()
            if not self.is_grammar_simple():
                continue

            while True:
                input_str = input("Enter string to check: ").strip()
                self.parse_input(input_str)

                self.display_in_color("\n========================", 'HEADER')
                print("1- Check another string")
                print("2- Enter new grammar")
                print("3- Exit")
                choice = input("Your choice: ").strip()

                if choice == '1':
                    continue
                elif choice == '2':
                    break
                elif choice == '3':
                    self.display_in_color("Exiting...", 'OKGREEN')
                    return
                else:
                    self.display_in_color("Invalid choice. Please try again.", 'WARNING')


if __name__ == "__main__":
    parser = GrammarParser()
    parser.menu()
