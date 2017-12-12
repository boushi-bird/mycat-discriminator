from bottle import route, run, static_file, request, response
import json

from setting import env, env_path

from path_util import relative_path
from discriminator import Discriminator

PORT = env('PORT')

discriminator = Discriminator(env_path('STORED_MODEL'), env_path('STORED_LABELS'))

@route('/api/upload', method='POST')
def upload():
  upload = request.files.get('upload')
  result = discriminator.run(upload)
  response.content_type = 'application/json'
  print(result)
  return json.dumps(result)

@route('/')
@route('/<filepath:path>')
def public_files(filepath = 'index.html'):
  if filepath.endswith('/'):
    filepath = '{}index.html'.format(filepath)
  if filepath.endswith('.js'):
    response.content_type = 'text/javascript'
  elif filepath.endswith('.css'):
    response.content_type = 'text/css'
  else:
    response.content_type = 'text/html; charset=utf-8'
  return static_file(filepath, root = relative_path(__file__, '../public'))

run(host='0.0.0.0', port=PORT, debug=True)
