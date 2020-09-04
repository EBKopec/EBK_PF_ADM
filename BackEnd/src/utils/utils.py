import os
import shutil
from zipfile import ZipFile
import os
from os.path import basename


def monthId(month_id):
    if len(str(month_id)) == 5:
        monthId = str(month_id)[0:4] + '0' + str(month_id)[4:]
        # print(monthId)
        return monthId
    else:
        # print(month_id)
        return month_id

# Check dir
# If not exists - create it
# if exists - them use it


def checkDir(root, folder):

    path = root+'/'+folder
    CHECK_FOLDER = os.path.isdir(path)

    if not CHECK_FOLDER:
        os.makedirs(path)
        print('Folder Created for: %s' % path)

    return path


# Zip File
def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths

def zipFilesInDir(dirName, zipFileName, filter):
   # create a ZipFile object
   with ZipFile(zipFileName, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))