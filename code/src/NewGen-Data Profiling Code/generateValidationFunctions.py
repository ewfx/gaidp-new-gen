import os

# Define the results directory
RESULTS_DIR = "results"

# Ensure the directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)  # Create directory if it doesn't exist
    
import re
import os

# Define the output directory and file
RESULTS_DIR = "results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "rules_functions.py")

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

import re
import os

# Define the output directory and file
RESULTS_DIR = "results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "rules_functions.py")

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

def clean_function_name(field_name):
    """
    Cleans up the field name to create a valid function name.
    - Removes unwanted characters.
    - Replaces spaces with underscores.
    - Fixes patterns like "1._FieldName" → "1_FieldName".
    """
    field_name = re.sub(r"[^\w\s]", "", field_name)  # Remove special characters
    field_name = re.sub(r"\s+", "_", field_name.strip())  # Replace spaces with underscores
    return field_name

def generate_validation_function(rule_text):
    """
    Parses a rule text and generates a validation function dynamically.
    """
    # Extract field name (before ":")
    field_match = re.match(r"^(\d+)?\.?\s*(.*?):\s*(.*)", rule_text)
    if field_match:
        rule_number, field_name, description = field_match.groups()
    else:
        return None  # Skip invalid rules

    # Format function name correctly
    if rule_number:
        function_name = f"validate_{rule_number}_{clean_function_name(field_name)}"
    else:
        function_name = f"validate_{clean_function_name(field_name)}"

    # Extract allowed values
    allowed_values_match = re.search(r"Allowed values:\s*(.*?)\.", rule_text, re.IGNORECASE)
    allowed_values = allowed_values_match.group(1).split(", ") if allowed_values_match else []

    # Generate the validation function
    function_code = f"""
# Function to validate {field_name}
def {function_name}(df):
    \"\"\"
    Validation Rule:
    - Field: {field_name}
    - Description: {description}
    - Allowed values: {', '.join(allowed_values) if allowed_values else "Not specified"}
    - Not allowed values: Any value outside the allowed values.
    \"\"\"
    not_allowed_values = df[~df["{field_name}"].isin({allowed_values if allowed_values else '[]'})]
    return not_allowed_values  # Returns rows with invalid values
"""

    return function_code.strip()

def process_rules_file(input_file):
    """
    Reads a text file of rules, generates validation functions, and saves them to a Python file.
    """
    try:
        # Read rules from the text file
        with open(input_file, "r", encoding="utf-8") as file:
            rules = file.readlines()

        # Ensure the output file is empty before writing
        with open(OUTPUT_FILE, "w", encoding="utf-8") as py_file:
            py_file.write("# Auto-generated validation functions\n\nimport pandas as pd\n\n")  # Header

            for rule in rules:
                rule = rule.strip()
                if rule:  # Ignore empty lines
                    function_code = generate_validation_function(rule)
                    if function_code:
                        py_file.write(function_code + "\n\n")  # Append function to file

        print(f"✅ Validation functions saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error processing rules file: {str(e)}")
import os
import re

# Define the output directory and file
RESULTS_DIR = "results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "rules_functions.py")

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Dictionary to store allowed values for each field
ALLOWED_VALUES = {}

def clean_function_name(field_name):
    """
    Cleans up the field name to create a valid function name.
    - Removes unwanted characters.
    - Replaces spaces with underscores.
    - Fixes patterns like "1._FieldName" → "1_FieldName".
    """
    field_name = re.sub(r"[^\w\s]", "", field_name)  # Remove special characters
    field_name = re.sub(r"\s+", "_", field_name.strip())  # Replace spaces with underscores
    return field_name

def extract_allowed_values(rule_text):
    """
    Extracts allowed values from a rule text and stores them in the ALLOWED_VALUES dictionary.
    """
    match = re.search(r"Allowed values(?: include)?[:]\s*(.*?)\.", rule_text, re.IGNORECASE)
    if match:
        values = set(match.group(1).split(", "))
        return values
    return set()  # Return empty set if no allowed values found

def generate_validation_function(rule_text):
    """
    Parses a rule text and generates a validation function dynamically.
    """
    # Extract field name and description
    field_match = re.match(r"^(\d+)?\.?\s*(.*?):\s*(.*)", rule_text)
    if not field_match:
        return None  # Skip invalid rules

    rule_number, field_name, description = field_match.groups()
    field_name_cleaned = clean_function_name(field_name)

    # Store allowed values
    allowed_values = extract_allowed_values(rule_text)
    if allowed_values:
        ALLOWED_VALUES[field_name_cleaned] = allowed_values

    # Format function name correctly
    function_name = f"validate_{rule_number}_{field_name_cleaned}" if rule_number else f"validate_{field_name_cleaned}"

    # Generate validation function
    function_code = f"""
# Function to validate {field_name}
def {function_name}(df):
    \"\"\"
    Validation Rule:
    - Field: {field_name}
    - Description: {description}
    - Allowed values: {', '.join(allowed_values) if allowed_values else "Not specified"}
    - Not allowed values: Any value outside the allowed values.
    \"\"\"
    allowed_values = {allowed_values if allowed_values else 'set()'}
    return df[~df["{field_name}"].isin(allowed_values)]
"""

    return function_code.strip()

def process_rules_file(input_file):
    """
    Reads a text file of rules, extracts allowed values, generates validation functions, and saves them to a Python file.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            rules = file.readlines()

        # Ensure the output file is empty before writing
        with open(OUTPUT_FILE, "w", encoding="utf-8") as py_file:
            py_file.write("# Auto-generated validation functions\n\nimport pandas as pd\n\n")  # Header

            # Extract allowed values and generate validation functions
            for rule in rules:
                rule = rule.strip()
                if rule:
                    function_code = generate_validation_function(rule)
                    if function_code:
                        py_file.write(function_code + "\n\n")  # Append function to file

            # Write allowed values dictionary
            py_file.write("# Allowed values as per rules\n")
            for key, values in ALLOWED_VALUES.items():
                py_file.write(f"ALLOWED_{key.upper()} = {values}\n")

        print(f"✅ Validation functions saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error processing rules file: {str(e)}")
