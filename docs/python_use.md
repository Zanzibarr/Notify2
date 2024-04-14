# Using notify as a python module
After following the [installation process](../readme.md#install), you should be able to use notify as a python module.  
Please note that all details about parameters of the methods can be found in the method's description (either read the source or use an IDE and read the method's description).  

## Index
- [Import and Access to the bot](#initial-steps)
    - [Import the module](#import-the-module)
    - [Access the bot](#access-the-telegram-bot)
- [Manage the configuration file](#managing-configuration-file)
    - [Setup a new profile](#setup-a-new-profile)
    - [Edit a profile](#edit-a-profile)
    - [Delete a profile](#delete-a-profile)
    - [View profiles](#view-possible-profiles)
- [Manage the bot's profile](#manage-bot-local-profile)
    - [Edit the bot's profile](#edit-the-bots-profile)
    - [Save the bot's profile to the configuration file](#save-current-profile-to-configuration-file)
- [Activate/Disable the bot](#activatedisable-the-bot)
- [Send messages](#send-messages)
    - [Send a text](#send-a-text-message-by-text)
    - [Send a text from a file](#send-a-text-message-by-file-content)
    - [Send a photo](#send-a-photo-by-path)
    - [Send an audio](#send-an-audio-by-path)
    - [Send a document](#send-a-document-by-path)
    - [Send a video](#send-a-video-by-path)
- [Utilities](#utilities)
    - [Send an exception type message](#send-an-exception)
    - [Send a progress bar](#progress-bar)
- [Edit messages](#edit-messages)
    - [Edit a message text](#edit-message-text)
    - [Edit a message caption](#edit-message-caption)
    - [Edit a message media](#edit-message-media)
- [Delete messages](#delete-a-message)

## Initial steps
### Import the module
```python
import notify
```

### Access the telegram bot
```python
bot = notify.bot(...)
```

You can use one of the following parameters to access the bot:  
- through your bot token
```python
bot = notify.bot(token="your_token")
```
- through a profile
```python
bot = notify.bot(profile="profile_name")
```
The profile you choose must be saved inside the ~/.zanz_notify_profiles configuration file.  
See [how to setup a profile through python](#setup-a-new-profile).  

If you specify both a token and a profile, first the specified profile will be loaded, then the token specified will take precedence over the token in the profile.  
If the token specified isn't a valid token, the token inside the profile will be used.  

You may want to disable the bot as you create it:
```python
bot = notify.bot(..., set_on=False)
```

## Managing configuration file
### Setup a new profile
You can create (or overwrite) a profile saved in the configuration file in one of two ways:
- you can specify manually the parameters you want to write in the profile
```python
notify.write_conf_profile(name="profile_name", token="your_token", ...)
```
- you can pass as a parameter a dict which needs to follow a strict structure (explained in the method's description)
```python
notify.write_conf_profile(name="profile_name", profile={...})
```

### Edit a profile
You can edit a profile from the configuration file as follows:
```python
notify.edit_conf_profile(name="profile_name"; ...)
```

### Delete a profile
You can remove a profile from the configuration file as follows:
```python
notify.remove_profile(name="profile_name")
```
If the profile specified doesn't exists, nothing happens.  

### View possible profiles
You can see which profiles are saved in the configuration file as follows:
```python
profiles = notify.get_profiles()
```
This method returns a dictionary with the profiles saved in the configuration file.  

## Manage bot local profile
After [accessing a bot](#access-the-telegram-bot), you can customize locally the profile associated to the bot (won't edit the configuration file).  
### Edit the bot's profile
You can edit the profile associated to the bot in one of the following ways:
- manually edit the profile parameters
```python
bot.edit_profile(...)
```
- specify a dict with the new profile parameters
```python
bot.set_profile_from_dict(profile={...})
```
- specify a profile from the configuration file
```python
bot.load_profile(name="profile_name")
```
If you wish you may also override the token by specifying a token:
```python
bot.load_profile(name="profile_name", token="your_token")
```
If the token is invalid, the one from the profile will be used.
### Save current profile to configuration file
You can save the profile used locally for the bot in the configuration file for future use:
```python
bot.save_profile(name="profile_name")
```
## Activate/Disable the bot
You can activate/disable the bot so that if it's disabled no message will be sent.  
- to activate the bot
```python
bot.on()
```
- to disable the bot
```python
bot.off()
```

## Send messages
Each of the following methods will return the response recieved from the telegram API.  
You have plenty of options to send messages through the bot:
### Send a text message by text
```python
bot.sent_message_by_text(text="text_message", ...)
```
### Send a text message by file content
```python
bot.send_message_by_file(file_path="path_to_file", ...)
```
### Send a photo by path
```python
bot.send_photo_by_path(file_path="path_to_file", ...)
```
### Send an audio by path
```python
bot.send_audio_by_path(file_path="path_to_file", ...)
```
### Send a document by path
```python
bot.send_document_by_path(file_path="path_to_file", ...)
```
### Send a video by path
```python
bot.send_video_by_path(file_path="path_to_file", ...)
```
### Forward a message
Please read the method's description to further understand how this method works.  
```python
bot.forward_message(message_id="message_id", chat_id="chat_id", ...)
```
### Copy a message
Please read the method's description to further understand how this method works.  
```python
bot.copy_message(message_id="message_id", chat_id="chat_id", ...)
```

## Utilities
Each of the following methods will return the response recieved from the telegram API.  
We've implemented some utilities that you might find useful:
### Send an exception
Sends a text message formatted in a way that it stands out as exception:
```python
bot.send_exception(...)
```
### Progress bar
Send an updating progress bar to keep track of the progress of your code.  
First you'll need to create the progress bar:
```python
bot.create_progress_bar(steps=n_steps, ...)
```
You'll need to specify the number of steps that the progress bar will need to complete.  
Then inside your loop you can update the progress bar:
```python
bot.update_progree_bar()
```
Then, once you're done, you can conclude the progress bar to show the final message:
```python
bot.conclude_progress_bar()
```

Example of usage:
```python
...

n_steps = 10
bot.create_progress_bar(steps=n_steps)

for i in range(n_steps):
    ...
    bot.update_progree_bar()

bot.conclude_progree_bar()

...
```

## Edit messages
Each of the following methods will return the response recieved from the telegram API.  
There are a few options to edit messages that has been sent:
### Edit message text
Please read the method's description to further understand how this method works.  
```python
bot.edit_message_text(text="new_text", chat_id="chat_id", message_id="message_id", ...)
```
### Edit message caption
Please read the method's description to further understand how this method works.  
```python
bot.edit_message_caption(caption="new_caption", chat_id="chat_id", message_id="message_id", ...)
```
### Edit message media
Please read the method's description to further understand how this method works.  
```python
bot.edit_message_media(file_path="new_media_file_path", chat_id="chat_id", message_id="message_id", ...)
```

## Delete a message
```python
bot.delete_message(message_id="message_id", ...)
```