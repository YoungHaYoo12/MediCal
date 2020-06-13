from app.core import core

@core.route('/')
def index():
  return "Index Page"