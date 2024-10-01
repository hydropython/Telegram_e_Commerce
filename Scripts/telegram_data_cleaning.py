
import pandas as pd
import re

class TelegramDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.df_clean = None
        self.output_cleaned_path = 'cleaned_telegram_data.csv'
        self.labeled_data_path = 'labeled_telegram_product_price_location.txt-'
    
    def drop_empty_rows(self):
        """Drops rows where all values are NaN and saves the cleaned dataframe."""
        self.df_clean = self.df.dropna(how='all')
        # Save cleaned data
        self.df_clean.to_csv(self.output_cleaned_path, index=False)
        # Print row count after dropping
        print(f"Number of rows after dropping empty rows: {self.df_clean.shape[0]}")
    
    def check_nan_in_column(self, column_name):
        """Checks and removes NaN values in the specified column."""
        nan_count = self.df[column_name].isnull().sum()
        print(f"Number of NaN values in '{column_name}' column: {nan_count}")
        # Drop NaN values from the specified column
        self.df_clean = self.df.dropna(subset=[column_name])
        print(f"Dataset shape after dropping NaN values in '{column_name}' column: {self.df_clean.shape}")

    @staticmethod
    def remove_emojis(text):
        """Removes emojis from a given text."""
        emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+", 
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)
    
    def apply_remove_emojis(self):
        """Applies emoji removal to the 'Message' column."""
        if self.df_clean is not None:
            self.df_clean['Message'] = self.df_clean['Message'].apply(self.remove_emojis)
        else:
            print("Please clean the dataset first by dropping NaN values.")
    
    @staticmethod
    def remove_english_from_amharic(text):
        """Removes English characters and common symbols from Amharic text."""
        if isinstance(text, str):
            amharic_only_text = re.sub(r'[A-Za-z0-9.,!?:;\'\"()\[\]{}\-_/]', '', text)
            return amharic_only_text
        return text

    def apply_remove_english(self):
        """Applies the removal of English characters from the 'Message' column."""
        if self.df_clean is not None:
            self.df_clean['Cleaned_Message'] = self.df_clean['Message'].apply(self.remove_english_from_amharic)
        else:
            print("Please clean the dataset first by dropping NaN values.")
    
    def save_cleaned_data(self, output_path):
        """Saves the cleaned DataFrame to a CSV file."""
        if self.df_clean is not None:
            self.df_clean.to_csv(output_path, index=False)
            print(f"Cleaned text saved to {output_path}.")
        else:
            print("No cleaned data to save.")

    def save_labeled_data(self):
        """Saves labeled data in a text file."""
        if self.df_clean is not None:
            with open(self.labeled_data_path, 'w', encoding='utf-8') as f:
                for index, row in self.df_clean.iterrows():
                    f.write(f"{row['Labeled_Message']}\n\n")
        else:
            print("No labeled data to save.")