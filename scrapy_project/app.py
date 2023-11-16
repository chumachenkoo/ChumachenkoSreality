from flask import Flask, render_template, request
import database
from scrapy_project.scrapy_project.spiders import sreality_spider


app = Flask(__name__)

db_manager = database.DatabaseManager(
    dbname="scrapy_db",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)

db_manager.create_database()
db_manager.create_table_if_doesnt_exist()
db_manager.delete_all_items()
sreality_spider.launch()

PER_PAGE = 25


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    items = db_manager.load_all_items()[start:end]

    total_items = len(db_manager.load_all_items())
    total_pages = (total_items + PER_PAGE - 1) // PER_PAGE

    return render_template('index.html', items=items, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
