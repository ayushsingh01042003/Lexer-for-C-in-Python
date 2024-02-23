import re
import random

class CLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = self.tokenize()

    def tokenize(self):
        # Define regular expressions for common C tokens
        patterns = [
            (r'\bint\b', 'INT'),
            (r'\bfloat\b', 'FLOAT'),
            (r'\bchar\b', 'CHAR'),
            (r'\bif\b', 'IF'),
            (r'\belse\b', 'ELSE'),
            (r'\bwhile\b', 'WHILE'),
            (r'\bfor\b', 'FOR'),
            (r'\breturn\b', 'RETURN'),
            (r'\bprintf\b', 'PRINTF'),
            (r'\bscanf\b', 'SCANF'),
            (r'\bvoid\b', 'VOID'),
            (r'\bmain\b', 'MAIN'),
            (r'\binclude\b', 'INCLUDE'),
            (r'\bdefine\b', 'DEFINE'),
            (r'\bstruct\b', 'STRUCT'),
            (r'\btypedef\b', 'TYPEDEF'),
            (r'\bconst\b', 'CONST'),
            (r'\bvolatile\b', 'VOLATILE'),
            (r'\bstatic\b', 'STATIC'),
            (r'\bextern\b', 'EXTERN'),
            (r'\bauto\b', 'AUTO'),
            (r'\bregister\b', 'REGISTER'),
            (r'\bsizeof\b', 'SIZEOF'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Variable or function names
            (r'\d+', 'NUMBER'),  # Integer literals
            (r'\d+\.\d+', 'FLOAT_NUMBER'),  # Floating-point literals
            (r'"([^"]*)"', 'STRING_LITERAL'),  # String literals
            (r'\'([^\'\\]|\\.){1}\'', 'CHAR_LITERAL'),  # Character literals
            (r'[-+*/%=<>!&|;,\(\)\{\}\[\]\.\?:]', 'OPERATOR'),  # Operators and punctuation
        ]

        combined_patterns = '|'.join('(?P<%s>%s)' % (name, pattern) for pattern, name in patterns)
        token_pattern = re.compile(combined_patterns)

        variable_addresses = {}  # Dictionary to store variable names and addresses
        tokens = []

        for match in token_pattern.finditer(self.code):
            token_type = match.lastgroup
            token_value = match.group()

            if token_type == 'IDENTIFIER':
                if token_value in variable_addresses:
                    # Reuse the existing address for the variable
                    address = variable_addresses[token_value]
                else:
                    # Generate a random 4-digit number as the address for new variables
                    address = random.randint(1000, 9999)
                    # Store the variable name and address in the dictionary
                    variable_addresses[token_value] = address

                tokens.append((token_type, token_value, address))
            else:
                tokens.append((token_type, token_value))

        return tokens

    def get_tokens(self):
        return self.tokens

# Read input from an external text file
file_path = 'code.txt'  # Replace with your file path
with open(file_path, 'r') as file:
    code_from_file = file.read()

# Create lexer and get tokens
lexer = CLexer(code_from_file)
tokens = lexer.get_tokens()

# Print tokens to the terminal
for token in tokens:
    if len(token) == 3:  # Check if the token has an address (for IDENTIFIER)
        print(f'{token[0]}: {token[1]} (Address: {token[2]})')
    else:
        print(f'{token[0]}: {token[1]}')
