import json
import unittest
from urllib import parse

import paramunittest

from common import commom, configHTTP
from common.commom import logger

local_config_http=configHTTP.Config_Http()
editclass_excel=commom.get_excel("testCase.xlsx","editClass")
@paramunittest.parametrized(*editclass_excel)
class editClass(unittest.TestCase):
    def setUp(self):
        pass
    def setParameters(self,case_name,method,url,parameter,code,status,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        self.status=str(status)
        self.message=str(message)
        print(self.parameter)

    def test_editClass(self):
        self.delect_class()
        login_cookies=commom.get_customer_login()
        header={"content-Type":"application/json;charset=UTF-8","cookie":login_cookies}
        local_config_http.get_Heardes(header)
        send_dict=json.loads(self.parameter)
        send_dict["classId"]=self.select_classId()[0][0]
        send_parm=json.dumps(send_dict)
        print(send_parm)
        local_config_http.get_data(send_parm.encode(encoding="UTF-8"))
        local_config_http.get_Path(self.url)

        #self.delect_class()
        self.reponse=local_config_http.set_post()

        self.checkResult()

    def description(self):
        return  self.case_name

    def checkResult(self):
        commom.show_return_msg(self.reponse,self.case_name,self.parameter)
        self.header = self.reponse.headers
        if self.header["Content-Type"] == "application/octet-stream;charset=UTF-8":
            self.info = self.reponse.text
            self.assertIsNotNone(self.info, msg=None)
        elif self.header["Content-Type"] == "application/json;charset=UTF-8":
            self.info = self.reponse.json()

            if self.reponse.status_code == 200 and self.info["success"] == True:
                self.assertEqual(self.info["code"], int(float(self.code)))
                self.assertEqual(self.info["message"], self.message)
            elif self.reponse.status_code == 200 and self.info["success"] == False:
                self.assertEqual(self.info["code"], int(float(self.code)))
                self.assertIn(self.info["message"], self.message)

    def select_classId(self):
        sql = "select class_id from cs_summary_class where class_name like '你%' and tenant_id='149' "
        print(sql)
        classId = commom.getSelect_dataBase(sql)
        print(classId)
        return classId

    def delect_class(self):
        send_dict=json.loads(self.parameter)
        for className in send_dict:
            if className!="":
                sql="DELETE from cs_summary_class where class_name="+"'"+send_dict[className]+"'"
                print(sql)
                commom.getDelecte_dataBase(sql)
'''
    def select_classId(self):
        sql="select class_id from cs_summary_class where class_name='你'"
        print(sql)
        classId=commom.get_dataBase(sql)
        print(classId)
        return classId
'''




if __name__=="__main__":
    unittest.main()





