import re

def capture_file_paths_until_diff(filename, keyword="diff"):
    file_paths = []
    
    # Adjusted regular expression to match relative file paths (e.g., lib/kunit/device.c)
    path_pattern = re.compile(r'^[\w./-]+$')  # Matches relative file paths

    with open(filename, 'r') as file:
        for line in file:
            # Stop the loop if the keyword (e.g., "diff") is found
            if keyword in line.lower():
                break
            
            # If the line matches the relative file path pattern, add it to the list
            if path_pattern.match(line.strip()):
                file_paths.append(line.strip())
    
    return file_paths

# Example usage
file_paths = capture_file_paths_until_diff('webpage_data_1.txt')
print("Captured file paths:")
for path in file_paths:
    print(path)

