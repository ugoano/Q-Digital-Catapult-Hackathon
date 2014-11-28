#!/usr/bin/python

from APIClient import APIClient

def main():
    SELECTED_EVENT_ID = '109349'
    print "Hi, my name is Q, Catapult Q..."

    userid = '5852'
    api_key = '8d055933415f8daff4fb51c8eccc2a25271e248c'
    base_url = 'https://www.eiseverywhere.com/'

    # Create the client
    api = APIClient( userid = userid,
                     api_key = api_key,
                     base_url = base_url )

    api.error = None # clear the old error, if any

    # create a request
    r = api.request(
                method = 'GET',
                # this will be appended to the base or test url and add .json at the end
                path = 'api/v2/global/authorize',
                params = {
                    'accountid': userid,
                    'key': api_key
                }
            )

    if api.error:
        print "Error! " + api.error
    else:
        print "Grande! "
        accessToken = r['accesstoken']

    # -----------------------------------------------------------
    r = api.request(
                method = 'GET',
                # this will be appended to the base or test url and add .json at the end
                path = 'api/v2/global/listEvents',
                params = {
                    'accesstoken': accessToken
                }
            )

    if api.error:
        print "Error! " + api.error
    else:
        print "Grande! "
        print str(r)

    r = api.request(method='GET', path='api/v2/ereg/getEvent',
                    params={'accesstoken': accessToken, 'eventid': r[0]['eventid']})
    if api.error:
        print "Error: " + api.error
    else:
        print str(r)
    """
    # -----------------------------------------------------------
    r = api.request(
                method = 'GET',
                # this will be appended to the base or test url and add .json at the end
                path = 'api/v2/ereg/listQuestions',
                params = {
                    'accesstoken': accessToken,
                    'eventid': SELECTED_EVENT_ID
                }
            )

    if api.error:
        print "Error! " + api.error
    else:
        print "Grande! "
        print "Questions asked: "
        print str(r)
    """

    # -----------------------------------------------------------
    r = api.request(
                method = 'GET',
                # this will be appended to the base or test url and add .json at the end
                path = 'api/v2/ereg/listAttendees',
                params = {
                    'accesstoken': accessToken,
                    'eventid': SELECTED_EVENT_ID
                }
            )

    if api.error:
        print "Error! " + api.error
    else:
        print "Grande! "

    print 'Attendees for eventid >' + SELECTED_EVENT_ID + '< are:'
    for attendee in r:
        print str(attendee) + "\n"
        #print attendee['name'], attendee['attendeeid']

    # UGO: the block below contains another call that successfully returns
    #      all questions asked to the user upon registration. I haven't finished
    #      splitting the response (the last line gives an error) but I think
    #      we don't actually need this call at all as we have everything we need
    #      in the code above.
    # # -----------------------------------------------------------
    for attendeeFromList in r:
        ra = api.request(
                    method = 'GET',
                    # this will be appended to the base or test url and add .json at the end
                    path = 'api/v2/ereg/getAttendee',
                    params = {
                        'accesstoken': accessToken,
                        'eventid': SELECTED_EVENT_ID,
                        'attendeeid': attendeeFromList['attendeeid']
                    }
                )

        if api.error:
            print "Error! " + api.error
        else:
            print "Grande! "
            print "Name: " + attendeeFromList['name']
            print "Email: " + attendeeFromList['email']
            if 'responses' in ra:
                qs = {'9': 'Company', '27': 'Project', '29': 'Objectives', '25': 'Twitter'}
                for num in qs:
                    if num in ra['responses']:
                        print qs[num] + ": " + ra['responses'][num]['response']

    #     print 'Attendees for eventid >' + SELECTED_EVENT_ID + '< are:'
    #     print ra
    #     for singleAttendee in ra:
    #         print singleAttendee['name']

if __name__ == '__main__':
  main()

















