import asyncio
import motor.motor_asyncio
from pymongo import ReturnDocument
from datetime import datetime, timedelta


class BannerDBManager:
    def __init__(self, client, db):
        url = "mongodb://localhost:27017"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self.client[client]
        self.banners = self.db[db]
        self.last_versions = self.db['last_versions']
        self.counters = self.db['counters']

    async def get_next_sequence_value(self, sequence_name):
        sequence_document = await self.counters.find_one_and_update(
            {'_id': sequence_name},
            {'$inc': {'sequence_value': 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return sequence_document['sequence_value']

    async def create_banner(self, tag_ids, feature_id, content, is_active):
        banner_id = await self.get_next_sequence_value('banner_id')
        document = {
            "_id": banner_id,
            "tag_ids": tag_ids,
            "feature_id": feature_id,
            "content": content,
            "is_active": is_active,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await self.banners.insert_one(document)
        return banner_id

    async def update_banner(self, banner_id, tag_ids, feature_id, content, is_active):
        old_banner = await self.banners.find_one({"_id": banner_id})
        if old_banner:
            prev_version = old_banner.copy()
            prev_version['prev_id'] = old_banner['_id']
            await self.last_versions.insert_one(prev_version)

        new_values = {
            "$set": {
                "tag_ids": tag_ids,
                "feature_id": feature_id,
                "content": content,
                "is_active": is_active,
                "updated_at": datetime.utcnow()
            }
        }
        await self.banners.update_one({"_id": banner_id}, new_values)

    async def delete_banner(self, banner_id):
        await self.banners.delete_one({"_id": banner_id})

    async def find_banners_by_criteria(self, tag_id, feature_id, use_last_revision=False):
        query = {
            "tag_ids": tag_id,
            "feature_id": feature_id,
            "is_active": True
        }
        if use_last_revision:
            five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
            query["created_at"] = {"$gte": five_minutes_ago}

        return await self.banners.find(query).to_list(None)

    async def find_banners_by_tag_or_feature(self, tag_id, feature_id, limit):
        query = {
            "$or": [{"tag_ids": {"$in": [tag_id]}}, {"feature_id": feature_id}],
            "is_active": True
        }
        return await self.banners.find(query).to_list(limit)

    async def find_all_versions_by_id(self, banner_id):
        return await self.last_versions.find({"prev_id": banner_id}).to_list(None)

    async def delete_banners_by_tag_or_feature(self, tag_id, feature_id):
        await self.banners.delete_many({
            "$or": [{"tag_ids": {"$in": [tag_id]}}, {"feature_id": feature_id}]
        })


if __name__ == "__main__":
    db_manager = BannerDBManager("avito",
                                   "banners")


    async def demo_operations():
        # Создание нескольких записей
        ids = []
        ids.append(await db_manager.create_banner([1, 2], 101,
                                                  {'title': 'Title 1', 'text': 'Text 1', 'url': 'http://url1.com'},
                                                  True))
        ids.append(await db_manager.create_banner([3, 4], 102,
                                                  {'title': 'Title 2', 'text': 'Text 2', 'url': 'http://url2.com'},
                                                  True))

        # Обновление записи
        await db_manager.update_banner(ids[0], [5, 6], 103, {'title': 'Updated Title', 'text': 'Updated Text',
                                                             'url': 'http://updatedurl.com'}, False)

        # Получение всех версий по ID
        versions = await db_manager.find_all_versions_by_id(ids[0])
        print("Versions of first banner:", versions)

        # Поиск записей по критериям
        active_banners = await db_manager.find_banners_by_criteria(2, 101, False)
        print("Active banners:", active_banners)

        # Удаление записей по tag_id или feature_id
        await db_manager.delete_banners_by_tag_or_feature(5, 103)


    # Запуск демо
    loop = asyncio.get_event_loop()
    loop.run_until_complete(demo_operations())
