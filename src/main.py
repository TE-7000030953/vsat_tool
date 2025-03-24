import handle_file_conversion_operations
import handle_patch_file_operations
import handle_config_check_operations
import json

csv_file_path = "data.csv"

# Get json string from csv file [ Done ]
        # Multiple patch link can be present convert it into array [ Pending ]

# Iterate it to get patch file link 
    # if no patch link found ie, patch not found, stop and note down details.
    # else continue further

# Download the contents of the patch link in readable format [ Done ]

# Extract file path list from the contents of patch link [ Pending : logic required ]

# For each file path; find its Makefile [ Pending : logic required ]

# In Makefile check if object file is generated, and capture config data [ Pending : logic required ]

# In CXD file check if config is set of not, note the respective details [ Pending : logic required ]
    # Config found : Config is set
    # Config found : Config is not set : Config invalid
    # Config not found : Config invalid

json_string = handle_file_conversion_operations.csv_to_json(csv_file_path)

json_data = json.loads(json_string)

file_paths_from_link = []

for item in json_data:
    #print(type(item))  # Check the type of each 'item'
    patch_file_link = item[" Patch link"]
    print(f"Patch link: {patch_file_link}")
    handle_patch_file_operations.download_webpage_text_curl(patch_file_link)
    file_paths_from_link = handle_patch_file_operations.get_file_path()
    #item[" Patch file"] = file_paths_from_link
    #item[" Patch link"] += "\n"
    print("Captured file paths :")
    for path in file_paths_from_link:
        #print(path)
        item[" Patch file"] += f"{path}\r\n"
    # Write logic to only call the function of check config if .c files are present in the file_paths_from_link

    handle_config_check_operations.check_and_set_config(file_paths_from_link, item, json_data)

print("json_data :::::::::::::::")
modified_json_data = json.dumps(json_data, indent=4)
print(modified_json_data)
handle_file_conversion_operations.json_to_csv("output_csv_file", json_data)
