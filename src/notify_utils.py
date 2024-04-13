import os, platform, sys, json

#---------------------------------------------------------------
#region                       PATHS                            
#---------------------------------------------------------------

HOME = os.path.expanduser("~")
CONFIG_PATH = f"{HOME}/.zanz_notify_profiles"#f"{HOME}/.notify2_profiles"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DEST_PATH = f"{HOME}/.notify2"

OS = platform.system()
SHELL_RC_FILE = f"{HOME}/.zshrc"
PYTHON_VERSION = "/usr/bin/python3"

#endregion


#---------------------------------------------------------------
#region                     CONSTANTS                          
#---------------------------------------------------------------
ALIAS = "notify"
VERSION = "1.0.0"

SHELL_RC_EDIT = f"""

#notify2
alias {ALIAS} = '{PYTHON_VERSION} {DEST_PATH}/notify2_cmd.py'
export PYTHONPATH = '{DEST_PATH}/python_module'

"""

HELP_START = "\nHi! Thanks for using notify2!\n\nIf this instructions are not helping, please open an issue on github or give a look to the telegram API website (linked at the end of this message).\n\nHere's the """
HELP_END = f"""

Base folder: {BASE_PATH}
Profiles file: {CONFIG_PATH}
Base repository: https://github.com/Zanzibarr/Notify2
Telegram API explanation: https://core.telegram.org/bots/api

Version: {VERSION}
"""
#endregion


#---------------------------------------------------------------
#region                      ERRORS                            
#---------------------------------------------------------------

OPEN_ISSUE = "Please open an issue on GitHub about it."
WRONG_ARGUMENTS = "Wrong arguments."

#endregion


#---------------------------------------------------------------
#region                      LOGGING                           
#---------------------------------------------------------------

INFO_MSG  = "\033[92m\033[1m[ INFO  ]:\033[0m "
INPUT_MSG = "\033[94m\033[1m[ INPUT ]:\033[0m "
WARN_MSG  = "\033[93m\033[1m[ WARN  ]:\033[0m "
ERROR_MSG = "\033[91m\033[1m[ ERROR ]:\033[0m "

def ntf_error(msg : str, loc : str = "", line : int = "", sugg : str = "") -> None:

    [ print(f"{ERROR_MSG}{line}" if line != "" else "") for line in msg.splitlines() ]
    if loc != "": print(f"{ERROR_MSG}Origin: {loc}:{line}")
    if sugg != "": ntf_info(sugg)
    exit(1)

def ntf_info(msg : str) -> None:

    [ print(f"{INFO_MSG}{line}" if line != "" else "") for line in msg.splitlines() ]

def ntf_warn(msg : str, loc : str = "", line : int = "", sugg : str = ""):

    [ print(f"{WARN_MSG}{line}" if line != "" else "") for line in msg.splitlines() ]
    if loc != "": print(f"{WARN_MSG}Origin: {loc}:{line}")
    if sugg != "": ntf_info(sugg)

def ntf_input(msg : str, options : list[str]) -> str:

    if len(msg.splitlines()) > 1: ntf_warn("Input message should contain only one line for readability.")

    choice = input(f"{INPUT_MSG}{msg} {str(options).replace(',', ' |')}: ")
    while choice not in options:
        ntf_warn("Command not recognised.")
        choice = input(f"{INPUT_MSG}{msg} {str(options).replace(',', ' |')}: ")

    return choice

def ntf_exc(msg : str, loc : str = "", line : int = "") -> None:

    ntf_error(msg=msg, loc=loc, line=line)
    raise Exception(msg)


#endregion


