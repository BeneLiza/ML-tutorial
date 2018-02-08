import pandas as pd


def tokens_for_Stanford_input(tml_token_file):
    """Function that takes a tml_token file (where sep=\|), extracts tokens and returns a text file for Stanford
    dependency parser """
    df_tokens = pd.read_csv(tml_token_file, sep='\|', header=None).dropna(axis=1)
    # Converts to dataframe
    df_tokens.columns = ["article_id", "sentence_id", "token_id", "token", "na1", "na2", "na3"]
    # Assigns headings
    df_tokens["token"] = df_tokens["token"].str.replace("'", "")
    # Removes apostrophes
    token_string = df_tokens['token'].to_string(index=False)
    # Converts token column into string
    removed_enters = token_string.replace('\n', ' ')
    final_tokens = ' '.join(removed_enters.split())
    # Makes sure that there is only one white space between tokens
    with open('stanford_input.txt', 'w', encoding='utf8') as outfile:
        outfile.write(final_tokens)

tokens_for_Stanford_input('tml_tokens.txt')
