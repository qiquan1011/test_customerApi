import json
import os
import time

import requests
from selenium import webdriver
from xlrd import open_workbook

import readConfig
from common import configHTTP
from common.Log import Log

local_read_Config=readConfig
local_config_Http=configHTTP.Config_Http()
porDir=local_read_Config.porDir
logger=Log().logger
chat_cl=[]
customer_cl=[]
chatbot_cl=[]
#获取后台登录cookie
'''
def get_chatbot_login():
   # sql_0=' update public_config_mode set int_value=0 where code="conf.login.decrypt" and web_id="-1" '
   # update_chatbotData(sql_0)


    send_pearm={"username":"auto_test","password":"123456abc","isRememberMe":"false"}
    #baseUrl=local_read_Config.get_HTTP("baseUrl")
    header={"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*"}
    login_response=requests.post("http://v5-dev-customer.faqrobot.net/admin/login",params=send_pearm,headers=header)
    print(login_response.headers)

    chatbot_cookies=requests.utils.dict_from_cookiejar(login_response.cookies)
    print(chatbot_cookies)
    if len(chat_cl)>0 :
        del chat_cl[-len(chat_cl):]
    for k, v in chatbot_cookies.items():
        if k + ":" + v:
            s = k + "=" + v
            chat_cl.append(s)
    login_chat_cookies=";".join(chat_cl)
    print("login_chat_cookies是：",login_chat_cookies)
    print(type(login_chat_cookies))

    sql_1=' update public_config_mode set int_value=1 where code="conf.login.decrypt" and web_id="-1" '
    update_chatbotData(sql_1)
    r = requests.get("http://v5-dev-customer.faqrobot.net/customerservice/loginMonitor/login")
    r_cookie=requests.utils.dict_from_cookiejar(r.cookies)
    for k, v in r_cookie.items():
        if k + ":" + v:
            s = k + "=" + v
            chat_cl.append(s)
    print(chat_cl)
    chat_cl.pop(2)
    chat_customer_cookie=';'.join(chat_cl)
    print(chat_customer_cookie)

    print(r_cookie)

    return login_chat_cookies,chatbot_cookies,chat_customer_cookie

    #url = "http://v5-dev-customer.faqrobot.net/customerservice/summary/exportSum"

    #payload = "{\"remark\":\"\",\"classId\":\"\",\"beginTime\":\"2020-05-17 00:00:00\",\"endTime\":\"2020-08-17 23:59:59\",\"visitorName\":\"游客18285154\",\"queryType\":2}"
    #headers = {
        #'Content-Type': 'application/json;charset=UTF-8',
        #'Accept':'application/json, text/plain, */*',
        #'Cookie':login_chat_cookies
    #}
    #print(headers)
    #response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text.encode('utf8'))


'''
def get_customer_login():
    #sql_0 = ' update public_config_mode set int_value=0 where code="conf.login.decrypt" and web_id="-1" '
    #update_chatbotData(sql_0)
    #客服登录
    send_pearm={"username":"auto_kefu","password":"123456abc","isRememberMe":"false"}
    #baseUrl = local_read_Config.get_HTTP("baseUrl")
    header={"Content-Type":"application/x-www-form-urlencoded","Authorization":"Basic bml5YXpob3U6MTIzNDU2YWJj","Referer":"http://v5-dev-customer.faqrobot.net/webcustomer/index_standard.html",
            "Accept": "application/json, text/plain, */*" }
    customer_login = requests.post("http://v5-dev-customer.faqrobot.net/customerservice/login",params=send_pearm,headers=header)
    #处理cookie
    #customer_login_cookie=customer_login.headers["set-cookie"]
    customer_cookie = requests.utils.dict_from_cookiejar(customer_login.cookies)
    if len(customer_cl) > 0:
        del customer_cl[-len(customer_cl):]
    for k, v in customer_cookie.items():
        if k + ":" + v:
            s = k + "=" + v
            customer_cl.append(s)
    login_customer_cookies = ";".join(customer_cl)
    return login_customer_cookies

    # congexcel中读取测试用例
def get_excel(excel_name, sheet_name):
    cls = []
    # 获取excel路径
    excelPath = os.path.join(porDir, "testFile", "case", excel_name)

    # 打开文件
    try:
        file = open_workbook(excelPath)
        sheet = file.sheet_by_name(sheet_name)
        first_line = sheet.nrows
        for i in range(first_line):
            if sheet.row_values(i)[0] != u'case_name':
                cls.append(sheet.row_values(i))
        return cls
    except FileExistsError:
        logger.error("文件打开失败")

