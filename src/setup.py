import sys
sys.dont_write_bytecode = True

from notify_utils import *
import subprocess, shlex, notify, json, requests, os

if len(sys.argv) == 2 and sys.argv[1] != "-u" or len(sys.argv) > 2:
    ntf_error("Wrong arguments.", sugg=f"Please use {PYTHON_VERSION} setup.py")

isupdate = len(sys.argv) == 2 and sys.argv[1] == "-u"

if not isupdate: ntf_info("\nThanks for downloading notify2!\n\nBase repo: https://github.com/Zanzibarr/Notify2\nScript made by @Zanzibarr.\nBeginning setup...\n")

if HOME == "/var/root":
    ntf_error("Please run the setup in user mode.")

#---------------------------------------------------------------
#region                  CONFIGURATIONS                        -
#---------------------------------------------------------------

if not isupdate: 
    
    config = False
    if os.path.exists(CONFIG_PATH):

        ntf_info(f"Found configuration file located in '{CONFIG_PATH}'.")
        choice = ntf_input("Wish to use this configuration file?", ["y", "n"])

        if choice == "y":
            config = True

    if not config and any(os.path.exists(config) for config in OLD_CONFIG_PATHS):

        old_path = OLD_CONFIG_PATHS[0] if os.path.exists(OLD_CONFIG_PATHS[0]) else OLD_CONFIG_PATHS[1]

        ntf_info(f"Found configuration file from a past version located in '{old_path}'.")
        choice = ntf_input("Wish to use this configuration file?", ["y", "n"])

        if choice == "y":
            ntf_info("Loading old configuration.")
            subprocess.run(shlex.split(f"cp {old_path} {CONFIG_PATH}"))
            config = True

    skip = False

    if not config:
        choice = ntf_input("wish to create a configuration file?", ["y", "n"])

        if choice == "n":
            ntf_warn("Without a configuration file you would need to specify each time the telegram API token and the chat you wish to send the message to.")
            ntf_info("No configuration file created.")
            skip = True

    if not config:

        ntf_info("Creating a new configuration file.")
        with open(CONFIG_PATH, "w") as f:
            f.write(json.dumps({"def":"default", "profiles":{}}, indent=4))

    if not skip:

        with open(CONFIG_PATH, "r") as f:
            configuration = json.loads(f.read())

        default = configuration["def"]
        profiles = configuration["profiles"]

        if len(profiles) > 0:

            ntf_info(f"Profiles available: {list(profiles.keys())}")

            choices = [key for key in profiles.keys()]
            choices.append("-new")
            name = ntf_input("Choose the profile to use (-new to create a new one): ", choices)

        new_def = True

        if len(profiles) == 0 or name == "-new":

            ntf_info("Creating a new profile.")
            name = ntf_input("Insert the name of the profile to create")
            token = ntf_input("Insert the telegram API token of the bot to use.")
            chat = ntf_input("Insert the default chat id to associate to the profile ('-q' to ignore this for now): ")
            while not requests.post(f"https://api.telegram.org/bot{token}/getMe").json()["ok"]:
                ntf_warn("The token specified isn't associated to a telegram bot, please use a valid token.")
                token = ntf_input("Insert the telegram API token of the bot to use. ('-q' to quit the setup) ")

                if token == "-q":
                    ntf_warn("Profile not created.", sugg="Using 'default' as default profile.")
                    new_def = False
                    break

            chat = "" if chat == "-q" else chat
            if new_def: notify.write_conf_profile(name=name, token=token, to_chat_id=chat)
        
        if new_def:
            ntf_info(f"Setting {name} as default profile.")
            notify.set_default_profile(name=name)

#endregion


#---------------------------------------------------------------
#region                    MOVING FILES                        -
#---------------------------------------------------------------

if not os.path.exists(DEST_PATH):
    ntf_info(f"Folder {DEST_PATH} not found, creating one.")
    os.mkdir(DEST_PATH)

