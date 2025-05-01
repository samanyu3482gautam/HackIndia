
def fill_missing_with_mean(csv_filepath):
    """
    Reads a CSV file, identifies columns with missing values (empty strings or NaN),
    calculates the mean of each such column (ignoring missing values), and
    fills the missing values with the respective column's mean.

    Args:
        csv_filepath (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The modified DataFrame with missing values filled with the mean.
                          Returns None if the file is not found or an error occurs.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_filepath)

        # Identify columns with missing values (empty strings or NaN)
        cols_with_missing = [col for col in df.columns if df[col].isnull().any() or (df[col] == '').any()]

        if not cols_with_missing:
            print("No missing values found in the specified columns.")
            return df

        for col in cols_with_missing:
            # Check if the column is numeric (int or float)
            if pd.api.types.is_numeric_dtype(df[col]):
                # Calculate the mean of the non-missing values
                mean_value = df[col].mean()
                print(f"Filling missing values in column '{col}' with mean: {mean_value:.2f}")
                # Fill NaN values with the mean
                df[col].fillna(mean_value, inplace=True)
                # Fill empty string values with the mean (after converting to NaN for calculation)
                df[col].replace('', mean_value, inplace=True)
            else:
                print(f"Column '{col}' is not numeric. Skipping mean imputation.")

        return df

    except FileNotFoundError:
        print(f"Error: File not found at '{csv_filepath}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    file_path = input("Please enter the path to your CSV file: ")
    modified_df = fill_missing_with_mean(file_path)

    if modified_df is not None:
        # You can now save the modified DataFrame to a new CSV file or work with it directly
        output_filepath = input("Please enter the path to save the modified CSV file (or press Enter to just display it): ")
        if output_filepath:
            try:
                modified_df.to_csv(output_filepath, index=False)
                print(f"Modified CSV file saved to '{output_filepath}'")
            except Exception as e:
                print(f"Error saving the modified CSV: {e}")
        else:
            print("\nModified DataFrame:")
            print(modified_df)