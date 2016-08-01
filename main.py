import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))






class PizzaOrder(ndb.Model):

    crust = ndb.StringProperty(required=True)
    size = ndb.StringProperty(required=True)
    sauce = ndb.StringProperty(required=False)
    cheese = ndb.StringProperty(required=False)
    topings = ndb.StringProperty(required=False)

class Customer(ndb.Model):
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    age = ndb.IntegerProperty(required=True)
    address = ndb.StringProperty(required=True)
    pizza_id = ndb.KeyProperty(required=True)




class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
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
        template = jinja_environment.get_template('templates/output_order.html')
        pizza_order = {
          'crust_answer': self.request.get('crust'),
          'size_answer': self.request.get('size'),
          'sauce_answer': self.request.get('sauce'),
          'cheese_answer': self.request.get('cheese'),
          'topings_answer': self.request.get('topings')}
        pizza_instance = PizzaOrder(crust=self.request.get('crust'),size=self.request.get('size'),sauce=self.request.get('sauce'),cheese=self.request.get('cheese'),topings=self.request.get('topings'))
        key = pizza_instance.put()
        pizza_order['order_number']=key.id()
        self.response.write(template.render(pizza_order))
        customer1 = Customer(email=user.email(),name=self.request.get('name'),age=int(self.request.get('age')),pizza_id=key,address=self.request.get('address'))
        customer1.put()


app = webapp2.WSGIApplication([
  ('/', MainHandler),
], debug=True)
