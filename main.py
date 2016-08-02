import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))






class Student(ndb.Model):

    name = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    school = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class Tutor(ndb.Model):
    name = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(repeated=True)
    school = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            student_query = Student.query()
            student_query = student_query.filter(Student.email == user.email())
            student_data = student_query.fetch()
            if student_data:
                self.response.write(student_data[0].year)
            else:
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                            (user.nickname(), users.create_logout_url('/')))
                self.response.out.write('%s' % greeting)
                template = jinja_environment.get_template('templates/input_order.html')
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
        student1 = Student(name=self.request.get('name'), year=self.request.get('year'), email=user.email(), school=self.request.get('school'), description=self.request.get('description'))
        student1.put()
        student_query = Student.query()
        student_query = student_query.filter(Student.email == user.email())
        student_data = student_query.fetch()
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
], debug=True)
