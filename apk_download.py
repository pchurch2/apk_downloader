#import gplaydl
import sys
import os
import re
import subprocess
import jadx
from getpass import getpass
from Naked.toolshed.shell import execute_js, muterun_js
from gpapi.googleplay import GooglePlayAPI, RequestError
from datetime import datetime


# GooglePlay-Scraper Variables
collection_type = "TOP_FREE"
app_per_category = "1"
apk_initial_list = []
apk_download_list = []
category_apk_list = {}
category_dir_list = {}


# Google Server Variables
LOCALE = "us_US"
TIMEZONE = "America/Chicago"
server = GooglePlayAPI("us_US","America/Denver")

# Directory Variables
project_dir = os.getcwd()
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
apk_dir = "apks_" + timestamp


def get_credentials():

    gsfId = getpass("GSFID: ")
    authSubToken = getpass("AUTHSUBTOKEN: ")

    return gsfId, authSubToken

def remove_duplicate_ids(id_list):
    
    return list(dict.fromkeys(id_list))


def get_app_id(category_type):

    # Executes the app_list.js file allowing Python to control
    # Standard Output and Standard Error entires
    get_apps = muterun_js("app_list.js " + \
        category_type + " " + \
        collection_type + " " + \
        app_per_category)

    # If app_list.js call is successfull, get app_ids
    if get_apps.exitcode == 0:

        # Parse incoming data to only grab app_ids
        input_apps = get_apps.stdout
        category_list = re.findall(r"appId: '.*?'", str(input_apps))
        download = re.findall(r"'(.*?)'", str(category_list))

	    # Initialize category in list
        category_apk_list.setdefault(str(category_type), [])

        # Grab non-empty apk_ids
        for app in download:
            if app != "":
                print("Found: " + app)
                apk_initial_list.append(app)
                category_apk_list.setdefault(str(category_type),[]).append(str(app))
                
    else:
        sys.stderr.write(get_apps.stderr)
        #return

def generate_apk_list():

    # Executes the category_list.js file allowing Python to control
    # Standard Output and Standar Error entries
    get_categories = muterun_js("category_list.js")

    # If category_list.js file is successfull, get categories
    if get_categories.exitcode == 0:

        # Parse incoming data to only grab categories
        input_categories = get_categories.stdout
        categories = re.findall(r"'(.*?)'", str(input_categories))

        print("\nGenerating app_id list.  Please wait...")

        for title in categories:
            
            print("\n" + title.center(50, '-') + "\n")
            get_app_id(title)
            create_directory = str(project_dir + "/" + apk_dir + "/" + title)

            # Initialize category directory list
            category_dir_list.setdefault(str(title), [])

            # Create Directories
            try:

                os.makedirs(create_directory)
                os.chdir(create_directory)		# TODO - Implement path not cd
                category_dir_list.setdefault(str(title),[]).append(str(create_directory))
                print("Directory created for: " + title)
                os.chdir(project_dir)			# TODO - Implement path not cd
            
            except FileExistsError:

                # Directory Already Exists
                print("Directory already exists for: " + title)
                pass

        # Remove any duplicate app_id entries and sort in ascending order
        apk_download_list = remove_duplicate_ids(apk_initial_list)
        #apk_download_list.sort()

        return apk_download_list

    else:

        sys.stderr.write(get_categories.stderr)



def server_login():

    print("\nLogging in with GSFID and SubAuthToken (ac2dm).\n")
    gsfId, authSubToken = get_credentials() 
    server.login(None, None, int(gsfId), authSubToken)



def download_apks(get_apk, get_directory):

    #app_id = download_apk
    app_id = get_apk
    server.log(app_id)
    
    print("\nDownloading {}...".format(app_id))

    # Change to Category Directory
    os.chdir(project_dir + "/" + apk_dir + "/" + get_directory)
    
    try:

        app = server.download(app_id)

        with open(app_id + ".apk", "wb") as apk_file:
            for app in app.get("file").get("data"):
                
                apk_file.write(app)

            print("Success")
    
    except Exception:        
        
        pass
        print("Failed")

    # Change to Project Directory
    os.chdir(project_dir)



def jadx():

    start_dir = apk_dir
    #start_dir = "apks_20191210-233249"
    
    for dir_name, sub_dir_list, file_list in os.walk(start_dir):
        print('\nCurrent Directory: %s' % dir_name)
        
        for file_name in file_list:
            print('\nDecompiling %s...' % file_name)
            subprocess.call(["/home/preston/Downloads/jadx/build/jadx/bin/jadx", "-d", start_dir + "/00_decompiled_apks/" + file_name, "/home/preston/git/apk_downloader/" + dir_name + "/" + file_name])


def main():

    # Log into Google servers
    server_login()

    #library = generate_apk_list()  # Used to generate apk list
    
    # Retrieves APK list based on given categories
    generate_apk_list()	
    
    # Download found APK files
    print("\nDownloading APKs...")
    
    for category in category_apk_list:
        for apk in category_apk_list[category]:
            download_apks(str(apk), str(category))

    # Run JADX to decompile found APKs
    jadx()


main()
