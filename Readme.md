# Notify2

This python application will send messages through telegram to any chat you wish.  

Current version: 1.0.0  

Feel free to suggest us new improvements or to report any bug/problem by opening an [issue](https://github.com/Zanzibarr/Notify2/issues).


## Index
- [Requirements](#requirements)
- [Install](#install)
- [Using notify as a python module](#using-notify-as-a-python-module)
- [Update](#update)
- [Uninstall](#uninstall) 

## Requirements:
- Works for **UNIX based OS**
- Make sure you have the requests module installed for python  

_example code for linux:_
```shell
python3 pip -m install requests
```
- python3 is required for the update and the setup, if you wish to specify the location of your python you can change it manually:
```shell
nano $HOME/.notify2/notify_utils.py
```
_inside the notify_utils.py file:_
```python
...

PYTHON_VERSION = "/usr/bin/python3" #edit this (roughly at line 20)
...
```
- At some point in the installation process you will be asked to set a Telegram API token, you can follow [this tutorial](https://www.youtube.com/watch?v=aNmRNjME6mE) to create a new bot and recieve your token.
- You may also want to know your telegram chat id so that you can send messages to yourself: follow [this tutorial](https://www.youtube.com/watch?v=UPC5Ck1oU6k) and you will get the following message:
```json
{
    "update_id": "...",
    "message": {
        "message_id": "...",
        "from": {
            "..."
        },
        "chat": {
            "id": "CHAT_ID",
            "first_name": "...",
            "username": "...",
            "type": "..."
        },
        "date": "...",
        "text": "...",
        "entities": [
            "..."
        ]
    }
}
```
You will need the CHAT_ID field.  

## Install
To install you just need to download the [installer](https://www.zanzi.dev/Archive/notify/install.py):
```shell
curl https://www.zanzi.dev/Archive/notify/install.py -o ./install.py
```
Then run it:
```shell
python3 install.py
```

Once the installation has finished you can delete the installer.  

## Using notify as a python module
[Python lib use](docs/python_use.md)

## Update
To get the latest version of notify:
```shell
> notify -update
```

## Uninstall
To uninstall just run the command
```shell
> notify -uninstall
```
Uninstalling notify won't remove the configuration file located at
```shell
$HOME/.notify2_profiles
```
To remove those too just write
```shell
> rm $HOME/.notify2_profiles
```