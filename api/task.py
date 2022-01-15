from flask import jsonify, request
from flask_restful import Resource
#from app import mongo
import logging as logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KeywordSearch(Resource):
    def post(self):
        body = request.get_json()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        driver.get("http://www.seobook.com/user")
        print(driver.title)

        username = driver.find_element_by_name("name")
        username.send_keys("arrowgance99")

        password = driver.find_element_by_name("pass")
        password.send_keys("RmB7MMRMKB")

        password.send_keys(Keys.RETURN)

        textinp = body['blogDescription']

        textinp = " ".join(textinp.split())
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Tools"))
            )
            element.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Keyword Density Analyzer"))
            )
            element.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-type='text']"))
            )
            element.click()
            
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "url"))
            )
            element.clear()
            element.send_keys(textinp)
            element = driver.find_element_by_id("form-submit")
            element.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "row"))
            )
            body = element.find_elements_by_tag_name("table")
            keywords = dict()
            for e in body:
                tbody = e.find_element_by_tag_name("tbody")
                rows = tbody.find_elements_by_tag_name("tr")
                keys = []
                for row in rows:
                    datas = row.find_elements_by_tag_name("td")
                    rowdata = []
                    for data in datas:
                        rowdata.append(data.text)
                    keyDict = {"Keyword":rowdata[0],"Density":rowdata[2]}
                    keys.append(keyDict)
                head = e.find_element_by_tag_name("th")
                keywords.update({head.text:keys})
            return jsonify(keywords)
            time.sleep(5)
        finally:
            driver.quit()

class Task1(Resource):
    def get(self,author):
        content = mongo.db.content

        output = []

        q = content.find_one({'author' : author})
        if q:
            output = {'author' : q['author'], 'title' : q['title'], 'blog' : q['blog']}
        else:
            output = 'Not found'
        return jsonify({'result' : output})

class Task(Resource):       
    def get(self):
        content = mongo.db.content

        output = []

        for q in content.find():
            output.append({'author' : q['author'], 'title' : q['title'], 'blog' : q['blog']})

        return jsonify({'result' : output})

    def post(self):
        content = mongo.db.content

        author = request.json['author']
        title = request.json['title']
        blog = request.json['blog']

        content.insert({'author' : author, 'title' : title, 'blog' : blog})
        return 'Successful Insertion'
    def patch(self):
        author = request.json['author']

        content = mongo.db.content

        content.update({'author' : author },
                    {'author': 'Harry',
                    'title': 'Second Blog',
                    'blog': 'Hello everyone welcome to my first blog. Update: actually second'
                            })
        return 'Insertion Successful'

    def delete(self):
        author = request.json['author']

        content = mongo.db.content

        content.remove({'author' : author })

        return 'Deletion Successful'