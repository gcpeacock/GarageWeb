"""
appserver.py
- creates an application instance and runs the dev server
"""
from garagewebapi.application import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)