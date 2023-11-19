from database import db_manager


class ScrapyProjectPipeline:
    def process_item(self, item, spider):
        name, image = item['name'], item['image']["href"]
        db_manager.insert_item(name, image)

        return item
