#import gplaydl
import sys
import os
import re
from getpass import getpass
from Naked.toolshed.shell import execute_js, muterun_js
from gpapi.googleplay import GooglePlayAPI, RequestError
from datetime import datetime


# GooglePlay-Scraper Variables
collection_type = "TOP_FREE"
app_per_category = "1"
apk_initial_list = []
apk_download_list = []
category_apk_list = {} #####


# Google Server Variables
LOCALE = "us_US"
TIMEZONE = "America/Chicago"
server = GooglePlayAPI("us_US","America/Denver")

# Directory Variables
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
apk_dir = "./apks_" + timestamp

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
        #category_apk_list.setdefault(str(category_type), [])  #####
        #testlist = []

        # Grab non-empty apk_ids
        for app in download:
            if app != "":
                print(app)
                apk_initial_list.append(app)
                #testlist.append(app)
                #category_apk_list(str(category_type),[]).append(str(app))  #####
                
        #for app_in_category in testlist:
            #category_apk_list.setdefault(str(category_list), []).append(str(app_in_category))
        #return testlist

    else:
        sys.stderr.write(get_apps.stderr)
        #return

    #Test
    #for item in category_apk_list:	#####
        #print("Testing: " + category_apk_list)  #####


def generate_apk_list():

    # Executes the category_list.js file allowing Python to control
    # Standard Output and Standar Error entries
    get_categories = muterun_js("category_list.js")

    # If category_list.js file is successfull, get categories
    if get_categories.exitcode == 0:

        # Parse incoming data to only grab categories
        input_categories = get_categories.stdout
        categories = re.findall(r"'(.*?)'", str(input_categories))

        print("\nGenerating app_id list.  Please wait...\n")

      # Initialize category in list
        #category_apk_list.setdefault(str(category_type), [])  #####

        for title in categories:
            
            print("\n" + title.center(50, '-') + "\n")
            get_app_id(title)
            
            # Create Directories
            try:

                os.makedirs(apk_dir + "/" + title)
                print("Directory created for: " + title)

            except FileExistsError:

                # Directory Already Exists
                pass
                print("Directory already exists for: " + title)

        # Remove any dupliacte app_id entries and sort in ascending order
        apk_download_list = remove_duplicate_ids(apk_initial_list)
        #apk_download_list.sort()

        return apk_download_list

        # Print found apks
        #print("\nAPKs available for download:")
        #for apk in apk_download_list:
        #    print(apk)

    else:

        sys.stderr.write(get_categories.stderr)


def server_login():

    print("\nLogging in with GSFID and SubAuthToken (ac2dm).\n")
    gsfId, authSubToken = get_credentials() 
    server.login(None, None, int(gsfId), authSubToken)


def download_apks(download_apk):

    app_id = download_apk
    server.log(app_id)
    
    print("\nDownloading {}...".format(app_id))
   
    try:

        app = server.download(app_id)

        with open(app_id + ".apk", "wb") as apk_file:
            for app in app.get("file").get("data"):
                apk_file.write(app)
                #apk_file.write(apk_dir + "/" + app)
            print("Success")
    
<<<<<<< HEAD
    except Exception:        
        
        pass
        print("Failed")
=======
    try:
        
        app = server.download(app_id)
    
        with open(app_id + ".apk", "wb") as apk_file:
            for chunk in app.get("file").get("data"):
                apk_file.write(chunk)
            print("Success")
            
     except Exception:
        
        pass
>>>>>>> 1db2b4b508a926eccef49267bda927f304e3888e

def main():

    server_login()
    library = generate_apk_list()
	
    #print("Categories and Apps\n\n")
    #print(category_apk_list)

    # Download APKs
    print("\nDownloading APKs.  Please wait...\n")
    
    for apk in library:
        download_apks(apk)


main()
