# Slack Status Changer

Slack Status Changer changes Slack status by SSID or IP address.  
If you use this application, please authenticate from the link below first.  
https://nazboost.github.io/slack-status-changer/

## Requirement
As of February 26, 2019/02, it is not yet compatible with Windows.  
I recommend execute this application on Python 3.6 or higher on linux or mac.

## Usage
1. First, you should clone this repository.

2. Rename .env.sample file to .env and add value of `client_id` and `client_secret`.

3. Get temporary code to exchange with access token.  
   You can do it from the link above, or you can also use the `authorize()` function of [slack_status_changer.py](https://github.com/nazboost/slack-status-changer/blob/master/slack_status_changer.py).

4. Your temporary code is described in the parameter on the link.  
   Execute slack_status_changer.py with copying it, and input the code to exchange with the access token.  
   In order to omit the authentication from the next time on, add the access token to the `token` on .env file.

## Setting
Add SSID, status text and status emoji in [config.json](https://github.com/nazboost/slack-status-changer/blob/master/config.json) to make it correspond to your environment.