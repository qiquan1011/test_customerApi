import json
import unittest

import paramunittest as paramunittest

from common import configHTTP, commom

from common.Log import Log



local_config_Http=configHTTP.Config_Http()
queerySatisfaction_excel=commom.get_excel("testCase.xlsx","querySatisfactions")
@paramunittest.parametrized(*queerySatisfaction_excel)
class querySatisfaction(unittest.TestCase):
    def setUp(self):
        pass
    def setParameters(self,case_name,method,url,parameter,code,success,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        print("self.code是：",self.code)
        self.success=str(success)
        self.message=str(message)

    def description(self):
            return self.case_name

    def test_querySatisfaction(self):
        login_cookies = commom.get_customer_login()
        header={"Content-Type":"application/json;charset=UTF-8","Cookie":login_cookies}
        local_config_Http.get_Heardes(header)
        local_config_Http.get_Path(self.url)

        local_config_Http.get_data(self.parameter.encode(encoding="utf-8"))
        self.reponse =local_config_Http.set_post()

        self.checkResult()
    def checkResult(self):
        self.info = self.reponse.json()
        commom.show_return_msg(self.reponse,self.case_name,self.parameter)

        if self.reponse.status_code == 200 and self.info["success"]==True:
            self.assertEqual(self.info["code"], int(float(self.code)))
            self.assertEqual(self.info["message"], self.message)
        elif self.reponse.status_code == 200 and self.info["success"] ==False:
            self.assertEqual(self.info["code"], int(float(self.code)))
            self.assertIn(self.info["message"], self.message)

    def tearDown(self):
        pass

if __name__=="__main__":
    unittest.main()














