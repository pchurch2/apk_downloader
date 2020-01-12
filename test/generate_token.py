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
    print('\nLogging in with email and password...\n')
    server.login(email, password, None, None)

    gsfId = int(os.environ["GPAPI_GSFID"])
    authSubToken = os.environ["GPAPI_TOKEN"]

    print("\nIMPORTANT!!!  Save GSFID and AUTHSUBTOKEN for later use!")
    print("GSFID:\t" + gsfId)
    print("AUTHSUBTOKEN:\t" + authSubToken)

def main():

    # Log into Google Servers
    credential_login()

main()