ntf_info(f"Moving files to base path: {DEST_PATH}")
for file in os.listdir(BASE_PATH):
    subprocess.run(["cp", f"{BASE_PATH}/{file}", f"{DEST_PATH}/{file}"])

if not os.path.exists(f"{DEST_PATH}/python_module"):
    os.mkdir(f"{DEST_PATH}/python_module")

subprocess.run(["mv", f"{DEST_PATH}/notify.py", f"{DEST_PATH}/python_module/notify.py"])

#endregion

if isupdate: 
    exit(0)

#---------------------------------------------------------------
#region                   RC FILES EDIT                        -
#---------------------------------------------------------------

if not os.path.exists(f"{BASHRC_FILE}") and not os.path.exists(f"{ZSHRC_FILE}"):
    ntf_warn(f"Couldnt find {BASHRC_FILE} nor {ZSHRC_FILE}.\nTo use notify as a python module: use the module {DEST_PATH}/python_module/notify.py\nTo use notify as a shell command: {PYTHON_VERSION} {DEST_PATH}/app.py <options>")

else:
    ntf_warn(f"If you're not using zsh or bash you can find the files needed to use notify inside the {DEST_PATH}/ folder.\nTo use notify as a python module: use the module {DEST_PATH}/python_module/notify.py\nTo use notify as a shell command: {PYTHON_VERSION} {DEST_PATH}/app.py <options>")

check_bashrc = False
check_zshrc = False

if os.path.exists(BASHRC_FILE):

    with open(BASHRC_FILE, "r") as f:
        bash_file = f.read()

    if OLD_SHELL_RC_EDIT in bash_file:
        bash_file = bash_file.replace(OLD_SHELL_RC_EDIT, "")
        with open(BASHRC_FILE, "w") as f:
            f.write(bash_file)

    if SHELL_RC_EDIT in bash_file:
        check_bashrc = True

    if not check_bashrc:

        ntf_info(f"Writing on {BASHRC_FILE} file (append).")
        with open(BASHRC_FILE, "a") as f:
            f.write(f"{SHELL_RC_EDIT}\n")

else:

    check_bashrc = True

if os.path.exists(ZSHRC_FILE):

    with open(ZSHRC_FILE, "r") as f:
        zsh_file = f.read()

    if OLD_SHELL_RC_EDIT in zsh_file:
        zsh_file = zsh_file.replace(OLD_SHELL_RC_EDIT, "")
        with open(ZSHRC_FILE, "w") as f:
            f.write(zsh_file)

    if SHELL_RC_EDIT in zsh_file:
        check_zshrc = True

    if not check_zshrc:

        ntf_info(f"Writing on {ZSHRC_FILE} file (append).")
        with open(ZSHRC_FILE, "a") as f:
            f.write(f"{SHELL_RC_EDIT}\n")

else:

    check_zshrc = True

if not check_zshrc or not check_bashrc:
    ntf_warn(f"To use the application now, you will have to reload the RC file (bash or zsh).")

#endregion

if any(os.path.exists(file) for file in OLD_CONFIG_PATHS):
    choice = ntf_input("Wish to remove old configuration files?", ["y", "n"])

    if choice == "y":
        if os.path.exists(OLD_CONFIG_PATHS[0]): subprocess.run(shlex.split(f"rm {OLD_CONFIG_PATHS[0]}"))
        if os.path.exists(OLD_CONFIG_PATHS[1]): subprocess.run(shlex.split(f"rm {OLD_CONFIG_PATHS[1]}"))
        ntf_info("Old configuration files removed.")

if os.path.exists(OLD_DEST_PATH):
    choice = ntf_input("Wish to remove old version of notify?", ["y", "n"])

    if choice == "y":
        subprocess.run(shlex.split(f"rm -r {OLD_DEST_PATH}"))

ntf_info("notify2 installed.")