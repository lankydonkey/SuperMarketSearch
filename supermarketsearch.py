from flask import Flask, render_template
from flask import request
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
import productsearch as ps

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/',methods=['POST'])
def run_query():

   text_search=request.form['textsearch']
   results=ps.get_all_prices(text_search)
   print(results)
   return render_template('results.html', results=results)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')





if __name__ == '__main__':
    app.run(debug=True)