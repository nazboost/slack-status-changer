"""
This script is a main script of Slack Status Changer.
Each user must authenticate and run this script locally.
"""

import json
import logging
import os
import subprocess
import sys
import time
import webbrowser

import requests
import schedule

import settings

# Load config
with open('config.json') as f:
    config = json.load(f)

# Logging settings
formatter = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)


def get_ssid(device_os='posix'):
    if device_os == 'posix':
        # Linux, Mac
        cmd = 'nmcli -t -f state,type,device,connection dev status'
        proc = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        stdouts = proc.stdout.read().decode('utf-8')
        stdouts_list = stdouts.split('\n')[:-1]

        outs = []
        for out in stdouts_list:
            outs.append(out.split(':'))

        for out in outs:
            if out[0] == '接続済み':
                if 'enp' in out[2]:
                    return out[3]
                elif 'wlp' in out[2]:
                    return out[3]
                else:
                    return 'no_connection'

    else:
        # TODO: Add how to know SSID or IP on Windows
        # Windows
        pass


def fetch_user_list():
    """
    Fetch id and name of all users.
    This function is ancillary and basically not used.
    """

    url = 'https://slack.com/api/users.list'

    payload = {
        'token': settings.token
    }

    res = requests.get(url=url, params=payload)

    for member in json.loads(res.text)['members']:
        print(member['id'], member['real_name'])


def change_slack_status(status_text, status_emoji):
    url = 'https://slack.com/api/users.profile.set'

    payload = {
        'token': os.environ['token'],
        # 'user': '',
        'profile': json.dumps({
            'status_text': status_text,
            'status_emoji': status_emoji
        })
    }

    res = requests.post(url=url, params=payload)


def authorize():
    """
    First step of get access token.
    This function is unnecessary when starting authentication from the web link.
    https://nazboost.github.io/slack-status-changer/
    """

    # https://api.slack.com/docs/oauth

    url = 'https://slack.com/oauth/authorize'

    payload = {
        'client_id': settings.client_id,
        'scope': 'users:read,users.profile:write',
        'redirect_uri': 'https://nazboost.github.io/slack-status-changer/',
        # 'state': '',
        # 'team': ''
    }

    res = requests.get(url=url, params=payload)
    webbrowser.open_new_tab(res.url)


def get_access_token(code):
    url = 'https://slack.com/api/oauth.access'

    payload = {
        'client_id': settings.client_id,
        'client_secret': settings.client_secret,
        'code': code,
        'redirect_uri': 'https://nazboost.github.io/slack-status-changer/',
        # 'single_channel': 'false'
    }

    res = requests.post(url=url, params=payload)
    res_dict = json.loads(res.text)

    if not res_dict['ok']:
        print('Failed to get access token')
        print(res_dict['error'])

    else:
        print('Successful getting access token')
        print('access_token:', res_dict['access_token'])

        return res_dict['access_token']


def job():
    # Execute  periodically
    ssid = get_ssid(device_os=os.name)

    if ssid == 'no_connection':
        pass

    elif ssid in list(config['ssid'].keys()):
        change_slack_status(
            status_text=config['ssid'][ssid]['status_text'],
            status_emoji=config['ssid'][ssid]['status_emoji']
        )

    else:
        change_slack_status(
            status_text='Out',
            status_emoji=':japan:'
        )

    print('Connect to', ssid)


if __name__ == '__main__':
    if not len(settings.token):
        access_token = get_access_token(input('code > '))
    else:
        access_token = settings.token

    os.environ['token'] = access_token

    job()

    schedule.every(10).seconds.do(job)
    # schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
