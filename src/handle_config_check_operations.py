import handle_patch_file_operations
import os
import re


# first check if the path is ending with .c or not if yes then proceed
# strip the last part of the file path remove it and store it in a variable and attach it with the source code file path in begining and Makefile in ending
# check if the file exists
    # if Makefile exists :
        # Open the makefile and check if the saved name in variable is present in file or not.
            # if present then 

source_code_path = "Kernel_171H-TAG_REL_SNG_KERNEL_COMMON_220620_01/"

cxd_file_path = "Kernel_171H-TAG_REL_SNG_KERNEL_COMMON_220620_01/cxd_file/abcd.cxd"


makefile_contents = ""
cxdfile_contents = ""
config_result = ""

# this is a test code 
def test_code():
    file_paths_from_link = handle_patch_file_operations.get_file_path()
    print("______________________________")
    print("Captured file paths :")
    for path in file_paths_from_link:
        print(path) 
    print("____________________________________")
    check_and_set_config(file_paths_from_link)

def check_and_set_config(file_paths, item, json_data):
#def check_and_set_config(file_paths):

    global makefile_contents
    global cxdfile_contents
    global config_result

    config_detect_pattern1 = r'^obj-y$'
    config_detect_pattern2 = r'^[a-zA-Z0-9_-]+-y$'
    config_detect_pattern3 = r'^obj-\$\([A-Z_]+\)$'
    # strores makefile contents before uploading to json data
    makefile_contents = ".Makefile\r\n"
    #cxdfile_contents = ".CXD File\r\n"

    for path in file_paths:
        if(path.strip().endswith(".c")):
            print("____________________________________")
            print("Checking file path : " + path)
            head_tail = os.path.split(path)
            
            file_search = head_tail[1]
            #print(path)

            while (head_tail[1]!=""):
                # logic to find stuff
                # add /file/../head_tail[1]/Makefile to find
                #print(head_tail[0])
                
                if(head_tail[0]!=""):
                    file_path_head = head_tail[0] + "/"
                else:
                    file_path_head = ""
                
                makefile_path = source_code_path + file_path_head + "Makefile"
                
                #print(makefile_path)
                if(os.path.isfile(makefile_path)):
                    print("Makefile file exists for the file path : " + makefile_path)
                    #write code to check send (makefile_path, file_search) as parametersi
                    makefile_data = check_if_object_file_exists(makefile_path, file_search.rstrip(".c") + ".o")
                    # if config is obj-y then directly write the config result
                    # if config is xyz-y then search for xyz.o in check_if_config_exists and get config and search cxd file for the config
                    # if config is obj-$(CONFIG_XYZ) then send to search_cxd file for the config

                    if makefile_data is not None:
                    
                        # Check if the variable matches pattern 1 (exact 'obj-y')
                        if re.match(config_detect_pattern1, makefile_data):
                            print(f"'{makefile_data}' matches Pattern 1: obj-y")
                            #return 'Pattern 1: obj-y'
                            #makefile_contents += 

                        # Check if the variable matches pattern 2 (any string ending in '-y')
                        elif re.match(config_detect_pattern2, makefile_data):
                            print(f"'{makefile_data}' matches Pattern 2: <any-string>-y")
                            #return 'Pattern 2: <any-string>-y'
                            makefile_data = check_if_object_file_exists(makefile_path, makefile_data.rstrip("-y") + ".o")
                            config_data = get_config_name_from_makefile_data(makefile_data)
                            check_if_config_exists(config_data)

                        # Check if the variable matches pattern 3 (e.g., 'obj-$(CONFIG_XYZ)')
                        elif re.match(config_detect_pattern3, makefile_data):
                            print(f"'{makefile_data}' matches Pattern 3: obj-$(XYZ)")
                            config_data = get_config_name_from_makefile_data(makefile_data)
                            check_if_config_exists(config_data)

                        else:
                            # If no pattern matches
                            print(f"'{makefile_data}' does not match any pattern.")
                            #return 'No pattern match'
                    
                    else:

                        print("Object file not found in Makefile")
                        makefile_contents += "Makefile not found\n"
                        config_result = "CONFIG invalid\n"

                    break
                head_tail = os.path.split(head_tail[0])

    makefile_contents = remove_duplicates(makefile_contents)
    cxdfile_contents = remove_duplicates(cxdfile_contents)
    config_result = remove_duplicates(config_result)

    item[" Makefile data"] = f"{makefile_contents}\n{cxdfile_contents}"
    item[" Config details"] = f"{config_result}"

    print(f"Makefile contents are ::: {makefile_contents}")
    print(f"Cxdfile contents are ::: {cxdfile_contents}")
    print(f"Config result is ::: {config_result}")
            # usecase : write that no makefile exists in that specific item of json_data
           