#---------------------------------------------------------------
#region                      PARSER                            
#---------------------------------------------------------------
class arg_parser:

    def __init__(self):
        self.__params = {}

    def add_param(self, alias : str, cmd_list : list[str]) -> None:

        if alias in self.__params.keys(): ntf_error(f"PARSER: Alias {alias} has a duplicate.\n{OPEN_ISSUE}", loc=__file__, line=sys._getframe().f_lineno)
        if any(p_cmd in self.__params[name] for p_cmd in cmd_list for name in self.__params.keys()): ntf_error(f"PARSER: A command in {cmd_list} has a duplicate in the parser.\n{OPEN_ISSUE}", loc=__file__, line=sys._getframe().f_lineno)
        if len(cmd_list) == 0: ntf_error(f"PARSER: No commands for alias {alias}.\n{OPEN_ISSUE}", loc=__file__, line=sys._getframe().f_lineno)

        self.__params[alias] = cmd_list

    def parse(self, argv : list[str], skip : bool = True, dict : bool = False, merge : bool = False) -> list[dict]:

        parsed = {} if dict else []

        last_alias = ""

        start = 1 if skip else 0
        
        for token in argv[start:]:
            alias = next((key for key in self.__params.keys() if token in self.__params[key]), None)

            if alias is None and len(parsed.keys() if dict else parsed) == 0:
                ntf_error(WRONG_ARGUMENTS, sugg=self.help())
            
            if alias is None:
                if dict:
                    parsed[last_alias].append(token)
                else:
                    parsed[-1]["list"].append(token)
            else:
                if dict:
                    if merge and last_alias != "": parsed[last_alias] = " ".join(parsed[last_alias])
                    parsed[alias] = []
                    last_alias = alias
                else:
                    parsed.append({"alias":alias, "list":[token]})

        if merge and last_alias != "": parsed[last_alias] = " ".join(parsed[last_alias])

        return parsed

    def help(self) -> str:

        if "help" not in self.__params: return "First element in the list to parse is not a command."

        return f"Use {ALIAS} {str(self.__params['help']).replace(',', ' |')} to view options."
    
    def params(self) -> dict :
        
        return self.__params

PARAMETERS = {

    "help" : ["-help", "-h", "--help", "--h"],
    "version" : ["-version", "--version", "--v"],
    "update" : ["-update", "-u"],
    "dev" : ["-dev", "-d"],
    "uninstall" : ["-uninstall"],
    "config" : ["-conf", "-config", "-c"],
    "add" : ["-add"],
    "remove" : ["-rm", "-r", "-remove"],
    "edit" : ["-edit", "-e"],
    "set" : ["-set", "-def"],
    "see" : ["-see", "-view"],
    "profile" : ["-profile", "-prof"],

    "text" : ["-text", "-t"],
    "photo" : ["-photo", "-p"],
    "audio" : ["-audio", "-a"],
    "document" : ["-document", "-doc", "-d"],
    "video" : ["-video", "-v"],
    "exception" : ["-exception", "-exc"],

    "token" : ["-token"],
    "to_chat" : ["-to", "-chat"],
    "mthread" : ["-mt_id"],
    "pmode" : ["-parse"],
    "webprev" : ["-no_webp_preview"],
    "dino" : ["-silent"],
    "protcont" : ["-protect_content"],
    "reply_id" : ["-reply"],
    "reply_anyway" : ["-reply_anyway"],
    "mex_id" : ["-message"],
    "from_chat" : ["-from"],
    "caption" : ["-caption"],
    "spoiler" : ["-spoiler"],
    "duration" : ["-duration"],
    "performer" : ["-performer"],
    "title" : ["-title"],
    "thumbnail" : ["-thumb_path"],
    "typedetect" : ["-no_ctype_det"],
    "width" : ["-width"],
    "height" : ["-height"],
    "streaming" : ["-streaming"]
}

SHORTCUTS = ["webprev", "dino", "protcont", "reply_anyway", "spoiler", "typedetect", "streaming"]

