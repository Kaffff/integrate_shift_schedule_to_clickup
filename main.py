from distutils.log import error
from json import JSONEncoder
import os
from selenium import webdriver
from dotenv import load_dotenv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import requests


class RShift:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("./driver/chromedriver")
        self.driver.get(url)

    def login(self, user_id, user_password):
        elm_uid = self.driver.find_element_by_name("login_email")
        elm_uid.clear()
        elm_uid.send_keys(user_id)
        elm_pass = self.driver.find_element_by_name("login_pass")
        elm_pass.clear()
        elm_pass.send_keys(user_password)

        login_button = self.driver.find_element_by_tag_name("button")
        login_button.click()

    def extract_shiftdata(self,date,):
        self.driver.get(self.url+"&target_date="+date)
        tr = self.driver.find_element_by_id(
            "daily-tbody1").find_elements_by_tag_name("tr")
        if tr[0].get_attribute("class") != 'off': 
            work_time = tr[0].find_elements_by_tag_name("td")[1].find_element_by_class_name("works")
            work_time_from = work_time.get_attribute(
                    "data-working_time_from")
            working_time_to = work_time.get_attribute("data-working_time_to")
            return [work_time_from,working_time_to]
        else:
            return []


class ClickUp:
    def __init__(self,token,list_id):
        self.token = token
        self.list_id = list_id

    def create_task(self,start_date,due_date,member_id):
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        data = {
            "name": "バイト",
            "assignees": [member_id],
            "start_date":start_date,
            "start_date_time":True,
            "due_date":due_date,
            "due_date_time":True,
        }
        encoder = JSONEncoder()
        data = encoder.encode(data)
        res = requests.post(url='https://api.clickup.com/api/v2/list/'+self.list_id+'/task',headers=headers,data=data)
        print(res)


def to_unixtime(date,addtime):
    return int(parse(str(date)+" "+str(addtime)).timestamp())*1000


def main():
    load_dotenv()
    api_token = os.getenv("CLICKUP_API_TOKEN")
    list_id = os.getenv("CLICKUP_LIST_ID")
    member_id = os.getenv("CLICKUP_MEMBER_ID")
    clickup = ClickUp(api_token,list_id)


    print("シフト開始日を入力してください。 例 2022/02/02")
    date_from = input()
    print("シフト終了日を入力してください。")
    date_to = input()
    date = parse(date_from)
    user_id = os.getenv("USER_ID")
    user_password = os.getenv("USER_PASSWORD")
    rshift_url = os.getenv("RSHIFT_URL")
    rshift = RShift(rshift_url)
    rshift.login(user_id,user_password)
    for i in range((parse(date_to)-parse(date_from)).days+1):
        tmp_date = date+relativedelta(days=+i)
        work_time = rshift.extract_shiftdata(format(tmp_date, "%Y%m%d"))
        if len(work_time)!=0:
            start_date = to_unixtime(tmp_date.date(),work_time[0])
            due_date = to_unixtime(tmp_date.date(),work_time[1])
            clickup.create_task(start_date,due_date,member_id)
        
main()