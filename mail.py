import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

if __name__ == '__main__':
  
    # 发送邮件服务器地址
    smtp_server = 'smtp.163.com'
    # 发送方账号
    sender = 'lewamlyn@163.com'
    # 发送方密码（或授权密码）
    password = str(sys.argv[1])

    # 收件方邮箱
    # jin mei ju hao jiao
    names = ['604504800@qq.com','3180106149@zju.edu.cn','22231084@zju.edu.cn','3180106149@zju.edu.cn','22231084@zju.edu.cn']
    if time.localtime().tm_wday > 4:
        change = 0 
        # 获取轮班信息
        try:
            with open('./week.txt', 'r') as f:
                for line in f.readlines():
                    change = int(line)
                    receiver = names[change]
                    change = (change + 1) % 5
                    print(change)
            f.close
            with open('./week.txt', 'w') as f:
                f.write(str(change))
            f.close()
        except:
            print('无本地存储信息')
            with open('./week.txt', 'w') as f:
                f.write(str(time.localtime().tm_wday))    
            f.close()
    else:
        receiver = names[time.localtime().tm_wday]

    # 邮件标题
    subject = 'SCDA小助手上班啦！(●ˇ∀ˇ●)'
    # 邮件内容
    if time.localtime().tm_hour < 12:
        mail_msg = """
                    <p>每日日报：每日新闻 + 宣讲会</p>
                    <p><a href="https://www.career.zju.edu.cn/">浙大就业指导与服务中心</a></p>
                    """
    else:   
        mail_msg = """
                    <p>社群招聘信息汇总</p>
                    """
    print(receiver)

    message = MIMEText(mail_msg, 'html', 'utf-8')  # 发送内容 （文本内容，发送格式，编码格式）
    # 发送地址
    message['From'] = sender
    # 接受地址
    message['To'] = receiver
    # 邮件标题
    message['Subject'] = Header(subject,'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_server)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, message.as_string())
        print('success:发送成功')
    except smtplib.SMTPException:
        print('error:邮件发送失败')
    finally:
        smtp.quit()
