from google.appengine.ext import webapp


class ProcessEventHandler(webapp.RequestHandler):

    def get(self):
        event = self.request.get("event_id")


class GetMatchesHandler(webapp.RequestHandler):

    def get(self):
        user = self.request.get("email")

application = webapp.WSGIApplication([('/processevent', ProcessEventHandler),
                                      ('/getmatches', GetMatchesHandler)],
                                     debug=True)
