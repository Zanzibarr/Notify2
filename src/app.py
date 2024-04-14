import sys
sys.dont_write_bytecode = True

import python_module.notify as notify
from notify_utils import *
import subprocess, shlex, requests, json


#---------------------------------------------------------------
#region                       HELP                             -
#---------------------------------------------------------------

def __help(parsed : list[dict]):
    
    if len(parsed) > 2 or len(parsed) == 2 and len(parsed[1]["list"]) > 1:
        ntf_warn("Too many arguments.", sugg=f"Command used: '{ALIAS} {parsed[0]['list'][0]} {parsed[1]['list'][0]}'.")
        if ntf_input("Proceed anyways?", ["y", "n"]) == "n":
            ntf_info("Exiting.")
            exit(0)

    elif len(parsed) == 1 and len(parsed[0]["list"]) > 1:
        ntf_error(f"'{' '.join(parsed[0]['list'][1:])}' is not a {ALIAS} option.", sugg=f"Example usage: '{ALIAS} {parsed[0]['list'][0]} {PARAMETERS['text'][0]}' to view text help.")

    elif len(parsed) > 1 and len(parsed[0]["list"]) > 1:
        ntf_warn("Too many aruguments.", sugg=f"Command used: '{ALIAS} {parsed[0]['list'][0]} {parsed[1]['list'][0]}'.")
        if ntf_input("Proceed anyways?", ["y", "n"]) == "n":
            ntf_info("Exiting.")
            exit(0)

    msg = HELP_START

    if len(parsed) > 1:
        msg += f"{ALIAS} {parsed[1]['list'][0]} options:\n\n"
        msg += f"{EXPLANATION[parsed[1]['alias']]}\n\n"
    
    else:
        msg += f"{ALIAS} options:\n\n"
        for exp in EXPLANATION:
            msg += f"{EXPLANATION[exp]}\n\n"

    msg += f"Values for boolean options can be omitted and their value will be assigned to 'True'. (Es: '{PARAMETERS['dino'][0]} True' =: '{PARAMETERS['dino'][0]}')\n"

    msg += HELP_END

    print(msg)

#endregion


#---------------------------------------------------------------
#region                     VERSION                            -
#---------------------------------------------------------------

def __version(parsed : list[dict]):

    if len(parsed) > 1 or len(parsed[0]["list"]) > 1:
        ntf_warn("Too many arguments.", sugg=f"Command used: '{ALIAS} {parsed[0]['list'][0]}'.")
    
    print(f"notify2 version: {VERSION}")

#endregion


#---------------------------------------------------------------
#region                      UPDATE                            -
#---------------------------------------------------------------

def __update(parsed : list[dict]):

    if len(parsed) > 1 or len(parsed[0]['list']) > 2:
        ntf_warn("Too many arguments.", sugg=f"Command used: '{ALIAS} {PARAMETERS['update'][0]} {parsed[0]['list'][1] if len(parsed[0]['list']) > 1 else 'latest'}'.")
    
    try:
        ntf_info("Fetching releases.")
        response = requests.get(f"{RELEASES}/{RELEASES_LIST}")
    except Exception as e:
        ntf_error(CONNECTION_ISSUE)

    if not response.ok:
        ntf_error(f"Status code: '{response.status_code}'.", sugg=OPEN_ISSUE)

    versions = json.loads(response.content.decode('utf-8'))
    asked_version = parsed[0]["list"][1] if len(parsed[0]["list"]) > 1 else "latest"
    
    if asked_version not in versions:
        ntf_warn(f"Cannot find version '{asked_version}'.", sugg="Here's the list of available versions:")
        print(json.dumps(list(versions.keys()), indent=2))
        choices = [ver for ver in versions.keys()]
        choices.append("-q")
        asked_version = ntf_input("Which version you want to update to? ('-q' to exit update)", choices)

        if asked_version == "-q":
            ntf_info("Exiting.")
            exit(0)

    new_version = versions[asked_version]['version']
    if VERSION == new_version:
        ntf_info(f"Already to version {VERSION}.")
        exit(0)

    ntf_info(f"Downloading version {new_version}.")
    choice = ntf_input("Proceed?", ["y", "n"])

    if choice == "n":
        ntf_warn("notify not updated.", sugg="Exiting.")
        exit(0)

    asked_version = f"v{new_version}.zip"

    if not os.path.exists(f"{BASE_PATH}/ntfdwntmp"):
        os.mkdir(f"{BASE_PATH}/ntfdwntmp")

    downloaded = requests.get(f"{RELEASES}/{asked_version}", allow_redirects=True)
    with open(f"{BASE_PATH}/ntfdwntmp/{asked_version}", "wb") as f:
        f.write(downloaded.content)

    subprocess.run(shlex.split(f"unzip {BASE_PATH}/ntfdwntmp/{asked_version} -d {BASE_PATH}/ntfdwntmp/"), stdout=subprocess.DEVNULL)
    subprocess.run(shlex.split(f"rm {BASE_PATH}/ntfdwntmp/{asked_version}"))
    subprocess.run(shlex.split(f"{PYTHON_VERSION} {BASE_PATH}/ntfdwntmp/setup.py -u"))
        
    ntf_info("notify2 has been updated")

