# utility functions for running Password Manager

import json
from pwinput import pwinput 
from pyperclip import copy as to_clipboard
from cryptography.fernet import Fernet

WELCOME_STR = r"""
        ________              ________  ________                       ________   ________   _______
       |        |     /\     |         |         \                  / |        | |        | |       |_
       |        |    /  \    |         |          \                /  |        | |        | |         |
       |________|   /    \   |________ |________   \      /\      /   |        | |________| |         |
       |           /______\           |         |   \    /  \    /    |        | |     \    |         |
       |          /        \          |         |    \  /    \  /     |        | |      \   |        _|
       |         /          \ ________| ________|     \/      \/      |________| |       \  |_______|
                                          _                       ________   ________  ________
            /\      /\           /\      | \      |      /\      |        | |         |        |
           /  \    /  \         /  \     |  \     |     /  \     |          |         |        |
          /    \  /    \       /    \    |   \    |    /    \    |________  |_____    |________|
         /      \/      \     /______\   |    \   |   /______\   |        | |         |     \
        /                \   /        \  |     \  |  /        \  |        | |         |      \
       /                  \ /          \ |      \_| /          \ |________| |________ |       \

    """

def read_json(
        filepath: str,
        is_encrypted: bool,
        fernet: Fernet | None = None
    ) -> dict:
    """
    reading json file into python dictionary

    Parameters
    ----------
    filepath : str
        location of json file
    is_encrypted : bool
        whether file is encrypted or not
    fernet : Fernet | None, optional
        Fernet encryption object (to decrypt), by default None

    Returns
    -------
    dict
        contents of json file
    """
    if is_encrypted:
        assert fernet, "no Fernet object passed to decrypt json"
        with open(filepath, "rb") as file:
            stuff = file.read()
        clean = fernet.decrypt(stuff).decode("utf-8")
        to_json = json.loads(clean)
        return to_json
    else:
        with open(filepath, "r") as file:
            return json.load(file)

def dump_json(
        filepath: str,
        update: dict, 
        encrypt: bool,
        fernet: Fernet | None = None
    ) -> None:
    """
    dump a python dictionary to json file

    Parameters
    ----------
    filepath : str
        location of json to dump to
    update : dict
        dictionary to be dumped
    encrypt : bool
        whether to encrypt or not
    fernet : Fernet | None, optional
        Fernet encryption object, by default None
    
    Returns
    -------
    None

    """
    if encrypt:
        assert fernet, "no Fernet object passed to encrypt json"
        as_str = json.dumps(update)
        as_bytes = as_str.encode("utf-8")
        encrypted_bytes = fernet.encrypt(as_bytes)
        with open(filepath, "wb") as file:
            file.write(encrypted_bytes)
        return
    else:
        with open(filepath, "w") as file:
            json.dump(update, file, indent=4)

def handle_client(
        data: dict, 
        mask: bool = False
    ) -> dict:
    """
    function for using/updating password manager data

    Parameters
    ----------
    data : dict
        dictionary of user password data
    mask : bool, optional
        whether or not to mask passwords as they're typed/displayed

    Returns
    -------
    dict
        updated data dictionary
    """
    action = input(f"""
        welcome, enter the appropriate option to continue

        `a`     add new credentials
        `c`     copy current credentials to clipboard
        `e`     edit current credentials
        `r`     remove current credentials
        `v`     view titles of all credentials
        `x`     to quit
    """)

    # run loop until user terminates program
    while True:
        while action not in {'a','c','e','r','v','x'}:
            action = input("please enter a valid option (`a`, `c`, `e`, `r`, `v`, `x`):\t")

        # adding credentials
        if action == 'a':
            print("adding new credentials\n")
            while True:
                title = input("enter the title of these credentials or `exit`:  ")
                # allow user to exit if mistakenly entered `a`
                if title == 'exit':
                    print("aborting addition of new credentials\n")
                    break
                # 'USER' is a part of data.json but should not be displayed at any point in program
                elif title == "USER":
                    print("`USER` is an invalid title, try again\n")
                    break
                elif title in data.keys():
                    print(f"title `{title}` already in database, enter `e` to edit exsisting credentials")
                    break
                else:
                    # make new credentials, let user validate, retry if error made
                    local_user = input("enter the username for this credential:  ")
                    if mask:
                        new_pw = pwinput("enter password for this credential:  ")
                    else:
                        new_pw = input("enter password for this credential:  ")
                    print(f"""
                            new credentials created:
                                
                            title:      {title}
                            username:   {local_user}
                            password:   {'`masked`' if mask else new_pw}
                    """)
                    try_again = input("enter `r` to retry or any other key to choose another action:  ")
                    if try_again == 'r':
                        print("retry adding credentials\n")
                    else:
                        # update data dictionary
                        data[title] = {
                            "username" : local_user,
                            "password" : new_pw
                        }
                        print("new credentials added\n")
                        break  
        # main function for using Password Manager, copies password to clipboard
        elif action == 'c':
            title = input("enter the title of the credentials:  ")
            if title == "USER": # same as in `a`
                print("cannot view `USER` credentials\n")
            # this version of password is always masked
            elif title in data.keys():
                to_clipboard(data[title]['password'])
                print(f"""
                    username:  {data[title]['username']}
                    password:  (copied to clipboard)
                """)
            else:
                print(f"title {title} not found in credentials\n")
        # editing credentials (username or password)
        elif action == 'e':
            print("editing current credentials\n")
            title = input("enter the title of the credentials or `exit`:  ")
            if title == "USER": # same as `a` and `c`
                print("cannot edit `USER` credentials\n")
            elif title in data.keys():
                # similar code to adding credentials, update data dict 
                print(f"editing credentials for {title}")
                while True:
                    print(f"""
                        current credentials:
                            
                        username:  {data[title]['username']}
                        password:  {'masked' if mask else data[title]['password']}
                    """)
                    local_user = input("enter the username for this credential:  ")
                    if mask:
                        new_pw = pwinput("enter password for this credential:  ")
                    else:
                        new_pw = input("enter password for this credential:  ")
                    print(f"""
                        new credentials created:
                            
                        title:      {title}
                        username:   {local_user}
                        password:   {'`masked`' if mask else new_pw}
                    """)
                    try_again = input("enter `r` to retry or any other key to choose another action:  ")
                    if try_again == 'r':
                        print("retry adding credentials\n")
                        continue 
                    else:
                        data[title] = {
                            "username" : local_user,
                            "password" : new_pw
                        }
                        print("new credentials added\n")
                        break 
            elif title == 'exit': # leave the loop
                pass
            else:
                print(f"title `{title}` not found in credentials\n")
        # removing credentials
        elif action == 'r':
            print("removing credentials from database\n")
            title = input("enter the title of the credentials or `exit`:  ")
            if title == "USER":
                print("cannot remove `USER` credentials\n") # nice try
            elif title in data.keys():
                # add second layer of validation
                keep_going = input(f"are you sure you want to remove credentials for {title} (y/n):  ")
                keep_going = True if keep_going.lower() == 'y' else False
                if keep_going:
                    del data[title]
                else:
                    print("aborting removal of credentials\n")
            elif title == 'exit': # leave the loop
                pass
            else:
                print(f"title `{title}` not found in credentials\n")
        # incase you forget the titles of the credentials you have saved, 
        # view them so you can know what to enter
        elif action == 'v':
            print("\ntitles for credentials:")
            print([key for key in data.keys() if key != "USER"]) # don't show user stuff
            print()
        elif action == 'x': # exit app
            break
        action = input("enter another action (`a`, `c`, `e`, `r`, `v`) or `x` to quit:  ")
    return data
    