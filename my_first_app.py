import webapp2
class HomePage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write('<h3>Vista Jin</h3> Test my first app')
app = webapp2.WSGIApplication([
  ('/', HomePage)], debug=True)