import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))



class Human(ndb.Model):
    tors = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    major = ndb.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            human_query = Human.query()
            # human_query = human_query.filter(Human.email == user.email())
            human_data = human_query.fetch()
            # if student_data:
            #     self.response.write(student_data[0].year)
            # else:
                # greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                #             (user.nickname(), users.create_logout_url('/')))
                # self.response.out.write('%s' % greeting)
            template = jinja_environment.get_template('templates/register.html')
            self.response.write(template.render())

        else:
            self.response.write('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/'))

    def post(self):
        user = users.get_current_user()
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        # user = users.get_current_user()
        self.response.out.write('%s' % greeting)
        human1 = Human(tors=self.request.get('tors'),name=self.request.get('name'), year=self.request.get('year'), school=self.request.get('school'), major=self.request.get('major'))
        human1.put()
        human_query = Human.query()
        # human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            human_query = Human.query()
            # human_query = human_query.filter(Human.email == user.email())
            human_data = human_query.fetch()
            if human_data:
            #     self.response.write(student_data[0].year)
            # else:
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
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        user = users.get_current_user()
        self.response.out.write('%s' % greeting)
        tors_value = self.request.get('tors')
        # name_value = self.request.get('name')
        # year_value = self.request.get('year')
        # school_value = self.request.get('school')
        # major_value = self.request.get('major')
        #
        human1 = Human(tors=self.request.get('tors'),name=self.request.get('name'), year=self.request.get('year'), school=self.request.get('school'), major=self.request.get('major'))
        human1.put()
        # if tors_value == "Student":
        #     template = jinja_environment.get_template('templates/studentprofile.html')
        #     self.response.write(template.render())
        human_query = Human.query()
        # human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()

        """self.response.write(student_data[0].age)
        template = jinja_environment.get_template('templates/output_order.html')
        pizza_order = {
          'name': student_data[0].name,
          'year': student_data[0].year,
          'email': student_data[0].email,
          'school': student_data[0].school,
          'professor': student_data[0].professor,
          'description': student_data[0].description}
        self.response.write(template.render(pizza_order))"""

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/register.html',RegisterHandler),
], debug=True)
