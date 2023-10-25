import requests
import os 
import re
import json
from datetime import datetime

def copy_text_log(source, target):
    dest_file = open(target, 'wb')
    dest_file.write(source)
    dest_file.close()

# Function to copy JSON log files
def copy_json_log(source, target):
    src_file = open(target, 'w')
    data = json.load(src_file)
    json.dump(data, source, indent=2)

def copyErrorMessages(source, target):
    output_file = open(target, 'w') 
    # Iterate over all files in the directory
    for file in os.listdir(source):
        if file.endswith('.txt'):  # Assuming your log files have a .txt extension
            file_path = os.path.join(source, file)

        log_file = open(file_path,'r')

        print(f"In file: {file}")

        for line in log_file:
            outRes = file.split('_')[0] + ": " + line
            # Check if the line contains any of the error patterns
            if any(re.search(pattern, line) for pattern in error_patterns):
                # Process or print the line with the error message
                output_file.write(outRes)
    log_file.close()    
    output_file.close()



####### MAIN CODE
gitLogsObj = {"Apache": "https://raw.githubusercontent.com/logpai/loghub/master/Apache/Apache_2k.log"
              ,"Spark": "https://raw.githubusercontent.com/logpai/loghub/master/Spark/Spark_2k.log"
              ,"Hadoop": "https://raw.githubusercontent.com/logpai/loghub/master/Hadoop/Hadoop_2k.log"
             }


current_datetime = datetime.now()

formTime = current_datetime.strftime("%Y%m%d%H%M%S")

today_date = current_datetime.strftime("%Y%m%d")


directory = os.getcwd() 
# Define the folder path where you want to create the folder
folder_path = f"{directory}\\log_files\\logs_{today_date}"

error_patterns = [r'ERROR:', r'\[error\]', r'ERROR']

supported_extensions = ('.log', '.txt', '.json')


# Check if the folder already exists
if not os.path.exists(folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path)
    print(f"Folder for today's date '{today_date}' created at: {folder_path}")
else:
    print(f"Folder for today's date '{today_date}' already exists at: {folder_path}")


counter = 1

for key in gitLogsObj:

    print("{}. {} step!".format(counter, key))

    filename = folder_path + f'\\{key}_logs_{today_date}.txt'
    
    if gitLogsObj[key].endswith(supported_extensions):
        req = requests.get(gitLogsObj[key])
        
        res = req._content

        # Determine the file format and copy accordingly
        if gitLogsObj[key].endswith(('.log', '.txt')):
            copy_text_log(res, filename)
        elif gitLogsObj[key].endswith('.json'):
            copy_json_log(res, filename)
    counter += 1


ErrorTargetFile = f'{directory}\\log_files\\error_logs_{today_date}.txt' 

copyErrorMessages(folder_path, ErrorTargetFile)

print("Loop finished!")
