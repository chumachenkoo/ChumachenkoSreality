from database import DatabaseManager


class ScrapyProjectPipeline:
    def process_item(self, item, spider):
        name, image = item['name'], item['image']["href"]
        db_manager = DatabaseManager(
            dbname="scrapy_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        db_manager.insert_item(name, image)

        return item
