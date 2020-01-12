#!/usr/bin/python3
from gpapi.googleplay import GooglePlayAPI, RequestError
import sys
import os
import getpass

def credential_login():

    # Variables
    email = input("EMAIL:  ")
    password = getpass.getpass("PASSWORD:  ")
    server = GooglePlayAPI("us_US","America/Denver")

    # Email/Password Login
    print('\nLogging in with EMAIL and PASSWORD...\n')
    server.login(email, password, None, None)  

    # Retrieve and Print GSFID and AUTHSUBTOKEN
    api_gsfId = str(server.gsfId)
    api_authSubToken = str(server.authSubToken)

    print("IMPORTANT!!!  Save GSFID and AUTHSUBTOKEN for later use!\n")
    print("GSFID:\t\t" + api_gsfId)
    print("AUTHSUBTOKEN:\t" + api_authSubToken + "\n")

def main():

    # Log into Google Servers
    credential_login()

main()