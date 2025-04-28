import os
import pandas as panda

# Path to the directory with subfolders for each month's data.
data_directory = "data/west-midlands-sept-12-month-data"

# List to store the cleaned crime data from each month.
monthly_crime_data = []

# Loop through each folder (representing a month) in the directory.
for month_folder in os.listdir(data_directory):
    month_folder_path = os.path.join(data_directory, month_folder)

    if os.path.isdir(month_folder_path):
        print(f"Checking folder: {month_folder_path}")

        
        files = {
            "crime": f"{month_folder}-west-midlands-street.csv",
            "outcomes": f"{month_folder}-west-midlands-outcomes.csv",
            "stop_and_search": f"{month_folder}-west-midlands-stop-and-search.csv",
        }

        for file_type, file_name in files.items():
            file_path = os.path.join(month_folder_path, file_name)

            try:
                if file_type == "crime":
                    crime_data_df = panda.read_csv(file_path)
                    #Remove unnecessary columns.
                    crime_data_df = crime_data_df.drop(
                        columns=["Reported by", "Location"]
                    )
                    monthly_crime_data.append(crime_data_df)
                    print(f"Loaded and cleaned crime data: {file_path}")

                elif file_type == "outcomes":
                    panda.read_csv(
                        file_path
                    )  
                    print(f"Loaded outcomes data: {file_path}")

                elif file_type == "stop_and_search":
                    panda.read_csv(
                        file_path
                    )  
                    print(f"Loaded stop and search data: {file_path}")

            except FileNotFoundError:
                print(f"File not found: {file_path}")


if monthly_crime_data:
    combined_crime_data_df = panda.concat(monthly_crime_data, ignore_index=True)
    print(f"Combined Crime DataFrame shape: {combined_crime_data_df.shape}")

    #Save the combined data for future analysis - can do other regions in future.
    combined_crime_data_df.to_csv("data/cleaned_crime_data.csv", index=False)
    print("Cleaned crime data saved as 'cleaned_crime_data.csv'")
else:
    print("No crime data loaded.")