PARAMS_EXPLANATION = {
    "token"         : f"{str(PARAMETERS['token']).replace(',', ' |')} <str> : API token of the bot to use.",
    "to_chat"       : f"{str(PARAMETERS['to_chat']).replace(',', ' |')} <int> : chat to send the message to.",
    "mthread"       : f"{str(PARAMETERS['mthread']).replace(',', ' |')} <int> : Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.",
    "pmode"         : f"{str(PARAMETERS['pmode']).replace(',', ' |')} <str> : Mode for parsing entities in the message text/caption. See site for more details.",
    "webprev"       : f"{str(PARAMETERS['webprev']).replace(',', ' |')} : <bool> : Disables link previews for links in this message.",
    "dino"          : f"{str(PARAMETERS['dino']).replace(',', ' |')} <bool> : Sends the message silently. Users will receive a notification with no sound.",
    "protcont"      : f"{str(PARAMETERS['protcont']).replace(',', ' |')} <bool> : Protects the contents of the sent message from forwarding and saving.",
    "reply_id"      : f"{str(PARAMETERS['reply_id']).replace(',', ' |')} <int> : If the message is a reply, ID of the original message.",
    "reply_anyway"  : f"{str(PARAMETERS['reply_anyway']).replace(',', ' |')} <bool> : Pass True if the message should be sent even if the specified replied-to message is not found.",
    "mex_id"        : f"{str(PARAMETERS['mex_id']).replace(',', ' |')} <int> : the message to copy/forward.",
    "from_chat"     : f"{str(PARAMETERS['from_chat']).replace(',', ' |')} <int> : chat_id of the message to copy/forward.",
    "caption"       : f"{str(PARAMETERS['caption']).replace(',', ' |')} <str> : Caption, 0-1024 characters after entities parsing. If not specified, the original caption is kept.",
    "spoiler"       : f"{str(PARAMETERS['spoiler']).replace(',', ' |')} <bool> : Pass True if the file needs to be covered with a spoiler animation.",
    "duration"      : f"{str(PARAMETERS['duration']).replace(',', ' |')} <double> : Duration in seconds.",
    "performer"     : f"{str(PARAMETERS['performer']).replace(',', ' |')} <str> : Performer.",
    "title"         : f"{str(PARAMETERS['title']).replace(',', ' |')} <str> : Title.",
    "thumbnail"     : f"{str(PARAMETERS['thumbnail']).replace(',', ' |')} <path> : Path of the Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320.",
    "typedetect"    : f"{str(PARAMETERS['typedetect']).replace(',', ' |')} <bool> : Disables automatic server-side content type detection for files uploaded using multipart/form-data.",
    "width"         : f"{str(PARAMETERS['width']).replace(',', ' |')} <int> : Video/Animation width.",
    "height"        : f"{str(PARAMETERS['height']).replace(',', ' |')} <int> : Video/Animation height.",
    "streaming"     : f"{str(PARAMETERS['streaming']).replace(',', ' |')} <bool> : If the video is suitable for streaming."
}

