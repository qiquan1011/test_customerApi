import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common.configHTTP import local_Read_Config


class ProjectInfo():
    pass


# attachment, content
def send_mail(attachment, content):
    print("\033[31m开始发送测试报告......")
    # 设置邮件主题
    subject = "[" + time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())) + "] " + "customerApi自动化测试报告"
    # 构造一个MIMEMultipart对象代表邮件本身
    msg = MIMEMultipart()
    # HTML邮件正文
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = local_Read_Config.get_Email("sendmail")
    msg['To'] = ','.join(local_Read_Config.get_Email("receivemail"))
    # 添加附件
    with open(attachment, 'rb') as f:
        # MIMEBase表示附件的对象
        mime = MIMEBase('application', 'octet-stream')
        # filename是显示附件名字
        attachment_name = attachment.split("\\")[-1]
        mime.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        # 获取附件内容
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        # 作为附件添加到邮件
        msg.attach(mime)
    try:
        stmp = smtplib.SMTP_SSL(host="smtp.exmail.qq.com", port=465)
        # 连接SMTP主机
        stmp.connect(host="smtp.exmail.qq.com")
        # 登录邮箱
        stmp.login(local_Read_Config.get_Email("sendmail"), local_Read_Config.get_Email("PassKey"))
        # 邮件发送
        stmp.sendmail(local_Read_Config.get_Email("sendmail"), local_Read_Config.get_Email("receivemail"),
                      msg.as_string())
        # 断开SMTP连接
        stmp.quit()
        print("邮件发送——Success")
    except Exception as e:
        print("邮件发送——Fail" + str(e))
    print("----------------------------------------------------------\033[0m")


send_mail("C:/Users/yunwen/PycharmProjects/customerApi/result/report.html",
          "C:/Users/yunwen/PycharmProjects/customerApi/result/report.html")
