# import os
# import pandas as panda


# data_directory = "data/west-midlands-sept-12-month-data"


# monthly_crime_data = []

# for month_folder in os.listdir(data_directory):
#     month_folder_path = os.path.join(data_directory, month_folder)

#     if os.path.isdir(month_folder_path):
#         print(f"Checking folder: {month_folder_path}")

#       
#         files = {
#             "crime": f"{month_folder}-west-midlands-street.csv",
#             "outcomes": f"{month_folder}-west-midlands-outcomes.csv",
#             "stop_and_search": f"{month_folder}-west-midlands-stop-and-search.csv",
#         }

#         for file_type, file_name in files.items():
#             file_path = os.path.join(month_folder_path, file_name)
#             try:
#                 if file_type == "crime":
#                     crime_data_df = panda.read_csv(file_path)
#                     monthly_crime_data.append(crime_data_df)
#                     print(f"Loaded crime data from {file_name}")
#                 elif file_type == "outcomes":
#                     panda.read_csv(file_path)
#                     print(f"Loaded outcomes data from {file_name}")
#                 elif file_type == "stop_and_search":
#                     panda.read_csv(file_path)
#                     print(f"Loaded stop and search data from {file_name}")
#             except FileNotFoundError:
#                 print(f"File not found: {file_path}")


# if monthly_crime_data:
#     combined_crime_data_df = panda.concat(
#         monthly_crime_data, ignore_index=True
#     )
#     print(f"Combined Crime DataFrame shape: {combined_crime_data_df.shape}")
# else:
#     print("No crime data loaded.")