#endregion


#---------------------------------------------------------------
#region                    UNINSTALL                           -
#---------------------------------------------------------------

def __uninstall(parsed : list[dict]):

    if len(parsed) > 1 or len(parsed[0]["list"]) > 1:
        ntf_warn("Too many arguments.", sugg=f"Use '{ALIAS} {PARAMETERS['uninstall'][0]}' to uninstall notify.\nCommand used: '{ALIAS} {PARAMETERS['uninstall'][0]}'")
        
    choice = ntf_input("Proceeding to uninstall notify?", ["y", "n"])

    if choice == "n":
        ntf_info("Uninstall aborted.")
        exit(0)
    
    ntf_info("Uninstalling...")
    subprocess.run(shlex.split(f"rm -r {DEST_PATH}"))
    
    if os.path.exists(BASHRC_FILE):
        bashrc = ""
        with open(BASHRC_FILE, "r") as f:
            bashrc = f.read()
        bashrc = bashrc.replace(SHELL_RC_EDIT, "")
        with open(BASHRC_FILE, "w") as f:
            f.write(bashrc)
    
    if os.path.exists(ZSHRC_FILE):
        zshrc = ""
        with open(ZSHRC_FILE, "r") as f:
            zshrc = f.read()
        zshrc = zshrc.replace(SHELL_RC_EDIT, "")
        with open(ZSHRC_FILE, "w") as f:
            f.write(zshrc)
    
    ntf_info("notify has been succesfully uninstalled.\nPlease reload the RC file (bash or zsh).")

#endregion


#---------------------------------------------------------------
#region                     CONFIG                             -
#---------------------------------------------------------------