def get_config_name_from_makefile_data(makefile_data):
    print("Inside get config name from makefile data")
    config_match_pattern = r'\$\((.*?)\)'
    match = re.search(config_match_pattern, makefile_data)
    if match:
        # Return the captured content inside $() (e.g., CONFIG_WIFI)
        return match.group(1)
    else:
        return None  # Return None if no match is found
 


def check_if_object_file_exists(makefile_path, file_search):
    global makefile_contents
    captured_part = None
    search_pattern_1 = ':=' 
    search_pattern_2 = '+='
    #print("*****************************")
    #print(makefile_path)
    #print(file_search)
    #print("*****************************")
    with open(makefile_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if file_search in line:
            #print(f"'{file_search}' found in line {i+1}: {line.strip()}")

            for j in range(i, -1, -1):
                if search_pattern_1 in lines[j]:
                    #print(f"'{search_pattern_1}' found in line {j+1}: {lines[j].strip()}")
                    captured_part = lines[j].split(search_pattern_1)[0].strip()
                    print(f"Captured part in Makefile : {captured_part}")
                    makefile_contents += f"{captured_part} := {file_search}\n"
                    break;
                
                elif search_pattern_2 in lines[j]:
                    #print(f"'{search_pattern_2}' found in line {j+1}: {lines[j].strip()}")
                    captured_part = lines[j].split(search_pattern_2)[0].strip()
                    print(f"Captured part in Makefile : {captured_part}")
                    makefile_contents += f"{captured_part} = {file_search}\n"
                    break;
            # /// usecase : no specified search patterns found in line

    return captured_part

def check_if_config_exists(config_name):
    global cxdfile_contents
    global config_result
    cxdfile_contents = ".CXD File\r\n"
    print("Final config data for the provided file path :")
    print(config_name)
    config_line = None

    with open(cxd_file_path, 'r') as file:
        for line in file:
            if config_name in line:
                config_line = line.strip()  # Store the line and remove extra spaces
                break  # Stop after finding the line
    
    # deal with config line here
    if(config_line is not None):
        #print(config_line)
        if(f"{config_name}=y" == config_line):
            print("it is config = y")
            cxdfile_contents += f"{config_name}=y\n"
            config_result += "CONFIG is set\n"

        elif(f"{config_name}=m" == config_line):
            print("it is config = m")
            cxdfile_contents += f"{config_name}=m\n"
            config_result += "CONFIG is set\n"

        elif(f"{config_name} is not set" == config_line):
            print("it is config is not set")
            cxdfile_contents += f"{config_name} is not set\n"
            config_result += "CONFIG invalid\n"

        # here write logic for differentiating between CONFIG_XYZ=y, CONFIG_XYZ=m, Config is not set.
        # here write logic for recording in json data about the result in previous line.
    else:
        # here write logic for recording in json data about config is not set
        print("Config data is not existing")


def remove_duplicates(input_string):

    print("##############################################")
    print("input string is :")
    print(input_string)


    lines = input_string.strip().split("\n")
    
    # Use a list to preserve order and a set to track seen lines
    unique_lines = []
    seen = set()
    
    # Iterate over each line
    for line in lines:
        if line not in seen:
            unique_lines.append(line)  # Add to the list if it's not a duplicate
            seen.add(line)  # Mark the line as seen
    
    # Join the unique lines back into a string
    result = "\n".join(unique_lines)
    
    print("result is :")
    print(result)
    print("#############################################")
 
    return result



#test_code()
