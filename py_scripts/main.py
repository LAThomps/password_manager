# This is the main code to manage running the Password Manager App

import json
import re
import os
import stat
import time
from pwinput import pwinput
from cryptography.fernet import Fernet
from passmgmt import WELCOME_STR, handle_client, read_json, dump_json

def initialize():
    """
    function for creating root user/using app for first time
    """
    # basic config file
    with open("config.json", "r") as file:
        config = json.load(file)
    print("\n\ncreating root user\n")

    # dict to be used for passwords
    data = {
        "USER" : {
            "root" : ""
        }
    }
    print("""
        your password must meet all of the following conditions:
            
        at least one capital letter
        at least one lowercase letter
        at least one special character (!#$*&@%_)
        at least one number 
        must be at least 8 characters long
        
        **This is a one-time entry, you cannot change the root user password
        after the first initialization.**
    """)

    # ensure user makes secure password
    while True:
        while True:
            # check conditions of master password entered
            master_pw = pwinput("enter your master password: ")
            one_capital = bool(re.search(r"[A-Z]", master_pw))
            one_lower = bool(re.search(r"[a-z]", master_pw))
            one_special = bool(re.search(r"[!#$*&@%_]", master_pw))
            one_num = bool(re.search(r"[0-9]", master_pw))
            len_8 = True if len(master_pw) > 7 else False

            # must be all to pass, let the user know which ones failed
            if not (one_capital & one_lower & one_special & one_num & len_8):
                print(f"""
                    password entered did not meet all criteria:
                    at least one capital\t\t{one_capital}
                    at least one lowercase\t\t{one_lower}
                    at least one special\t\t{one_special}
                    at lease one number\t\t\t{one_num}
                    must be at least 8 characters\t{len_8}

                    please try again
                """)
                continue 
            else:
                break

        # enter again, set root password if good
        check = pwinput("reenter your master password: ")
        if master_pw == check:
            data['USER']['root'] = master_pw
            print("root user created\n")
            break 
        else:
            print("your two passwords didn't match, try again")
            continue

    # start building process
    print("building password manager based on config settings")

    # right now this is only built for Fernet from cryptography library
    method = config['ENCRYPTION_METHOD']
    if method == "Feret":
        # Fernet guarantees data encrypted cannot be manipulated or read
        # with out the URL-safe base64-encoded 32-byte key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # make key in app dir, notify user to change KEY_LOCATION in meta.json file
        # if desired to move
        os.mkdir("stuff")
        key_path = "stuff/key.key"
        print("encryption key being saved under app directory")
        print("**if you want to move the .key file, just update the KEY_LOCATION")
        print("in the meta.json file (within the app directory)**\n")
        time.sleep(5)
        
        # once good, save key as bytes
        with open(key_path, "wb") as file:
            file.write(key)
        # make key file read-only
        os.chmod(key_path, stat.S_IREAD)
    else:
        print(f"unknown encryption method from config file `{method}`")
        return

    # data.json will contain the encrypted password information
    data_path = os.path.join(config['DATA_LOCATION'], "data.json")

    # config will get saved as meta.json, useful info to run app
    config['KEY_LOCATION'] = key_path
    config['DATA_LOCATION'] = data_path 

    # write json meta and data files, data is encrypted
    dump_json("meta.json", config, False)
    dump_json(data_path, data, True, fernet)
    print("initialization complete\n\n")
    return


def main():
    """
    workflow for running app
    """
    print(WELCOME_STR)

    # run initialize if first run
    initial_meta = read_json("mgr.json", False)
    if initial_meta['INITIAL'] == "True":
        initialize()
        initial_meta['INITIAL'] = "False"
        dump_json("mgr.json", initial_meta, False)
        # make mgr.json read-only after first run
        os.chmod("mgr.json", stat.S_IREAD)

    # read in meta information
    meta = read_json("meta.json", False)
    try:
        with open(meta['KEY_LOCATION'], "rb") as file:
            key = file.read()
    except:
        print(f"unable to open/find key file `{meta['KEY_LOCATION']}`")
        print("make sure file path is correct in meta.json")
        print('exiting....')
        time.sleep(5)
        return

    # decrypt data file to verify user, permit password management
    fernet = Fernet(key)
    data = read_json(meta['DATA_LOCATION'], True, fernet)
    print("Welcome to the password manager, please enter your master password to begin ")

    # verify user
    password = pwinput("password: ")
    tries = 0
    while password != data['USER']['root'] and tries < 3:
        tries += 1
        print(f"invalid you have {4 - tries} {'tries' if tries < 3 else 'try'} left")
        password = pwinput("enter password: ")
    if tries == 3 and password != data['USER']['root']:
        print("\nmaximum tries reached, terminating program")
        return

    # masking is preference of user, no masking is generally recommended if you want
    # to verify the passwords on add, edit
    ask_mask = input("enter `m` if you wish to mask all passwords for this session:  ")
    mask = True if ask_mask == "m" else False

    # function for actually running the app, defined in passmgmt.py
    data = handle_client(data, mask)

    # update data, encrypt, and end program
    print("updating database")
    dump_json(meta['DATA_LOCATION'], data, True, fernet)
    print("terminating program")
    return 

if __name__ == "__main__":
    main()