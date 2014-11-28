from google.appengine.ext import webapp, db
from linkedin import find_profile
from etouches.etouches import get_attendees_by_event
import json
import logging
import traceback


class EventAttendeesModel(db.Model):
    event = db.StringProperty()
    data = db.TextProperty()


class ProcessEventHandler(webapp.RequestHandler):

    def get(self):
        event = self.request.get("event_id")
        attendees = get_attendees_by_event(event)
        if attendees is None:
            self.response.set_status(500)
            attendees = {'error': 'Error getting attendee info'}
        else:
            self.response.set_status(200)
            for person in attendees:
                search_term = attendees[person]['name']
                if 'company' in attendees[person]:
                    search_term += attendees[person]['company']
                skills = find_profile(search_term)
                if skills is not None:
                    attendees[person]['skills'] = skills
            events = EventAttendeesModel.all().filter("event =", event).get()
            if events is None:
                events = EventAttendeesModel()
            events.event = event
            events.data = json.dumps(attendees)
            events.put()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(attendees))


class GetMatchesHandler(webapp.RequestHandler):

    def get(self):
        user = self.request.get("email")
        event = self.request.get("event_id")

        events = EventAttendeesModel.all().filter("event =", event).get()
        matches = []
        if events is not None:
            try:
                attendees = json.loads(events.data)
                if 'skills' in attendees[user]:
                    skills = attendees[user]['skills']
                    logging.info("Comparing against: " + str(skills))
                    user_points = {}
                    for skill in skills:
                        for a_email in attendees:
                            if a_email != user:  # don't match yourself
                                if a_email not in user_points:
                                    user_points[a_email] = 0
                                logging.info(str(attendees[a_email]))
                                if 'skills' in attendees[a_email]:
                                    if skill in attendees[a_email]['skills']:
                                        logging.info("Found " + skill)
                                        user_points[a_email] += 1
                    for point_email in user_points:
                        if user_points[point_email] >= 1:
                            matches.append({'name': attendees[point_email]['name'],
                                            'points': user_points[point_email]})
                self.response.set_status(200)
                self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(json.dumps(matches))
            except:
                logging.error(traceback.format_exc())
                self.response.set_status(500)
        else:
            logging.error(traceback.format_exc())
            self.response.set_status(500)

application = webapp.WSGIApplication([('/processevent', ProcessEventHandler),
                                      ('/getmatches', GetMatchesHandler)],
                                     debug=True)
