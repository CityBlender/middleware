import settings
from flask import Flask, render_template

app = Flask(__name__)

# homepage
@app.route('/')
def homepage():
  return render_template('index.html')

# run the web server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)