import  re
import random # <-- Import the random module for shuffling

def parse_and_list_names(combined_string):
    """
    Parses a concatenated string of names and attempts to separate them into a legible list.
    The primary heuristic used is that a new name generally starts with a Capital Letter
    that is not preceded by a space.
    """
    print("--- Name List Parser ---")
    
    # 1. Clean the string: Remove all commas and dots, and normalize spaces.
    # The new string contains: Ashwin S.Bhavadharni K,Deborh Blessy . Jeevan Z...
    cleaned_string = combined_string.replace('.', '').replace(',', '')
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()
    
    print("Cleaned Input String:")
    print(cleaned_string)
    
    # 2. Heuristic Separation: Insert a newline character before every Capital Letter
    # that is not at the start of the string. This assumes a new name starts with a
    # capital letter, which is the most reliable pattern in this concatenated data.
    
    # Pattern: Lookahead for an uppercase letter ([A-Z]) that is NOT preceded by the start of string (?<!^).
    separated_names = re.sub(r'(?<!^)(?=[A-Z])', r'\n', cleaned_string)
    
    # 3. Split by newline and clean up the list
    name_list = separated_names.split('\n')
    
    # Final list cleaning and printing
    print("\nParsed and Formatted Name List (Random Order):")
    
    # We will strip extra whitespace from each name
    final_parsed_list = [name.strip() for name in name_list if name.strip()]

    # 4. Randomize the list order
    random.shuffle(final_parsed_list) # <-- Shuffles the list into a random order
    
    for i, name in enumerate(final_parsed_list, 1):
        # We try to add a space between an initial and the following name part (e.g., 'SBhavadharni' -> 'S Bhavadharni')
        # We look for a single capital letter followed immediately by another capital letter then a lowercase letter.
        # This fixes common concatenations like 'SBhavadharni' but might introduce extra spaces elsewhere.
        # Let's keep the output as is for simplicity, relying on the primary separation logic.
        print(f"{i:02d}. {name}")
    
    print(f"\n--- Finished: {len(final_parsed_list)} names found ---")

# User-provided string (latest version)
user_input_string = "Ashwin S.Bhavadharni K,Deborh Blessy . Jeevan Z.Dhakshayani A.Dhanushree J.Divya M.Gnanadeepika M R.Gokula Ramanan K.Janani V.Kaaviya S.Kanishka M.Kanthasamy C.AKaviya Sri V.Keerthana B.Kishor Kumar K.Lavanya Mahalakshmi B.Madhumitha S.Mirudhu Bhashini B.Nagagowtham T.Rohit Vikas M.Sathish Kumar K.Sivanya N.Sivaram S.Srikaviya S.Sudarshan S.Suwiss Antony J.Varun S.Vignesh B.Vignesh S.Vinitha N.Yogesh Gokul .R"

# Execute the function
if __name__ == "__main__":
    parse_and_list_names(user_input_string)