def show_return_msg(response, case_name,parameter):
    msg_url = response.url
    msg = response.text
    print("\n用例名字", case_name)
    print("\n请求体：",parameter)
    print("\n请求地址", msg_url)

    print("\n请求返回" + "\n" + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))

    #sql_1 = ' update public_config_mode set int_value=1 where code="conf.login.decrypt" and web_id="-1" '
    #update_chatbotData(sql_1)

#获取客服会话信息
def get_inService():
    header = {"Content-Type": "application/json;charset=UTF-8", "cookie": get_customer_login()}
    reponse = requests.get(
        "http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/inService?serviceType=single",
        headers=header)
    service = reponse.json()
    print(service)
    serviceId = service["data"]["service"]["serviceId"]
    serviceTime = service["data"]["service"]["beginTime"]
    visitorName = service["data"]["service"]["visitorName"]

    return serviceId, serviceTime, visitorName

def Turn_To_Artificial_Scene():
    get_cookie=get_customer_login()

    agentInfo_header = {"cookie": get_cookie}
    agentInfo_response = requests.get("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/agentInfo", headers=agentInfo_header)

    tenantId = agentInfo_response.json()["data"]["agent"]["tenantId"]
    employeeId = agentInfo_response.json()["data"]["agent"]["employeeId"]
    groupId=agentInfo_response.json()["data"]["groups"][0]["id"]
    groupName=agentInfo_response.json()["data"]["groups"][0]["name"]
    #切换客服技能组状态
    send_param = [{"tenantId": tenantId, "groupId": groupId, "groupName": groupName,
                  "agentId": employeeId, "agentName": "", "status": "ONLINE", "orginStatus": "LEAVE",
                  "agentStatus": 1, "orginAgentStatus": 3}]
    print(send_param)
    data = json.dumps(send_param)
    register_header = {"Content-Type": "application/json;charset=UTF-8", "cookie":get_cookie}
    register_response = requests.post(
        "http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/setUpAgentGroupStatus",
        data=data, headers=register_header)

    #获取visitorID
    header = {"Content-Type": "application/json;charset=UTF-8",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    send_param = {"visitorId": "",
                  "source": {"platformId": "self", "platformName": "self", "tenantId": "149", "typeId": "1",
                             "typeName": "网页渠道", "channelCode": "31", "channelName": "网页渠道"}}
    send_param_json = json.dumps(send_param)
    findOrCreate_reponse = requests.post("http://192.168.1.71/customerservice/webim/visitor/findOrCreate",
                            headers=header, data=send_param_json)
    print(findOrCreate_reponse.text)
    visitorId = findOrCreate_reponse.json()["data"]["visitorBasicInfo"]["visitorId"]


    #转人工

    header = {"Content-Type": "application/json;charset=UTF-8",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    send_param = {"visitor": {"visitorId":visitorId, "name": "游客09505403"},
                  "request": {"tenantId": tenantId, "groupId": groupId},
                  "source": {"platformId": "self", "platformName": "self", "tenantId": "149", "typeId": "1",
                             "typeName": "网页渠道", "channelCode": "31", "channelName": "网页渠道"},
                  "features": {"ip": "", "region": "", "terminal": "", "os": "", "accessProxy": ""},
                  "authInfo": {"id": "", "account": "", "name": "", "test": ""}}
    send_param_json = json.dumps(send_param)
    switchLabor_reponse = requests.post("http://v5-dev-customer.faqrobot.net/customerservice/webim/visitor/switchLabor",
                            headers=header, data=send_param_json)


    #获取会话信息
    header = {"cookie":get_cookie}
    inService_reponse = requests.get(
        "http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/inService?serviceType=single&agentId"+"="+ employeeId,
        headers=header)
    service = inService_reponse.json()

    serviceId = service["data"][0]["service"]["serviceId"]
    serviceTime = service["data"][0]["service"]["beginTime"]
    visitorName = service["data"][0]["service"]["visitorName"]
    print(serviceId)
    return serviceId,serviceTime,visitorName
'''
    return login_customer_cookies ,serviceId,serviceTime,visitorName
#获取客服信息
def get_agentInfo():
    header={"cookie":get_customer_login()}
    response=requests.get("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/agentInfo",headers=header)
    print(response.text)
    tenantId=response.json()["data"]["agent"]["tenantId"]
    employeeId=response.json()["data"]["agent"]["employeeId"]
    return tenantId,employeeId


#客服上线技能组
def get_register():
    send_param={"tenantId":get_agentInfo()[0],"groupId":"1000010341","groupName":"售前客服","agentId":get_agentInfo()[1],"agentName":"","status":"ONLINE","orginStatus":"LEAVE","agentStatus":1,"orginAgentStatus":3}
    print(send_param)
    data=json.dumps(send_param)
    header={"Content-Type":"application/json;charset=UTF-8","cookie":get_customer_login()}
    register_response=requests.post("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/setUpAgentGroupStatus",
                                    data=data,headers=header)
    print("客服上线技能组：",register_response.json())
'''
#初始化机器人
#def get_chabot():
    #header={"Content-Type":"application/json"}
    #reponse=requests.get("http://v5-dev-customer.faqrobot.net/chatbot/web/init/1601347359079?sysNum=1601347359079&sourceId=70167&lang=zh_CN&_=1606898265152"
     #                    ,headers=header)
'''
#转人工
def get_visitor():
    cookies=get_chabot()

    header = {"Content-Type": "application/json","cookie":cookies,"Accept":"application/json, text/javascript, */*; q=0.01"}
    send_param={"content":"转人工","type":0}
    data=json.dumps(send_param)
    response=requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1601347359079?sourceId=70167",
                           headers=header,data=data)
    print(response.json())
    vissitor_cookies=requests.utils.dict_from_cookiejar(response.cookies)
    print("cookies是：",vissitor_cookies)
    #send_params = {"content": "售前技术", "type": 0, "x": 0, "y": 0}
    #data_skill=json.dumps(send_params)
    #response_skill=requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1601347359079?sourceId=70167",
                           #headers=header,data=data_skill)
    #print(response_skill.json())
#选择转接的技能组
#def get_skills():
    #cookies1=get_chabot()
    #print("cookies1是：",cookies1)
    #header = {"Content-Type": "application/json", "cookie":cookies1,
               #"Accept":"application/json, text/javascript, */*; q=0.01",
              #"Referer":"http://v5-dev-customer.faqrobot.net/webchatbot/chat.html?sysNum=1577067263668&sourceId=169&lang=zh_CN"}
    #send_param ={"content":"售前技术","type":0,"x":0,"y":0}
    #data = json.dumps(send_param)
    #response = requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1577067263668?sourceId=169",
                             # headers=header, data=data)
    #print("技能组是：",response.json())
'''
'''
def get_visitorId():
    header={"Content-Type":"application/json;charset=UTF-8","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    send_param={"visitorId":"","source":{"platformId":"self","platformName":"self","tenantId":"149","typeId":"1","typeName":"网页渠道","channelCode":"31","channelName":"网页渠道"}}
    send_param_json=json.dumps(send_param)
    reponse=requests.post("http://192.168.1.71/customerservice/webim/visitor/findOrCreate",
                          headers=header,data=send_param_json)
    visitorId=reponse.json()["data"]["visitorBasicInfo"]["visitorId"]

    print(visitorId)
    return visitorId
def Transfer_To_Labor():
    header = {"Content-Type": "application/json;charset=UTF-8",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    send_param={"visitor":{"visitorId":get_visitorId(),"name":"游客09505403"},"request":{"tenantId":"149","groupId":"1000010341"},"source":{"platformId":"self","platformName":"self","tenantId":"149","typeId":"1","typeName":"网页渠道","channelCode":"31","channelName":"网页渠道"},"features":{"ip":"","region":"","terminal":"","os":"","accessProxy":""},"authInfo":{"id":"","account":"","name":"","test":""}}
    send_param_json = json.dumps(send_param)
    print(send_param_json)
    reponse = requests.post("http://v5-dev-customer.faqrobot.net/customerservice/webim/visitor/switchLabor",
                            headers=header,data=send_param_json)
    print(reponse.text)
'''



def getSelect_dataBase(sql):
    content=local_config_Http.get_datebase()
    cursor=content.cursor()
    cursor.execute(sql)
    content.commit()
    all=cursor.fetchall()
    return all

def getDelecte_dataBase(sql):
    content = local_config_Http.get_datebase()
    cursor = content.cursor()
    cursor.execute(sql)
    content.commit()
    print('成功删除', cursor.rowcount, '条数据')


def update_chatbotData(sql):
    content=local_config_Http.get_chatbotData()
    cussor=content.cursor()
    cussor.execute(sql)
    content.commit()













