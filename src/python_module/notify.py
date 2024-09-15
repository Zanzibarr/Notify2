import sys

sys.dont_write_bytecode = True
import json
import os
import subprocess
import time

import numpy as np

sys.path.append(f"{os.path.dirname(__file__)}/../")
import notify_utils as utils

# ---------------------------------------------------------------
# region                  CONFIGURATIONS                        -
# ---------------------------------------------------------------


def write_conf_profile(
    name,
    token,
    from_chat_id="",
    to_chat_id="",
    disable_web_page_preview="",
    disable_notification="",
    protect_content="",
    allow_sending_without_reply="",
    parse_mode="",
):
    """Method to set a profile in the configuration file for future use

    - name : str -> Unique name of the profile, can't have more profiles with the same name. If passed a name of a profile already in the configuration, that profile is gonna be modified with this parameters
    - token : str -> The token associated to the bot to use in this profile
    - from_chat_id : int/str (optional) -> Chat id to use when searching for a message to copy/forward/...
    - to_chat_id : int/str (optional) -> Chat id to use when sending/editing messages
    - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message
    - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
    - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
    - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found
    - parse_mode : str (optional) -> Mode for parsing entities in the message text. See the site for more details.
    """

    if (
        token != ""
        and not utils.requests_post(
            f"https://api.telegram.org/bot{token}/getMe"
        ).json()["ok"]
    ):
        utils.ntf_exc("NOTIFY_EXCEPTION: Invalid token.")

    if not os.path.exists(utils.CONFIG_PATH):
        subprocess.run(["touch", utils.CONFIG_PATH])
        with open(utils.CONFIG_PATH, "w") as f:
            f.write(json.dumps({"def": "default", "profiles": {}}, indent=4))

    with open(utils.CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    profile = configuration["profiles"][name] = {}
    profile["token"] = token
    profile["from_chat_id"] = from_chat_id
    profile["to_chat_id"] = to_chat_id
    profile["disable_web_page_preview"] = disable_web_page_preview
    profile["disable_notification"] = disable_notification
    profile["protect_content"] = protect_content
    profile["allow_sending_without_reply"] = allow_sending_without_reply
    profile["parse_mode"] = parse_mode

    with open(utils.CONFIG_PATH, "w") as f:
        f.write(json.dumps(configuration, indent=4))


def edit_conf_profile(
    name,
    token="",
    from_chat_id="",
    to_chat_id="",
    disable_web_page_preview="",
    disable_notification="",
    protect_content="",
    allow_sending_without_reply="",
    parse_mode="",
):
    """Method to set a profile in the configuration file for future use

    - name : str -> Unique name of the profile to edit, if the name doesn't exist in the configuration file an exception will be raised
    - token : str (optional) -> The token associated to the bot to use in this profile
    - from_chat_id : int/str (optional) -> Chat id to use when searching for a message to copy/forward/...
    - to_chat_id : int/str (optional) -> Chat id to use when sending/editing messages
    - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message
    - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
    - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
    - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found
    - parse_mode : str (optional) -> Mode for parsing entities in the message text. See the site for more details.
    """

    if (
        token != ""
        and not utils.requests_post(
            f"https://api.telegram.org/bot{token}/getMe"
        ).json()["ok"]
    ):
        utils.ntf_exc("NOTIFY_EXCEPTION: Invalid token.")

    if not os.path.exists(utils.CONFIG_PATH):
        utils.ntf_exc("NOTIFY_EXCEPTION: Configuration file not found.")

    with open(utils.CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    if name not in configuration["profiles"]:
        utils.ntf_exc(
            "NOTIFY_EXCEPTION: The specified name was not in the list of profiles in the configuration file."
        )

    profile = configuration["profiles"][name]
    if token != "":
        profile["token"] = token
    if from_chat_id != "":
        profile["from_chat_id"] = from_chat_id
    if to_chat_id != "":
        profile["to_chat_id"] = to_chat_id
    if disable_web_page_preview != "":
        profile["disable_web_page_preview"] = disable_web_page_preview
    if disable_notification != "":
        profile["disable_notification"] = disable_notification
    if protect_content != "":
        profile["protect_content"] = protect_content
    if allow_sending_without_reply != "":
        profile["allow_sending_without_reply"] = allow_sending_without_reply
    if parse_mode != "":
        profile["parse_mode"] = parse_mode

    with open(utils.CONFIG_PATH, "w") as f:
        f.write(json.dumps(configuration, indent=4))


def write_conf_profile_from_dict(name, profile):
    """Method to set a profile in the configuration file for future use

    - name : str -> Unique name of the profile, can't have more profiles with the same name. If passed a name of a profile already in the configuration, that profile is gonna be modified with this parameters
    - profile : dict -> Dictionary of the profile to write. The profile must have the following fields:
            - "token" : str
            - "from_chat_id" : int/str (optional)
            - "to_chat_id" : int/str (optional)
            - "disable_web_page_preview" : bool (optional)
            - "disable_notification" : bool (optional)
            - "protect_content" : bool (optional)
            - "allow_sending_without_reply" : bool (optional)
            - "parse_mode" : str (optional)
    """

    if "token" not in profile:
        utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'token' in the profile.")
    if not utils.requests_post(
        f"https://api.telegram.org/bot{profile['token']}/getMe"
    ).json()["ok"]:
        utils.ntf_exc("NOTIFY_EXCEPTION: Invalid token.")

    if not os.path.exists(utils.CONFIG_PATH):
        subprocess.run(["touch", utils.CONFIG_PATH])
        with open(utils.CONFIG_PATH, "w") as f:
            f.write({"def": "default", "profiles": {}})

    with open(utils.CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    if "from_chat_id" not in profile:
        utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'from_chat_id' in the profile.")
    if "to_chat_id" not in profile:
        utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'to_chat_id' in the profile.")
    if "disable_web_page_preview" not in profile:
        utils.ntf_exc(
            "NOTIFY_EXCEPTION: Missing 'disable_web_page_preview' in the profile."
        )
    if "disable_notification" not in profile:
        utils.ntf_exc(
            "NOTIFY_EXCEPTION: Missing 'disable_notification' in the profile."
        )
    if "protect_content" not in profile:
        utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'protect_content' in the profile.")
    if "allow_sending_without_reply" not in profile:
        utils.ntf_exc(
            "NOTIFY_EXCEPTION: Missing 'allow_sending_without_reply' in the profile."
        )
    if "parse_mode" not in profile:
        utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'parse_mode' in the profile.")

    configuration["profiles"][name] = profile

    with open(utils.CONFIG_PATH, "w") as f:
        f.write(json.dumps(configuration, indent=4))


def set_default_profile(name):
    """Method to set the default profile in the configuration file

    - name : str -> name of the profile to set as default"""

    with open(utils.CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    if name not in configuration["profiles"]:
        utils.ntf_exc(
            "NOTIFY_EXCEPTION: The specified name was not in the list of profiles in the configuration file."
        )

    configuration["def"] = name

    with open(utils.CONFIG_PATH, "w") as f:
        f.write(json.dumps(configuration, indent=4))


def remove_profile(name):
    """Method to remove a profile from the configuration file

    - name : str -> name of the profile to remove. If the profile isn't found, nothing happens
    """

    with open(utils.CONFIG_PATH, "r") as f:
        configuration = json.loads(f.read())

    if name in configuration["profiles"]:
        configuration["profiles"].pop(name)
    else:
        return

    with open(utils.CONFIG_PATH, "w") as f:
        f.write(json.dumps(configuration, indent=4))


def get_profiles():
    """Method to get the dict of the profiles saved in the configuration file"""

    with open(utils.CONFIG_PATH, "r") as f:
        return json.loads(f.read())["profiles"]


# endregion


class bot:

    class __progress_bar:

        active = False
        title = ""
        text = ""
        time = 0
        time_elapsed = 0
        time_per_step = [0]
        steps = 0
        missing_steps = 0
        chat_id = ""
        message_id = ""

    __def_url = ""
    __env = False
    __send = True
    __profile = {
        "token": "",
        "from_chat_id": "",
        "to_chat_id": "",
        "disable_web_page_preview": "",
        "disable_notification": "",
        "protect_content": "",
        "allow_sending_without_reply": "",
        "parse_mode": "",
    }

    __pb = __progress_bar()

    def __init__(self, token="", profile="", set_on=True):
        """Set the environment for the bot

        - token : str (limited) -> token of the bot to use. Either the token or the profile must be specified. If both are specified, the token will overrite the one in the profile.
        - profile : str (limited) -> The name of the profile (in the configuration file) to associate to the bot. Either the token or the profile must be specified
        - set_on : bool (optional) -> True to keep/turn the bot on after this operation, False to keep/turn off the bot after this operation
        """

        self.load_profile(token=token, name=profile)

        self.__def_url = f"https://api.telegram.org/bot{self.__profile['token']}"
        self.__env = True

        if set_on:
            self.on()
        else:
            self.off()

    # ---------------------------------------------------------------
    # region                      PROFILES                          -
    # ---------------------------------------------------------------

    def edit_profile(
        self,
        token="",
        from_chat_id="",
        to_chat_id="",
        disable_web_page_preview="",
        disable_notification="",
        protect_content="",
        allow_sending_without_reply="",
        parse_mode="",
    ):
        """Method to edit the profile of this bot

        - token : str (optional) -> The token associated to the bot to use in this profile
        - from_chat_id : int/str (optional) -> Chat id to use when searching for a message to copy/forward/...
        - to_chat_id : int/str (optional) -> Chat id to use when sending/editing messages
        - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found
        """

        if (
            token != ""
            and not utils.requests_post(
                f"https://api.telegram.org/bot{token}/getMe"
            ).json()["ok"]
        ):
            utils.ntf_exc("NOTIFY_EXCEPTION: Invalid token.")

        if token != "":
            self.__profile["token"] = token
            self.__def_url = f"https://api.telegram.org/bot{self.__profile['token']}"
        if from_chat_id != "":
            self.__profile["from_chat_id"] = from_chat_id
        if to_chat_id != "":
            self.__profile["to_chat_id"] = to_chat_id
        if disable_web_page_preview != "":
            self.__profile["disable_web_page_preview"] = disable_web_page_preview
        if disable_notification != "":
            self.__profile["disable_notification"] = disable_notification
        if protect_content != "":
            self.__profile["protect_content"] = protect_content
        if allow_sending_without_reply != "":
            self.__profile["allow_sending_without_reply"] = allow_sending_without_reply
        if parse_mode != "":
            self.__profile["parse_mode"] = parse_mode

    def set_profile_from_dict(self, profile):
        """Method to set the profile of the bot

        - profile : dict -> Dictionary of the profile to set. The profile must have the following fields:
                - "token" : str
                - "from_chat_id" : int/str (optional)
                - "to_chat_id" : int/str (optional)
                - "disable_web_page_preview" : bool (optional)
                - "disable_notification" : bool (optional)
                - "protect_content" : bool (optional)
                - "allow_sending_without_reply" : bool (optional)
                - "parse_mode" : str (optional) -> Mode for parsing entities in the message text. See the site for more details.
        """

        if "token" not in profile:
            utils.ntf_exc("NOTIFY_EXCEPTION: Missing field 'token' in the profile.")
        if profile["token"] == "":
            utils.ntf_warn("NOTIFY_EXCEPTION: Missing token in the profile.")
        if not utils.requests_post(
            f"https://api.telegram.org/bot{profile['token']}/getMe"
        ).json()["ok"]:
            utils.ntf_warn("NOTIFY_EXCEPTION: Invalid token.")

        if "from_chat_id" not in profile:
            utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'from_chat_id' in the profile.")
        if "to_chat_id" not in profile:
            utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'to_chat_id' in the profile.")
        if "disable_web_page_preview" not in profile:
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Missing 'disable_web_page_preview' in the profile."
            )
        if "disable_notification" not in profile:
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Missing 'disable_notification' in the profile."
            )
        if "protect_content" not in profile:
            utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'protect_content' in the profile.")
        if "allow_sending_without_reply" not in profile:
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Missing 'allow_sending_without_reply' in the profile."
            )
        if "parse_mode" not in profile:
            utils.ntf_exc("NOTIFY_EXCEPTION: Missing 'parse_mode' in the profile.")

        self.__profile["token"] = profile["token"]
        self.__profile["from_chat_id"] = profile["from_chat_id"]
        self.__profile["to_chat_id"] = profile["to_chat_id"]
        self.__profile["disable_web_page_preview"] = profile["disable_web_page_preview"]
        self.__profile["disable_notification"] = profile["disable_notification"]
        self.__profile["protect_content"] = profile["protect_content"]
        self.__profile["allow_sending_without_reply"] = profile[
            "allow_sending_without_reply"
        ]
        self.__profile["parse_mode"] = profile["parse_mode"]

        self.__def_url = f"https://api.telegram.org/bot{self.__profile['token']}"

    def load_profile(self, token="", name=""):
        """Method to associate a bot to a profile for faster configuration

        - token : str (limited) -> The token to use. Either the token or the name must be specified. If both are specified, the token will overrite the one in the profile.
        - name : str (limited) -> Unique name of the profile to use. Either the token or the name must be specified.
        """

        with open(utils.CONFIG_PATH, "r") as f:
            configuration = json.loads(f.read())

        if token == "" and name == "":
            self.set_profile_from_dict(
                profile=configuration["profiles"][configuration["def"]]
            )  # ---/---

        elif token == "" and name != "":
            if name not in configuration["profiles"]:
                utils.ntf_warn(
                    f"the name {name} of the profile to load isn't associated to any profile.\nNo profile loaded."
                )
                return  # ---/no match
            if "token" not in configuration["profiles"][name]:
                utils.ntf_warn("NOTIFY_EXCEPTION: Configuration file corrupted.")
            self.set_profile_from_dict(
                profile=configuration["profiles"][name]
            )  # ---/valid
            if not utils.requests_post(
                f"https://api.telegram.org/bot{self.__profile['token']}/getMe"
            ).json()["ok"]:
                utils.ntf_warn(
                    f"the token inside the profile {name} is invalid, profile loaded anyways.\nConsider changing it or specify a new token."
                )  # ---/invalid

        elif name == "":
            if not utils.requests_post(
                f"https://api.telegram.org/bot{token}/getMe"
            ).json()["ok"]:
                utils.ntf_warn("NOTIFY_EXCEPTION: Invalid token.")  # invalid/---
            self.__profile["token"] = token  # valid/---

        elif name != "":
            valid_token = utils.requests_post(
                f"https://api.telegram.org/bot{token}/getMe"
            ).json()["ok"]
            if name not in configuration["profiles"]:
                utils.ntf_warn(
                    f"the name {name} of the profile to load isn't associated to any profile. Loading only the token specified."
                )
                if not valid_token:
                    utils.ntf_warn(
                        "NOTIFY_EXCEPTION: Invalid token."
                    )  # invalid/no match
                self.__profile["token"] = token  # valid/no match
            else:
                if "token" not in configuration["profiles"][name]:
                    utils.ntf_warn("NOTIFY_EXCEPTION: Configuration file corrupted.")
                self.set_profile_from_dict(profile=configuration[name])
                valid_profile = utils.requests_post(
                    f"https://api.telegram.org/bot{self.__profile['token']}/getMe"
                ).json()["ok"]
                if not valid_token:
                    if not valid_profile:
                        utils.ntf_warn(
                            "NOTIFY_EXCEPTION: Both tokens (the one specified and the one in the profile) are invalid."
                        )  # invalid/invalid
                    utils.ntf_warn(
                        f"the token specified is invalid.\nUsing the {name} profile token."
                    )  # invalid/valid
                else:
                    if not valid_profile:
                        utils.ntf_warn(
                            f"the token inside the profile {name} is invalid.\nRest of the profile loaded successfully, used token specified."
                        )
                    self.__profile["token"] = token  # valid/valid or invalid

    def save_profile(self, name):
        """Method to save on the configuration file the profile associated to this bot

        - name : str -> The name to give to the profile"""

        write_conf_profile_from_dict(name, self.__profile)

    # endregion

    # ---------------------------------------------------------------
    # region                    UTILITIES                           -
    # ---------------------------------------------------------------

    def send_exception(self, text="", chat_id=""):
        """Sends a text message in the exception format

        - text : str (optional) -> Additional text to write in the message
        - chat_id : int/str (optional) -> chat_id to send the message to (If not specified, using the default one)
        """

        message = "\U00002757 *EXCEPTION CAPTURED* \U00002757"
        if len(text) > 0:
            message = message + "\n" + text

        return self.send_message_by_text(
            message, chat_id=chat_id, disable_notification=False, parse_mode="Markdown"
        )

    def create_progress_bar(self, steps, title="", text="", chat_id=""):
        """Creates and send the initial progress bar (works only on for loops with a known number of steps)

        - steps : int -> Number of steps of the progress bar
        - title : str (optional) -> Title of the progress bar
        - text : str (optional) -> Additional text of the progress bar
        - chat_id : int/str (optional) -> chat_id to send the message to (If not specified, using the default one)
        """

        message = f"*{title}*" + "\n" + text + "\n"
        message = message + "\\[" + "\u2581" * 20 + "]\n"
        message = message + f"Time elapsed: 0s/--"

        r = self.send_message_by_text(message, chat_id=chat_id, parse_mode="Markdown")

        self.__pb.active = True
        self.__pb.title = title
        self.__pb.text = text
        self.__pb.time = time.time()
        self.__pb.time_elapsed = 0
        self.__pb.time_per_step = [0]
        self.__pb.steps = steps
        self.__pb.missing_steps = steps
        self.__pb.chat_id = chat_id
        self.__pb.message_id = r["result"]["message_id"]

        return r

    def update_progress_bar(self):
        """Updates of 1 step the progress bar (works only on for loops with a known number of steps)"""

        if not self.__pb.active:
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Progress bar hasn't been created or has already terminated."
            )

        self.__pb.missing_steps = self.__pb.missing_steps - 1

        self.__pb.time_per_step.append(
            time.time() - self.__pb.time - self.__pb.time_elapsed
        )
        self.__pb.time_elapsed = time.time() - self.__pb.time

        message = f"*{self.__pb.title}*" + "\n" + self.__pb.text + "\n"
        completed_steps = int(
            np.floor((1 - self.__pb.missing_steps / self.__pb.steps) * 20)
        )
        message = (
            message
            + "\\["
            + "\u2588" * completed_steps
            + "\u2581" * (20 - completed_steps)
            + "]\n"
        )

        message = (
            message
            + f"Time elapsed: {utils.format_time(self.__pb.time_elapsed)}/{utils.format_time(self.__pb.time_elapsed + self.__pb.missing_steps * np.average(self.__pb.time_per_step))}"
        )

        r = self.edit_message_text(
            message,
            message_id=self.__pb.message_id,
            chat_id=self.__pb.chat_id,
            parse_mode="Markdown",
        )

        if self.__pb.missing_steps == 0:
            self.__pb.active = False

        return r

    def conclude_progress_bar(self):
        """Concludes a progress bar (use it after the end of the for loop)"""

        message = f"*{self.__pb.title}*" + "\n" + self.__pb.text + "\n"
        message = (
            message + "\nCompleted in " + utils.format_time(self.__pb.time_elapsed)
        )

        self.__pb.active = False

        return self.edit_message_text(
            message,
            message_id=self.__pb.message_id,
            chat_id=self.__pb.chat_id,
            parse_mode="Markdown",
        )

    # endregion

    # ---------------------------------------------------------------
    # region                    TELEGRAM API                        -
    # ---------------------------------------------------------------

    def on(self):
        """Turns on the bot"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")

        self.__send = True

    def off(self):
        """Turns off the bot"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")

        self.__send = False

    def send_message_by_text(
        self,
        text,
        chat_id="",
        message_thread_id="",
        parse_mode="",
        disable_web_page_preview="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send text messages. On success, the sent Message is returned.

        - text : str -> the text to write (can be formatted with MD, see the site for more info)
        - chat_id : int/str (optional) -> chat to send the message to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - parse_mode : str (optional) -> Mode for parsing entities in the message text. See site for more details.
        - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        See the site for formatting options.
        Refer to https://core.telegram.org/bots/api (sendMessage) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_web_page_preview == "":
            disable_web_page_preview = self.__profile["disable_web_page_preview"]
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("sendMessage", data=data).json()

    def send_message_by_file(
        self,
        file_path,
        chat_id="",
        message_thread_id="",
        parse_mode="",
        disable_web_page_preview="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send text messages. On success, the sent Message is returned.

        - file_path : str -> path to the text file to read
        - chat_id : int/str (optional) -> chat to send the message to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - parse_mode : str (optional) -> Mode for parsing entities in the message text. See site for more details.
        - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        See the site for formatting options
        Refer to https://core.telegram.org/bots/api (sendMessage) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_web_page_preview == "":
            disable_web_page_preview = self.__profile["disable_web_page_preview"]
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        with open(file_path, "r") as f:
            text = f.read()

        return self.send_message_by_text(
            text=text,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
        )

    def forward_message(
        self,
        message_id,
        chat_id,
        from_chat_id="",
        message_thread_id="",
        disable_notification="",
        protect_content="",
    ):
        """Use this method to forward messages of any kind. Service messages can't be forwarded. On success, the sent Message is returned.

        - message_id : int -> the message to forward
        - chat_id : int/str -> chat_id recieving the message
        - from_chat_id : int/str (optional) -> chat_id of the message to forward. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the forwarded message from forwarding and saving

        Refer to https://core.telegram.org/bots/api (forwardMessage) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if from_chat_id == "":
            from_chat_id = self.__profile["from_chat_id"]
        if from_chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a from_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "from_chat_id": from_chat_id,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "message_id": message_id,
        }

        return self.__request_format("forwardMessage", data=data).json()

    def copy_message(
        self,
        message_id,
        chat_id,
        from_chat_id="",
        message_thread_id="",
        caption="",
        parse_mode="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to copy messages of any kind. Service messages and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.

        - message_id : int -> the message to copy
        - chat_id : int/str -> chat id recieving the message
        - from_chat_id : int/str (optional) -> chat_id of the message to forward. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - caption : str (optional) -> New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept
        - parse_mode : str (optional) -> Mode for parsing entities in the new caption. See site for more details.
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the forwarded message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        Refer to https://core.telegram.org/bots/api (copyMessage) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if from_chat_id == "":
            from_chat_id = self.__profile["from_chat_id"]
        if from_chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a from_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("copyMessage", data=data).json()

    def send_photo_by_path(
        self,
        file_path,
        chat_id="",
        message_thread_id="",
        caption="",
        parse_mode="",
        has_spoiler="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send photos. On success, the sent Message is returned.

        - file_path : str -> Path to the photo to send
        - chat_id : int/str (optional) -> chat_id of the chat to send the photo to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - caption : str (optional) -> Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
        - parse_mode : str (optional) -> Mode for parsing entities in the photo caption. See the site for more details.
        - has_spoiler : bool (optional) -> Pass True if the photo needs to be covered with a spoiler animation
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        Refer to https://core.telegram.org/bots/api (sendPhoto) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        if not os.path.exists(file_path):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {file_path} doesn't lead to any file."
            )

        files = {"photo": open(file_path, "rb")}

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "has_spoiler": has_spoiler,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("sendPhoto", data=data, files=files).json()

    def send_audio_by_path(
        self,
        file_path,
        chat_id="",
        message_thread_id="",
        caption="",
        parse_mode="",
        duration="",
        performer="",
        title="",
        thumbnail="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.

        For sending voice messages, use the sendVoice method instead.

        - file_path : str -> Path to the audio to send
        - chat_id : int/str (optional) -> chat_id of the chat to send the audio to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - caption : str (optional) -> Audio caption (may also be used when resending audios by file_id), 0-1024 characters after entities parsing
        - parse_mode : str (optional) -> Mode for parsing entities in the audio caption. See the site for more details.
        - duration : int (optional) -> Duration of the audio in seconds
        - performer : str (optional) -> Performer
        - title : str (optional) -> Track name
        - thumbnail : str (optional) -> Path of the Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. More information in the site.
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        Refer to https://core.telegram.org/bots/api (sendAudio) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        if not os.path.exists(file_path):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {file_path} doesn't lead to any file."
            )
        if thumbnail != "" and not os.path.exists(thumbnail):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {thumbnail} doesn't lead to any file."
            )

        files = {"audio": open(file_path, "rb")}
        if thumbnail != "":
            files["thumbnail"] = open(thumbnail, "rb")

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "duration": duration,
            "performer": performer,
            "title": title,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("sendAudio", data=data, files=files).json()

    def send_document_by_path(
        self,
        file_path,
        chat_id="",
        message_thread_id="",
        thumbnail="",
        caption="",
        parse_mode="",
        disable_content_type_detection="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.

        - file_path : str -> Path to the document to send
        - chat_id : int/str (optional) -> chat_id of the chat to send the document to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - thumbnail : str (optional) -> Path of the Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. More information in the site.
        - caption : str (optional) -> Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
        - parse_mode : str (optional) -> Mode for parsing entities in the document caption. See the site for more details.
        - disable_content_type_detection : bool (optional) -> Disables automatic server-side content type detection for files uploaded using multipart/form-data
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        Refer to https://core.telegram.org/bots/api (sendDocument) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        if not os.path.exists(file_path):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {file_path} doesn't lead to any file."
            )
        if thumbnail != "" and not os.path.exists(thumbnail):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {thumbnail} doesn't lead to any file."
            )

        files = {"document": open(file_path, "rb")}
        if thumbnail != "":
            files["thumbnail"] = open(thumbnail, "rb")

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "disable_content_type_detection": disable_content_type_detection,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("sendDocument", data=data, files=files).json()

    def send_video_by_path(
        self,
        file_path,
        chat_id="",
        message_thread_id="",
        duration="",
        width="",
        height="",
        thumbnail="",
        caption="",
        parse_mode="",
        has_spoiler="",
        supports_streaming="",
        disable_notification="",
        protect_content="",
        reply_to_message_id="",
        allow_sending_without_reply="",
    ):
        """Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.

        - file_path : str -> The path to the video to send
        - chat_id : int/str (optional) -> chat_id of the chat to send the video to. The default one is the one specified by the profile
        - message_thread_id : int (optional) -> Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        - duration : int (optional) -> Duration of sent video in seconds
        - width : int (optional) -> Video width
        - height : int (optional) -> Video height
        - thumbnail : str (optional) -> Path of the Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. More information in the site.
        - caption : str (optional) -> Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
        - parse_mode : str (optional) -> Mode for parsing entities in the video caption. See the site for more details.
        - has_spoiler : bool (optional) -> Pass True if the video needs to be covered with a spoiler animation
        - supports_streaming : bool (optional) -> Pass True if the uploaded video is suitable for streaming
        - disable_notification : bool (optional) -> Sends the message silently. Users will receive a notification with no sound.
        - protect_content : bool (optional) -> Protects the contents of the sent message from forwarding and saving
        - reply_to_message_id : int (optional) -> If the message is a reply, ID of the original message
        - allow_sending_without_reply : bool (optional) -> Pass True if the message should be sent even if the specified replied-to message is not found

        Refer to https://core.telegram.org/bots/api (sendVideo) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a to_chat_id in the profile or specify one as a parameter."
            )
        if disable_notification == "":
            disable_notification = self.__profile["disable_notification"]
        if protect_content == "":
            protect_content = self.__profile["protect_content"]
        if allow_sending_without_reply == "":
            allow_sending_without_reply = self.__profile["allow_sending_without_reply"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        if not os.path.exists(file_path):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {file_path} doesn't lead to any file."
            )
        if thumbnail != "" and not os.path.exists(thumbnail):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {thumbnail} doesn't lead to any file."
            )

        files = {"video": open(file_path, "rb")}
        if thumbnail != "":
            files["thumbnail"] = open(thumbnail, "rb")

        data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "duration": duration,
            "width": width,
            "height": height,
            "caption": caption,
            "parse_mode": parse_mode,
            "has_spoiler": has_spoiler,
            "supports_streaming": supports_streaming,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        return self.__request_format("sendVideo", data=data, files=files).json()

    def edit_message_text(
        self,
        text,
        chat_id="",
        message_id="",
        inline_message_id="",
        parse_mode="",
        disable_web_page_preview="",
    ):
        """Use this method to edit text and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        - text : str -> New text of the message, 1-4096 characters after entities parsing
        - chat_id : int/str (limited) -> Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (if not defined looks for the default one)
        - message_id : int (limited) -> Required if inline_message_id is not specified. Identifier of the message to edit
        - inline_message_id : str (limited) -> Required if chat_id and message_id are not specified. Identifier of the inline message
        - parse_mode : str (optional) -> Mode for parsing entities in the message text. See the site for more details.
        - disable_web_page_preview : bool (optional) -> Disables link previews for links in this message

        Refer to https://core.telegram.org/bots/api (editMessageText) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if inline_message_id == "":
            if chat_id == "":
                chat_id = self.__profile["to_chat_id"]
            if message_id == "" or chat_id == "":
                utils.ntf_exc(
                    "NOTIFY_EXCEPTION: If the inline_message_id is not defined, both chat_id (default counts) and message_id must be defined."
                )
        else:
            chat_id = ""
            message_id = ""
        if disable_web_page_preview == "":
            disable_web_page_preview = self.__profile["disable_web_page_preview"]
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }

        return self.__request_format("editMessageText", data=data).json()

    def edit_message_caption(
        self, caption, chat_id="", message_id="", inline_message_id="", parse_mode=""
    ):
        """Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        - caption : str -> New caption of the message, 0-1024 characters after entities parsing
        - chat_id : int/str (limited) -> Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (if not defined looks for the default one)
        - message_id : int (limited) -> Required if inline_message_id is not specified. Identifier of the message to edit
        - inline_message_id : str (limited) -> Required if chat_id and message_id are not specified. Identifier of the inline message
        - parse_mode : str (optional) -> Mode for parsing entities in the message caption. See the site for more details.

        Refer to https://core.telegram.org/bots/api (editMessageCaption) for more info
        """

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if inline_message_id == "":
            if chat_id == "":
                chat_id = self.__profile["to_chat_id"]
            if message_id == "" or chat_id == "":
                utils.ntf_exc(
                    "NOTIFY_EXCEPTION: If the inline_message_id is not defined, both chat_id (default counts) and message_id must be defined."
                )
        else:
            chat_id = ""
            message_id = ""
        if parse_mode == "":
            parse_mode = self.__profile["parse_mode"]

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "caption": caption,
            "parse_mode": parse_mode,
        }

        return self.__request_format("editMessageCaption", data=data).json()

    def edit_message_media(
        self, file_path, chat_id="", message_id="", inline_message_id=""
    ):
        """Use this method to edit animation, audio, document, photo, or video messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        - file_path : str -> The path to the media to send
        - chat_id : int/str (limited) -> Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (if not defined looks for the default one)
        - message_id : int (limited) -> Required if inline_message_id is not specified. Identifier of the message to edit
        - inline_message_id : str (limited) -> Required if chat_id and message_id are not specified. Identifier of the inline message

        Refer to https://core.telegram.org/bots/api (editMessageMedia) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if inline_message_id == "":
            if chat_id == "":
                chat_id = self.__profile["to_chat_id"]
            if message_id == "" or chat_id == "":
                utils.ntf_exc(
                    "NOTIFY_EXCEPTION: If the inline_message_id is not defined, both chat_id (default counts) and message_id must be defined."
                )
        else:
            chat_id = ""
            message_id = ""

        if not os.path.exists(file_path):
            utils.ntf_exc(
                f"NOTIFY_EXCEPTION: The file_path {file_path} doesn't lead to any file."
            )
        files = {"media": open(file_path, "rb")}

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
        }

        return self.__request_format("editMessageMedia", data=data, files=files).json()

    def delete_message(self, message_id, chat_id=""):
        """Use this method to delete a message, including service messages, with the following limitations:
        - A message can only be deleted if it was sent less than 48 hours ago.
        - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        - Bots can delete incoming messages in private chats.
        - Bots granted can_post_messages permissions can delete outgoing messages in channels.
        - If the bot is an administrator of a group, it can delete any message there.
        - If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.
        Returns True on success.

        - message_id : int -> Identifier of the message to delete
        - chat_id : int/str (optional) -> Unique identifier for the target chat or username of the target channel (if not defined looks for the default one)

        Refer to https://core.telegram.org/bots/api (deleteMessage) for more info"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")
        if not self.__send:
            return {}

        if chat_id == "":
            chat_id = self.__profile["to_chat_id"]
        if chat_id == "":
            utils.ntf_exc(
                "NOTIFY_EXCEPTION: Either set a chat_id in the profile or specify one as a parameter."
            )

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }

        return self.__request_format("deleteMessage", data=data).json()

    def __request_format(self, command, data={}, files=None):
        """Creates a request to the telegram API and returns the response

        - command : str -> the command to use
        - data : str -> the data to pass through"""

        if not self.__env:
            utils.ntf_exc("NOTIFY_EXCEPTION: constructor hasn't been called yet.")

        url = self.__def_url + "/" + command

        return utils.requests_post(url, data=data, files=files)

    # endregion
