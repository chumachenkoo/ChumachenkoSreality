from flask import Flask, render_template, request
from database import db_manager
from scrapy_project.scrapy_project.spiders import sreality_spider


app = Flask(__name__)

sreality_spider.launch()

PER_PAGE = 25


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    items = db_manager.load_all_items()
    flats = items[start:end]
    flats_len = len(items)

    total_pages = (flats_len + PER_PAGE - 1) // PER_PAGE

    return render_template('index.html', items=flats, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
