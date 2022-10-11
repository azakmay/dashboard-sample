import flask
import pandas as pd
import requests
from flask import render_template, redirect, url_for
from jinja2 import TemplateNotFound

from apps import app
from .views.market import MarketView


@app.route('/')
def index():
    try:
        return redirect(url_for('todays_markets'))

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404


@app.route('/todays_markets', methods=['GET', 'POST'])
def todays_markets():
    view = MarketView()
    if view.is_htmx_request:
        html = view.get_daily_market_chart_html()
        resp = flask.make_response(html)
        return resp
    return render_template("home/todays-market-grid.html",
                           segment=view.segment)


@app.route('/search', methods=['GET', 'POST'])
def search():
    api_key = MarketView().av.api_key
    search_string = flask.request.args.get('q')
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search_string}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    search_results = data.get('bestMatches')
    search_results = pd.DataFrame(search_results)
    if not search_results.empty:
        search_results = search_results.loc[search_results['4. region'] == 'United States', :]
    search_results = search_results.drop_duplicates('1. symbol').to_dict(orient='records')
    return render_template('partials/search.html', search_results=search_results)


@app.route('/daily/chart', methods=['GET', 'POST'])
def daily_chart():
    from .views.stock import StockView
    view = StockView()
    return view.get_daily_stock_chart_html()


@app.route('/daily')
def daily():
    from .views.stock import StockView
    view = StockView()
    return render_template("home/daily.html", fig=view.get_daily_stock_chart_html(), symbol=view.symbol)