EXPLANATION = {

    "help"       : f"""{str(PARAMETERS['help']).replace(',', ' |')} : View notify options.
    => If followed by a {ALIAS} option prints the explanation of that parameter.""",

    "version"    : f"{str(PARAMETERS['version']).replace(',', ' |')} : View notify2 version.",

    "update"     : f"""{str(PARAMETERS['update']).replace(',', ' |')} : Update to latest stable version.
    => If followed by a version (es: {VERSION}) downloads and installs that specific version.
    => If followed by {str(PARAMETERS['dev']).replace(',', ' |')} update to latest non-stable version.""",

    "uninstall"  : f"{str(PARAMETERS['uninstall']).replace(',', ' |')} : Uninstalls notify2.",

    "config"     : f"""{str(PARAMETERS['config']).replace(',', ' |')} : View the location of the configuration file.
    => You can add one of these options:
        => {str(PARAMETERS['add']).replace(',', ' |')} <profile_name> {str(PARAMETERS['token']).replace(',', ' |')} <API_bot_token> [<profile_options>]* : Create a new profile in the configuration file with the name <profile_name> and with the API token <API_bot_token>.
        => {str(PARAMETERS['remove']).replace(',', ' |')} <profile_name> : Remove the profile specified from the configuration file.
        => {str(PARAMETERS['edit']).replace(',', ' |')} <profile_name> [<profile_options>]+ : Edit the profile specified from the configuration file.
        => {str(PARAMETERS['set']).replace(',', ' |')} <profile_name> : Set the profile specified as the default in the configuration file.
        => {str(PARAMETERS['see']).replace(',', ' |')} : View the configuration file content.
        
    => profile_options:
        => {PARAMS_EXPLANATION['from_chat']}
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['webprev']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_anyway']}
        => {PARAMS_EXPLANATION['pmode']}""",

    "profile"    : f"""{str(PARAMETERS['profile']).replace(',', ' |')} [<profile_options>]+ : Used optionally in pair with sending messages to manually choose a profile or specify profile options.
    => profile_options:
        => profile_name : If specified must be the first option. The profile to use from the configuration file.
        => {PARAMS_EXPLANATION['token']}
        => {PARAMS_EXPLANATION['from_chat']}
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['webprev']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_anyway']}
        => {PARAMS_EXPLANATION['pmode']}""",
    
    "text"       : f"""{str(PARAMETERS['text']).replace(',', ' |')} <text/file> [<text_params>]* : Sends a text message specified by text or path to the file to read.
    => text_params:
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['mthread']}
        => {PARAMS_EXPLANATION['pmode']}
        => {PARAMS_EXPLANATION['webprev']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_id']}
        => {PARAMS_EXPLANATION['reply_anyway']}""",

    "photo"      : f"""{str(PARAMETERS['photo']).replace(',', ' |')} <file> [<photo_params>]* : Sends the photo specified by the path.
    => photo_params:
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['mthread']}
        => {PARAMS_EXPLANATION['caption']}
        => {PARAMS_EXPLANATION['pmode']}
        => {PARAMS_EXPLANATION['spoiler']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_id']}
        => {PARAMS_EXPLANATION['reply_anyway']}""",

    "audio"      : f"""{str(PARAMETERS['audio']).replace(',', ' |')} <file> [<audio_params>]* : Sends the audio specified by the path.
    => audio_params:
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['mthread']}
        => {PARAMS_EXPLANATION['caption']}
        => {PARAMS_EXPLANATION['pmode']}
        => {PARAMS_EXPLANATION['duration']}
        => {PARAMS_EXPLANATION['performer']}
        => {PARAMS_EXPLANATION['title']}
        => {PARAMS_EXPLANATION['thumbnail']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_id']}
        => {PARAMS_EXPLANATION['reply_anyway']}""",

    "document"   : f"""{str(PARAMETERS['document']).replace(',', ' |')} <file> [<doc_params>]* : Sends the document specified by the path.
    => doc_params:
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['mthread']}
        => {PARAMS_EXPLANATION['thumbnail']}
        => {PARAMS_EXPLANATION['caption']}
        => {PARAMS_EXPLANATION['pmode']}
        => {PARAMS_EXPLANATION['typedetect']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_id']}
        => {PARAMS_EXPLANATION['reply_anyway']}""",

    "video"      : f"""{str(PARAMETERS['video']).replace(',', ' |')} <file> [<video_params>]* : Sends the video specified by the path.
    => video_params:
        => {PARAMS_EXPLANATION['to_chat']}
        => {PARAMS_EXPLANATION['mthread']}
        => {PARAMS_EXPLANATION['width']}
        => {PARAMS_EXPLANATION['height']}
        => {PARAMS_EXPLANATION['thumbnail']}
        => {PARAMS_EXPLANATION['caption']}
        => {PARAMS_EXPLANATION['pmode']}
        => {PARAMS_EXPLANATION['spoiler']}
        => {PARAMS_EXPLANATION['streaming']}
        => {PARAMS_EXPLANATION['dino']}
        => {PARAMS_EXPLANATION['protcont']}
        => {PARAMS_EXPLANATION['reply_id']}
        => {PARAMS_EXPLANATION['reply_anyway']}""",

    "exception"  : f"""{str(PARAMETERS['exception']).replace(',', ' |')} <text> [<exception_params>]* : Sends an exception with the text specified.
    => exception_params:
        => {PARAMS_EXPLANATION['to_chat']}""",

}

#endregion


















def main():
    
    #ntf_info("Prova di un messaggio di info\nQuesta è una seconda riga...")
    #ntf_input("Inserisci una parola e me la dimenticherò")
    #ntf_warn("Prova di un warning\nQuesta è una seconda riga...", loc=__file__, line=sys._getframe().f_lineno)
    #ntf_error("Prova di un errore\nQuesta è una seconda riga...", loc=__file__, line=sys._getframe().f_lineno)

    parser = arg_parser()
    
    parser.add_param()

    parsed = parser.parse(sys.argv)
    print(json.dumps(parsed, indent=4))
            
    print(OS)

if __name__ == "__main__":
    main()