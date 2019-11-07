#import gplaydl
import sys
import os
import re
from Naked.toolshed.shell import execute_js, muterun_js
from gpapi.googleplay import GooglePlayAPI, RequestError


# GooglePlay-Scraper Variables
collection_type = "TOP_FREE"
app_per_category = "3"
apk_initial_list = []
apk_download_list = []


# Login Variables
#gsfId = 
#authSubToken = 


# Google Server Variables
LOCALE = "us_US"
TIMEZONE = "America/Chicago"
server = GooglePlayAPI("us_US","America/Denver")


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

        # Grab non-empty apk_ids
        for app in download:
            if app != "":
                print(app)
                apk_initial_list.append(app)

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

        print("\nGenerating app_id list.  Please wait...\n")

        for title in categories:
            print("\n" + title.center(50, '-') + "\n")
            get_app_id(title)

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

    print("\nLogging in with ac2dm token and gsfId.\n")
    server.login(None, None, gsfId, authSubToken)


def download_apks(download_apk):

    app_id = download_apk
    server.log(app_id)
    
    print("\nDownloading {}...".format(app_id))
    
    app = server.download(app_id)
    
    with open(app_id + ".apk", "wb") as apk_file:
        for chunk in app.get("file").get("data"):
            apk_file.write(chunk)
        print("Success")

def main():

    library = generate_apk_list()
    server_login()

    # Download APKs
    print("\nDownloading APKs.  Please wait...\n")
    
    for apk in library:
        download_apks(apk)


main()
