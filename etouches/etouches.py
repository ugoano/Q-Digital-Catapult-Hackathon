#!/usr/bin/python

from APIClient import APIClient
import logging

USER_ID = '5852'
API_KEY = '8d055933415f8daff4fb51c8eccc2a25271e248c'
BASE_URL = 'https://www.eiseverywhere.com/'

ACCESS_TOKEN = None
SELECTED_EVENT_ID = '109349'
SELECTED_EVENT_ID2 = '110621'


def get_api_obj():
    # Create the client
    api = APIClient(userid=USER_ID,
                    api_key=API_KEY,
                    base_url=BASE_URL)

    api.error = None
    return api


def get_access_token():
    api = get_api_obj()

    # create a request
    r = api.request(
        method='GET',
        # this will be appended to the base or test url and add .json at the end
        path='api/v2/global/authorize',
        params={
            'accountid': USER_ID,
            'key': API_KEY
        }
    )

    if api.error:
        logging.error("Error! " + api.error)
    elif 'error' in r:
        logging.error(str(r))
    else:
        accessToken = r['accesstoken']
        return accessToken


def get_events():
    global ACCESS_TOKEN

    api = get_api_obj()
    ACCESS_TOKEN = get_access_token()

    events = {}
    r = api.request(
        method='GET',
        path='api/v2/global/listEvents',
        params={
            'accesstoken': ACCESS_TOKEN
        }
    )

    if api.error:
        logging.error("Error! " + api.error)
    elif 'error' in r:
        logging.error(str(r))
    else:
        events = r
        return events

    """
    r = api.request(method='GET', path='api/v2/ereg/getEvent',
                    params={'accesstoken': accessToken, 'eventid': r[0]['eventid']})
    if api.error:
        print "Error: " + api.error
    else:
        print str(r)
    """


def get_attendees_by_event(event_id):
    global ACCESS_TOKEN

    api = get_api_obj()
    ACCESS_TOKEN = get_access_token()

    attendees = {}
    r = api.request(
        method='GET',
        path='api/v2/ereg/listAttendees',
        params={
            'accesstoken': ACCESS_TOKEN,
            'eventid': event_id
        }
    )

    if api.error:
        logging.error("Error! " + api.error)
    elif 'error' in r:
        logging.error(str(r))
    else:
        logging.info('Attendees for eventid >' + event_id + '< are:')
        logging.info(r)
        print str(r)

        r = r[:15]  # maximum 15 people
        for attendeeFromList in r:

            ra = api.request(
                method='GET',
                path='api/v2/ereg/getAttendee',
                params={
                    'accesstoken': ACCESS_TOKEN,
                    'eventid': event_id,
                    'attendeeid': attendeeFromList['attendeeid']
                }
            )

            if api.error:
                logging.error("Error! " + api.error)
            elif 'error' in ra:
                logging.error(str(ra))
            else:
                email = attendeeFromList['email']
                attendees[email] = {}
                person = attendees[email]
                person['name'] = attendeeFromList['name']
                if 'responses' in ra:
                    qs = {'9': 'company', '27': 'project', '29': 'objective', '25': 'twitter'}
                    for num in qs:
                        if num in ra['responses']:
                            logging.info(qs[num] + ": " + ra['responses'][num]['response'])
                            person[qs[num].lower()] = ra['responses'][num]['response']
        return attendees
