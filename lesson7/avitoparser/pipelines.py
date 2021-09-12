# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

#оставляем для сохранения данных, для фото новый класс
class AvitoparserPipeline:  # В этот item попадаем после, потому что более низкий приоритет в settings
    def process_item(self, item, spider):
        print(2)
        return item

class AvitoPhotosPipeline(ImagesPipeline):  # В этот item попадаем сначала, потому что более высокий приоритет в settings
    #обязательно внести в сеттингс IMAGES_STORE = "название папки" и установить модуль пилоу
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img) # Скачиваем здесь фото и результат можно увидеть в след. методе item completed
                except Exception as e:
                    print(e)
        print('saved img')

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]   # Здесь проверяем результат скачивания и сохраняем внутри item
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):      # Метод для изменения места скачивания файлов
    #     pass
