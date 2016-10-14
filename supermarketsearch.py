# -*- coding: utf-8 -*-
import time
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
   start_time = time.time()
   results=ps.get_all_prices(text_search)
   tm = ' in '+str(int(time.time() - start_time)) +' seconds'
   amount=len(results)
   print(results)
   return render_template('results.html', amount=amount,tm=tm,results=results)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')



if __name__ == '__main__':
    app.run(debug=True)