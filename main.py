import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.api import app_identity
from google.appengine.api import mail
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
    subject = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty(required=True)

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
            dictionary = {
            "sign_in_url": '<a href="%s"><img src="../static_files/biglogo.png" alt="Sign in" style="width: auto; height:250px; border:0; margin-left: 415px; margin-top:180px;"></a>' %
            users.create_login_url('/')
            }
            template = jinja_environment.get_template('templates/signinpage.html')
            self.response.write(template.render(dictionary))

    def post(self):
        user = users.get_current_user()
        human1 = Human(tors=self.request.get('tors'),name=self.request.get('name'), year=self.request.get('year'), school=self.request.get('school'), major=self.request.get('major'), email=user.email(), subject=self.request.get_all('subject'), description=self.request.get('description'))
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
          'name' : human_data[0].name,
          'description':human_data[0].description,
          }
            template = jinja_environment.get_template('templates/tutorhome.html')
            self.response.write(template.render(info))
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('%s' % greeting)
        elif human_data[0].tors == "Student":
            info = {
          'name': human_data[0].name,
          }
            template = jinja_environment.get_template('templates/studenthome.html')
            self.response.write(template.render(info))
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('%s' % greeting)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        time.sleep(1)
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        info = {
            'school': human_data[0].school,
            'major' : human_data[0].major,
            'year' : human_data[0].year,
            'name' : human_data[0].name,
            'description': human_data[0].description,
        }
        user_id=self.request.get('id')
        template = jinja_environment.get_template('templates/studentprofile.html')
        self.response.write(template.render(info))
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        self.response.out.write('%s' % greeting)

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        search = self.request.get('searchbox')
        user = users.get_current_user()
        human_query1 = Human.query()
        human_query1 = human_query1.filter(Human.email == user.email())
        human_data1 = human_query1.fetch()
        school_of_user = human_data1[0].school
        human_query = Human.query()
        human_query =  Human.query(Human.subject == search)
        human_query = human_query.filter(Human.school == school_of_user)
        human_query = human_query.filter(Human.tors == "Tutor")
        human_data = human_query.fetch()
        names_of_results = ""
        keys_of_results = []
        y=0
        for x in human_data:
            keys_of_results.append({"name":Human.get_by_id(int(x.key.id())).name, "link":"/profileviewer?id="+str(x.key.id())})
            y=y+1
        for x in human_data:
            names_of_results=names_of_results+"<div>"+x.name+"</div>"
        template_values = {
        'results':keys_of_results,
        }
        template = jinja_environment.get_template('templates/results.html')
        self.response.write(template.render(template_values))


class ProfileViewerHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_id=self.request.get('id')
        tutor = {
        'tutor': Human.get_by_id(int(user_id))
        }
        template = jinja_environment.get_template('templates/tutorhomeview.html')
        self.response.write(template.render(tutor))
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        self.response.out.write('%s' % greeting)

class SendMailHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        send_approved_mail(user.email(), self.request.get('id'), self.request.get('email'))
        self.response.content_type = 'text/plain'
        self.redirect('/homepage')

def send_approved_mail(sender_address ,emailr, content):
    mail.send_mail(sender=sender_address,
                   to=emailr,
                   subject="Tutor Request",
                   body=content)

class EditHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        template = jinja_environment.get_template('templates/edit.html')
        info = {
      'university': human_data[0].school,
      'major' : human_data[0].major,
      'year' : human_data[0].year,
      'name' : human_data[0].name,
      'description' : human_data[0].description
      }
        self.response.write(template.render(info))
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        self.response.out.write('%s' % greeting)
    def post(self):
        user = users.get_current_user()
        human_query = Human.query()
        human_query = human_query.filter(Human.email == user.email())
        human_data = human_query.fetch()
        human_data = human_data[0]
        names=self.request.get('name')
        universitys=self.request.get('school')
        majors=self.request.get('major')
        years=self.request.get('year')
        descriptions=self.request.get('description')
        if len(names)>0:
            human_data.name=names
        if len(universitys)>0:
            human_data.school=universitys
        if len(majors)>0:
            human_data.major=majors
        if len(years)>0:
            human_data.year=years
        if len(descriptions)>0:
            human_data.description=descriptions
        human_data.put()
        self.redirect('/profile')

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', HomePageHandler),
  ('/profile',ProfileHandler),
  ('/results', ResultsHandler),
  ('/profileviewer', ProfileViewerHandler),
  ('/send_mail', SendMailHandler),
  ('/edit', EditHandler),
], debug=True)
