import os

# Define the results directory
RESULTS_DIR = "results"

# Ensure the directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)  # Create directory if it doesn't exist
    
def generate_validation_function(rule_text):
    """
    Generates a Python function for a validation rule.
    """
    function_name = f"validate_{rule_text.lower().replace(' ', '_')}"
    function_code = f"""
def {function_name}(df):
    \"\"\"Validates {rule_text}.\"\"\"
    # Implement validation logic here
    return df
"""
    return function_code.strip()

def extract_python_code(text):
    """
    Extracts only the Python function code from the RAG response.
    """
    start = text.find("```python")
    end = text.find("```", start + 7)

    if start != -1 and end != -1:
        return text[start + 7:end].strip()  # Extract only the code
    return text.strip()  # Return raw response if no markdown found

def process_rules_file(input_file, output_file=os.path.join(RESULTS_DIR, "rules_functions.py")):
    """
    Reads a text file of rules, generates validation functions, and saves them to a Python file.
    """
    try:
        # Read rules from the text file
        with open(input_file, "r", encoding="utf-8") as file:
            rules = file.readlines()

        # Ensure the output file is empty before writing
        with open(output_file, "w", encoding="utf-8") as py_file:
            py_file.write("# Auto-generated validation functions\n\nimport pandas as pd\n\n")  # Header

            for rule in rules:
                rule = rule.strip()
                if rule:  # Ignore empty lines
                    function_code = generate_validation_function(rule)
                    # function_code = extract_python_code(function_code)
                    py_file.write(function_code + "\n\n")  # Append function to file

        print(f"✅ Validation functions saved to {output_file}")

    except Exception as e:
        print(f"❌ Error processing rules file: {str(e)}")