def __config(parsed : list[dict]):

    if len(parsed) > 1:
        ntf_warn("Too many arguments.", sugg=f"Command used: '{ALIAS} {' '.join(parsed[0]['list'])}'.")
        if ntf_input("Proceed anyways?", ["y", "n"]) == "n":
            ntf_info("Exiting.")
            exit(0)

    if len(parsed[0]["list"]) == 1:
        ntf_error("Too few arguments.", sugg=f"Use '{ALIAS} {PARAMETERS['help'][0]} {PARAMETERS['config'][0]}' to view config options.")

    config_parser = arg_parser()

    for p in [
        "add", "token", "remove", "edit", "set", "see", "from_chat",
        "to_chat", "webprev", "dino", "protcont", "reply_anyway", "pmode"
    ]:
        config_parser.add_param(p, PARAMETERS[p])

    config_parsed = config_parser.parse(parsed[0]["list"], dict=True, merge=True, skip=True)
    
    if len([param for param in config_parsed.keys() if param in ["add", "remove", "edit", "set", "see"]]) > 1:
        ntf_error("Too many arguments.", sugg=f"Use '{ALIAS} {PARAMETERS['help'][0]} {PARAMETERS['config'][0]}' to view config options.")
    
    alias = [key for key in PARAMETERS if parsed[0]["list"][1] in PARAMETERS[key]][0]

    for param in [p for p in config_parsed if p in SHORTCUTS]:
        if config_parsed[param] == "": config_parsed[param] = "True"

    with open(CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    if alias == "add":

        if "token" not in config_parsed:
            ntf_error("Missing token.", sugg=f"Use '{ALIAS} {PARAMETERS['help'][0]} {PARAMETERS['config'][0]}' to view config options.")
        
        if config_parsed[alias] in configuration["profiles"]:
            ntf_warn(f"The profile '{config_parsed[alias]}' already exists.")
            if ntf_input(f"Overwrite this profile?", ["y", "n"]) == "n":
                ntf_info("Configuration file unchanged.")
                exit(0)

        notify.write_conf_profile(config_parsed["add"], config_parsed["token"], config_parsed.get("from_chat", ""), config_parsed.get("to_chat", ""), config_parsed.get("webprev", ""), config_parsed.get("dino", ""), config_parsed.get("protcont", ""), config_parsed.get("reply_anyway", ""), config_parsed.get("pmode", ""))

        ntf_info("Profile created succesfully.")

    elif alias == "remove":
        
        if config_parsed[alias] not in configuration["profiles"]:
            ntf_warn(f"The profile '{config_parsed[alias]}' doesn't exist.")
            ntf_info("Configuration file unchanged.")
            exit(0)

        ntf_warn(f"Removing profile '{config_parsed[alias]}'.")
        if ntf_input("Confirm?", ["y", "n"]) == "n":
            ntf_info("Configuration file unchanged.")
            exit(0)

        notify.remove_profile(config_parsed[alias])

        ntf_info("Profile removed succesfully.")

    elif alias == "edit":
        
        if config_parsed[alias] not in configuration["profiles"]:
            ntf_warn(f"The profile '{config_parsed[alias]}' doesn't exist.")
            ntf_info("Configuration file unchanged.")
            exit(0)

        ntf_warn(f"Editing profile '{config_parsed[alias]}'.")
        if ntf_input("Confirm?", ["y", "n"]) == "n":
            ntf_info("Configuration file unchanged.")
            exit(0)

        notify.write_conf_profile(config_parsed["edit"], config_parsed.get("token", ""), config_parsed.get("from_chat", ""), config_parsed.get("to_chat", ""), config_parsed.get("webprev", ""), config_parsed.get("dino", ""), config_parsed.get("protcont", ""), config_parsed.get("reply_anyway", ""), config_parsed.get("pmode", ""))

        ntf_info("Profile changed succesfully.")

    elif alias == "set":
        
        if config_parsed[alias] not in configuration["profiles"]:
            ntf_warn(f"The profile '{config_parsed[alias]}' doesn't exist.")
            ntf_info("Configuration file unchanged.")
            exit(0)

        ntf_warn(f"Setting the profile '{config_parsed[alias]}' as default.")
        if ntf_input("Confirm?", ["y", "n"]) == "n":
            ntf_info("Configuration file unchanged.")
            exit(0)

        notify.set_default_profile(config_parsed[alias])

        ntf_info("Default profile changed succesfully.")

    elif alias == "see":
        
        print(json.dumps(configuration, indent=4))

    else:
        ntf_error(WRONG_ARGUMENTS, sugg=f"Use '{ALIAS} {PARAMETERS['help'][0]} {PARAMETERS['config'][0]}' to view config options.")

#endregion


#---------------------------------------------------------------
#region                      SEND                              -
#---------------------------------------------------------------

def __send(parsed : list[dict]):

    index = 0

    if parsed[index]["alias"] == "profile":

        prof_parser = arg_parser()

        for p in [
            "profile", "token", "from_chat", "to_chat", "webprev",
            "dino", "protcont", "reply_anyway", "pmode"
        ]:
            prof_parser.add_param(p, PARAMETERS[p])

        prof_parsed = prof_parser.parse(parsed[index]["list"], skip=False, dict=True, merge=True)

        profile_name = prof_parsed.get("profile", "")

        for param in prof_parsed:
            if len(prof_parsed[param]) > 0 and any(value[0] == "-" for value in prof_parsed[param].split()):
                ntf_warn(f"'{prof_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if profile_name != "": 
            with open(CONFIG_PATH, "r") as f:
                if profile_name not in json.loads(f.read())["profiles"]:
                    ntf_error(f"Cannot find '{profile_name}' as a profile in the configuration file.")

        if profile_name != "": bot.load_profile(name=profile_name)

        for param in [p for p in prof_parsed if p in SHORTCUTS]:
            if prof_parsed[param] == "": prof_parsed[param] = "True"

        bot.edit_profile(prof_parsed.get("token", ""), prof_parsed.get("from_chat", ""), prof_parsed.get("to_chat", ""), prof_parsed.get("webprev", ""), prof_parsed.get("dino", ""), prof_parsed.get("protcont", ""), prof_parsed.get("reply_anyway", ""), prof_parsed.get("pmode", ""))

        index += 1

    parsed = parsed[index:]
    send_parser = arg_parser()

    #region -------------------------------- TEXT --------------------------------

    if parsed[0]["alias"] == "text":

        for p in [
            "text", "to_chat", "mthread", "pmode", "webprev",
            "dino", "protcont", "reply_id", "reply_anyway"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if send_parsed["text"] == "":
            ntf_error("Message body is empty, message not sent.", sugg=f"Example usage: '{ALIAS} {PARAMETERS['text'][0]} Text/Path [<text_options>]*' to send a text message either specifying the content or a file where to read it from.")

        for param in [p for p in send_parsed if p in SHORTCUTS]:
            if send_parsed[param] == "": send_parsed[param] = "True"

        if os.path.exists(send_parsed["text"]):
            bot.send_message_by_file(send_parsed["text"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("pmode", ""), send_parsed.get("webprev", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        else:
            bot.send_message_by_text(send_parsed["text"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("pmode", ""), send_parsed.get("webprev", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        
    #endregion

    #region -------------------------------- PHOTO --------------------------------

    if parsed[0]["alias"] == "photo":

        for p in [
            "photo", "to_chat", "mthread", "caption", "pmode",
            "spoiler", "dino", "protcont", "reply_id", "reply_anyway"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if send_parsed["photo"] == "" or not os.path.exists(send_parsed["photo"]):
            ntf_error(f"No file named '{send_parsed['photo']}', message not sent.")

        for param in [p for p in send_parsed if p in SHORTCUTS]:
            if send_parsed[param] == "": send_parsed[param] = "True"
        
        bot.send_photo_by_path(send_parsed["photo"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("caption", ""), send_parsed.get("pmode", ""), send_parsed.get("spoiler", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        
    #endregion

    #region -------------------------------- AUDIO --------------------------------

    if parsed[0]["alias"] == "audio":

        for p in [
            "audio", "to_chat", "mthread", "caption", "pmode", "duration",
            "performer", "title", "thumbnail", "dino", "protcont", "reply_id", "reply_anyway"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if send_parsed["audio"] == "" or not os.path.exists(send_parsed["audio"]):
            ntf_error(f"No file named '{send_parsed['audio']}', message not sent.")

        for param in [p for p in send_parsed if p in SHORTCUTS]:
            if send_parsed[param] == "": send_parsed[param] = "True"
        
        bot.send_audio_by_path(send_parsed["audio"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("caption", ""), send_parsed.get("pmode", ""), send_parsed.get("duration", ""), send_parsed.get("performer", ""), send_parsed.get("title", ""), send_parsed.get("thumbnail", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        
    #endregion

    #region -------------------------------- DOCUMENT --------------------------------
        
    if parsed[0]["alias"] == "document":

        for p in [
            "document", "to_chat", "mthread", "thumbnail", "caption", "pmode",
            "typedetect", "dino", "protcont", "reply_id", "reply_anyway"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if send_parsed["document"] == "" or not os.path.exists(send_parsed["document"]):
            ntf_error(f"No file named '{send_parsed['document']}', message not sent.")

        for param in [p for p in send_parsed if p in SHORTCUTS]:
            if send_parsed[param] == "": send_parsed[param] = "True"
        
        bot.send_document_by_path(send_parsed["document"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("thumbnail", ""), send_parsed.get("caption", ""), send_parsed.get("pmode", ""), send_parsed.get("typedetect", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        
    #endregion

    #region -------------------------------- VIDEO --------------------------------
        
    if parsed[0]["alias"] == "video":

        for p in [
            "video", "to_chat", "mthread", "duration", "width", "height", "thumbnail", "caption",
            "pmode", "spoiler", "streaming", "dino", "protcont", "reply_id", "reply_anyway"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        if send_parsed["video"] == "" or not os.path.exists(send_parsed["video"]):
            ntf_error(f"No file named '{send_parsed['video']}', message not sent.")

        for param in [p for p in send_parsed if p in SHORTCUTS]:
            if send_parsed[param] == "": send_parsed[param] = "True"
        
        bot.send_video_by_path(send_parsed["video"], send_parsed.get("to_chat", ""), send_parsed.get("mthread", ""), send_parsed.get("duration", ""), send_parsed.get("width", ""), send_parsed.get("height", ""), send_parsed.get("thumbnail", ""), send_parsed.get("caption", ""), send_parsed.get("pmode", ""), send_parsed.get("spoiler", ""), send_parsed.get("streaming", ""), send_parsed.get("dino", ""), send_parsed.get("protcont", ""), send_parsed.get("reply_id", ""), send_parsed.get("reply_anyway", ""))
        
    #endregion

    #region -------------------------------- EXCEPTION --------------------------------
        
    if parsed[0]["alias"] == "exception":

        for p in [
            "exception", "to_chat"
        ] :
            send_parser.add_param(p, PARAMETERS[p])

        send_parsed = send_parser.parse(parsed[0]["list"], skip=False, dict=True, merge=True)

        for param in send_parsed:
            if len(send_parsed[param]) > 0 and any(value[0] == "-" for value in send_parsed[param].split()):
                ntf_warn(f"'{send_parsed[param]}' has been considered as a value for the '{PARAMETERS[param][0]}' option and not splitted in multiple options: if it was supposed to be a command, check wether you wrote it correctly, otherwise ignore this warning.")

        bot.send_exception(send_parsed.get("exception", ""), send_parsed.get("to_chat", ""))

    #endregion

#endregion


#---------------------------------------------------------------
#region                 EXECUTE COMMAND                        -
#---------------------------------------------------------------

def __execute_commands(parsed : list[dict]) -> None:

    if parsed[0]["alias"] == "help":
        __help(parsed)
    
    elif parsed[0]["alias"] == "version":
        __version(parsed)

    elif parsed[0]["alias"] == "update":
        __update(parsed)

    elif parsed[0]["alias"] == "uninstall":
        __uninstall(parsed)

    elif parsed[0]["alias"] == "config":
        __config(parsed)

    elif parsed[0]["alias"] in (
        "profile", "text", "photo", "audio",
        "document", "video", "exception"
        ):
        __send(parsed)

    else:
        ntf_error(WRONG_ARGUMENTS, sugg=main_parser.help())

#endregion


#---------------------------------------------------------------
#region                  MASTER PARSER                         -
#---------------------------------------------------------------

def __build_master_parser() -> arg_parser:

    parser = arg_parser()

    for p in [
        "help", "version", "update", "uninstall",
        "config", "profile", "text", "photo",
        "audio", "document", "video", "exception"
    ] :
        parser.add_param(p, PARAMETERS[p])

    return parser

#endregion

def main():

    global main_parser, bot

    try:
    
        with open(CONFIG_PATH, "r") as f:
            default = json.loads(f.read())["def"]

        bot = notify.bot(profile=default)

        main_parser = __build_master_parser()
        parsed = main_parser.parse(sys.argv)

        __execute_commands(parsed)

    except Exception as e:    
        if "NOTIFY_EXCEPTION: " in repr(e):
            raise e
        else:
            ntf_error(f"Something went wrong: {e}\n{OPEN_ISSUE}")

if __name__ == "__main__":
    main()