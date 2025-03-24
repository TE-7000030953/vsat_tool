import pycurl
import re
from io import BytesIO
from bs4 import BeautifulSoup
#import os

# Set file name 
filename = "webpage_data_test.txt"

def get_file_path():
    start_keyword = "Diffstat"
    end_keyword = "diff"
    file_paths = []
    #path_pattern = re.compile(r'^[\w./-]+$')    
    #path_pattern = re.compile(r'^([a-zA-Z0-9_\/]+)\/([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)$')
    path_pattern = re.compile(r'^([a-zA-Z0-9_\/]+)\/([a-zA-Z0-9_-]+)\.([a-zA-Z0-9_]+)$')
    with open(filename, 'r') as file:
        lines = file.readlines()
    start_file_capture_flag = None
    test_start_index = None
    test_end_index = None
    for current_index, line in enumerate(lines):
        if start_keyword in line:
            test_start_index = current_index
            start_file_capture_flag = 1
        elif end_keyword in line:
            if(start_file_capture_flag):
                test_end_index = current_index
                break
        else:
            if(start_file_capture_flag):
                if path_pattern.match(line.strip()):
                    file_paths.append(line.strip())

    #print("start index : ", test_start_index)
    #print("end_index : ", test_end_index)
    #print("Captured file paths :")
    #for path in file_paths:
    #    print(path)
    #os.remove(filename)
    return file_paths

#get_file_path();

def download_webpage_text_curl(url):
    try:
        # Create a BytesIO object to hold the response
        buffer = BytesIO()
        
        # Initialize a pycurl object
        c = pycurl.Curl()
        
        # Set the URL
        c.setopt(c.URL, url)
        
        # Set the write function to the buffer
        c.setopt(c.WRITEDATA, buffer)
        
        # Set a user agent (optional but recommended)
        c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        
        # Perform the request
        c.perform()
        
        # Get the HTTP response code
        status_code = c.getinfo(c.RESPONSE_CODE)
        
        # Close the pycurl object
        c.close()
        
        # Check if the request was successful
        if status_code == 200:
            # Decode the buffer content to string
            webpage_content = buffer.getvalue().decode('utf-8')
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(webpage_content, 'html.parser')
            
            # Extract all the text from the webpage
            text = soup.get_text(separator='\n')
            
            # Write the readable text to a file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Webpage text successfully saved to {filename}")
        else:
            print(f"Failed to retrieve webpage. Status code: {status_code}")
    
    except pycurl.error as e:
        # Print any error that occurs during the request
        print(f"An error occurred: {e}")




# Example usage
#download_webpage_text_curl('https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bce1305c0ece3dc549663605e567655dd701752c')
#get_file_path()

#get_file_names_list('https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bce1305c0ece3dc549663605e567655dd701752c')
#get_file_names_list('https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=120434e5b305defa1fb1e7a38421ed08f93243d5')
