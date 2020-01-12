#!/usr/bin/python3
from gpapi.googleplay import GooglePlayAPI, RequestError
import sys
import os
import getpass

def token_login():

    # Variables
    gsfId = input("GSFID:  ")
    authSubToken = getpass.getpass("AUTHSUBTOKEN:  ")
    server = GooglePlayAPI("us_US","America/Denver")

    # LOGIN
    print("\nLogging in with GSFID and AUTHSUBTOKEN...\n")
    server.login(None, None, int(gsfId), authSubToken)

def main():

    # Log into Google Servers
    token_login()

main()