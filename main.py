import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import time

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))



class Human(ndb.Model):
    tors = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    major = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            human_query = Human.query()
            human_query = human_query.filter(Human.email == user.email())
            human_data = human_query.fetch()
            if human_data:
                self.redirect('/homepage')


            else:
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
                self.response.out.write('%s' % greeting)
                template = jinja_environment.get_template('templates/register.html')
                self.response.write(template.render())
        else:
            self.response.write('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/'))

    def post(self):
        user = users.get_current_user()
        human1 = Human(tors=self.request.get('tors'),name=self.request.get('name'), year=self.request.get('year'), school=self.request.get('school'), major=self.request.get('major'), email=user.email())
        human1.put()
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        self.redirect('/homepage')

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        time.sleep(1)
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        if human_data[0].tors == "Tutor":
            info = {
          'university': human_data[0].school,
          'major' : human_data[0].major,
          'year' : human_data[0].year,
          }
            template = jinja_environment.get_template('templates/tutorhome.html')
            self.response.write(template.render(info))
            self.response.write('tutor')
        elif human_data[0].tors == "Student":
            info = {
          'name': human_data[0].name,
          }
            template = jinja_environment.get_template('templates/studenthome.html')
            self.response.write(template.render(info))
            self.response.write('student')


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', HomePageHandler),
], debug=True)
