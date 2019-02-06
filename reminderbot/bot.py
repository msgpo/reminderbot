#!/usr/bin/env python

from bs4 import BeautifulSoup
from markdownify import markdownify
import requests

from urllib.parse import urljoin

from reminderbot.message import make_message

BOT_HEADERS = {
        'User-Agent': 'MeshBot User Agent',
        'From': 'probably eenblam'
}

# HTTP
def get(url):
    return requests.get(url, headers=BOT_HEADERS)

def get_minutes_list():
    return get('https://sudoroom.org/wiki/mesh/Minutes')

def send_to_chat(payload, webhook_url):
    payload = {
            "icon_emoji": ":clock7:",
            "text": payload
            }
    return requests.post(webhook_url, json=payload, headers=BOT_HEADERS)

# Parsers
def get_link_to_minutes(text):
    # Parse Mesh/Minutes to find link to latest minutes
    soup = BeautifulSoup(text, 'html.parser')
    try:
        # Get the main page body
        page = soup.find(id='mw-content-text')
        # Assumes the page layout doesn't change much
        minutes_location = page.div.table.tbody.td.a['href']
    except AttributeError:
        # Couldn't find it! Abort
        raise ValueError("Couldn't parse Mesh/Minutes for link to latest minutes.") 

    minutes_url = urljoin('https://sudoroom.org', minutes_location)
    return minutes_url

def get_action_items_from_minutes(text):
    item_soup = BeautifulSoup(text, 'html.parser')
    action_items = item_soup.find(id='Action_Items')
    if action_items is None:
        raise ValueError('No Action Items found for {}'.format(minutes_url))
    try:
        items_text = action_items.parent.find_next_sibling('ul')
    except AttributeError:
        err = "Couldn't navigate to action item list from #Action_Items on {}"
        raise ValueError(err.format(minutes_url))
    return items_text

def abort(msg):
    import sys
    print(msg)
    sys.exit(1)

def main(webhook_url):
    #webhook = os.getenv('ROCKETCHAT_WEBHOOK')
    #if webhook is None:
    #    abort('Could not access ROCKETCHAT_WEBHOOK environment variable')

    #TODO catch network exceptions? e.g. except requests.exceptions.ConnectionError
    print('Fetching list of minutes...')
    r = get_minutes_list()

    if not r.ok:
        abort("Couldn't get Mesh/Minutes page. HTTP status {}".format(r.status_code))

    print('...got list of minutes. Parsing for latest link.')
    try:
        minutes_url = get_link_to_minutes(r.text)
    except Exception as e:
        abort(e)

    print('Parsed minutes url {}. Attempting to fetch minutes...'.format(minutes_url))
    minutes = get(minutes_url)
    if not minutes.ok:
        abort("Couldn't get latest minutes page ({}). HTTP status {}".format(
            minutes_url, minutes.status_code
        ))

    print('...retrieved minutes. Parsing for action items.')
    try:
        items_text = get_action_items_from_minutes(minutes.text)
    except Exception as e:
        abort(e)

    # markdownify won't strip weird whitespace from mediawiki, so prettify first
    try:
        md = markdownify(items_text.prettify())
    except Exception as e:
        abort("Markdownify broke: {}".format(e))
    payload = make_message(source=minutes_url, items=md)
    print(payload)
    try:
        print(payload)
        rc_response = send_to_chat(payload, webhook_url)
    except Exception as e:
        abort("Couldn't send to chat: {}".format(e))
