import json
import unittest

import paramunittest as paramunittest

from common import commom,  configHTTP
from common.Log import Log


local_Config_Http=configHTTP.Config_Http()
v4SaveConfig_excel=commom.get_excel("testCase.xlsx","v4SaveConfig")
@paramunittest.parametrized(*v4SaveConfig_excel)
class evaluationConfigSave(unittest.TestCase):
    def setUp(self):
        pass

    def setParameters(self,case_name,method,url,parameter,code,status,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        self.message=str(message)

    def test_v4SaveConfig(self):
        login_cookies=commom.get_customer_login()
        local_Config_Http.get_cookies(login_cookies)
        header={"Content-type":"application/json;charset=UTF-8","Cookie":login_cookies}
        local_Config_Http.get_Heardes(header)
        local_Config_Http.get_Path(self.url)
        local_Config_Http.get_data(self.parameter.encode(encoding="utf-8"))
        parameter_dict=eval(self.parameter)
        v4name=parameter_dict["robotId"]
        print(v4name)
        v4name_select_sql="select robot_id from cs_robot_config"
        v4chatbot_name=commom.getSelect_dataBase(v4name_select_sql)
        print(v4chatbot_name)

        if v4name in v4chatbot_name[0][0] :
            v4name_delect_sql = "DELETE from cs_robot_config where robot_id=" + "'" + v4name + "'"
            commom.getDelecte_dataBase(v4name_delect_sql)
            self.reponse = local_Config_Http.set_post()
            print(self.reponse.text)
            self.checkResult()

        else:
            self.reponse = local_Config_Http.set_post()
            print(self.reponse.text)
            self.checkResult()

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
                self.assertIn(self.message,self.info["message"])
    def tearDown(self):
        pass
if __name__=="__main__":
    unittest.main()




