import re

def process_extracted_text(text):
    # Normalize text by replacing multiple newlines and trimming whitespace
    text = re.sub(r'\n+', '\n', text).strip()
    
    # Split text into lines
    lines = text.split('\n')
    
    # Create a structured recipe
    structured_recipe = {
        'lines': lines
    }

    return structured_recipe

def extract_ingredients_instructions(extracted_text):
    ingredients = extracted_text.get('ingredients', '').split('\n')
    instructions = extracted_text.get('instructions', '').split('\n')

    structured_recipe = {
        'ingredients': [line.strip() for line in ingredients if line.strip()],
        'instructions': [line.strip() for line in instructions if line.strip()],
    }

    return structured_recipe
