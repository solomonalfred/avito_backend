import unittest
import requests
import json
import random


# server url: https://194.58.121.210:7777
# host url: http://0.0.0.0:7777

url_path = "http://0.0.0.0:7777"
class TestDOCXTemplatePlaceholder(unittest.TestCase):
     def test_authorization(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()
         print("получение access token")
         print(token)
         self.assertTrue(bool(len(token["access_token"]) > 0))

     def test_create_banners(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()

         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         url = f"{url_path}/banner"
         flag = True
         try:
             for i in range(100000):
                 array_size = random.randint(1, 1000)
                 banner_data = {
                     "tag_ids": [random.randint(1, 100000) for _ in range(array_size)],
                     "feature_id": random.randint(1, 1000),
                     "content": {
                         "title": "Заголовок нового баннера",
                         "text": "Описание нового баннера",
                         "url": "http://example.com/image.png"
                     },
                     "is_active": True
                 }
                 requests.post(url, headers=headers, data=json.dumps(banner_data))
         except:
            flag = False
         self.assertEqual(flag, True)

     def test_get_banners(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()

         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         url = f"{url_path}/banner"

         params = {
             'tag_id': random.randint(1, 100000),
             'feature_id': random.randint(1, 1000),
             'limit': 10
         }

         response = requests.get(url, headers=headers, params=params)
         print(response.json())
         self.assertTrue(len(response.json())>0)


     def test_patch_banners(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()
         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         flag = True
         for i in range(10):
             url = f"{url_path}/banner/{i}"
             array_size = random.randint(1, 1000)
             banner_data = {
                 "tag_ids": [random.randint(1, 100000) for _ in range(array_size)],
                 "feature_id": random.randint(1, 1000),
                 "content": {
                     "title": "Заголовок нового баннера",
                     "text": "Описание нового баннера",
                     "url": "http://example.com/image.png"
                 },
                 "is_active": False
             }
             resp = requests.patch(url, headers=headers, data=json.dumps(banner_data))
             result =resp.json()
             if result["description"] != "OK":
                 flag = False
                 break
         self.assertEqual(flag, True)

     def test_banners_versions(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()
         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         flag = True
         try:
             for i in range(10):
                 url = f"{url_path}/banner_versions/{i}"
                 resp = requests.get(url, headers=headers)
                 print(resp.json())
         except:
             flag = False
         self.assertEqual(flag, True)

     def test_delete_banners(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()
         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         flag = True
         for i in range(10):
             url = f"{url_path}/banner/{i}"
             resp = requests.delete(url, headers=headers)
             result = resp.json()
             if result["description"] != "Баннер успешно удален":
                 flag = False
                 break
         self.assertEqual(flag, True)


     def test_delete_by_tag_or_feature(self):
         url = f"{url_path}/access_token"
         data = {
             "username": "admin",
             "password": "12345"
         }
         res = requests.post(url, data=data)
         token = res.json()
         headers = {'Authorization': f'Bearer {token["access_token"]}'}
         params = {
             'tag_id': random.randint(1, 100000),
             'feature_id': random.randint(1, 1000),
         }
         url = f"{url_path}/banner"
         resp = requests.delete(url, headers=headers, params=params)
         result = resp.json()
         self.assertEqual(result["description"], "Баннеры успешно удалены")

