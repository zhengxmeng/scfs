import time
from PIL import Image
from selenium import webdriver
import json
from util.chaojiying import Chaojiying_Client
from selenium.webdriver.support.select import Select

#打开浏览器
def openUrl(url):
    #打开ie浏览器
    driver = webdriver.Chrome()
    #打开网址
    driver.get(url)
    return driver
#填写登陆信息和验证码
def setFormData(driver,username,password):
    driver.refresh()

    # 睡眠2s等待页面反应
    time.sleep(2)

    # 有iframe进行切换
    logindiv = driver.find_element_by_xpath("//iframe[@width='273']")
    divx = logindiv.location['x']
    divy = logindiv.location['y']
    driver.switch_to.frame(logindiv)

    # 获取用户输入框
    name_input = driver.find_element_by_id('userCode')  # 找到用户名的框框
    name_input.clear()
    # 赋值
    name_input.send_keys(username)  # 填写用户名
    time.sleep(0.2)

    # password是隐藏的，设置为显示
    js = "document.getElementById('password').style.display='block'"  # 编写JS语句
    driver.execute_script(js)  # 执行JS
    pass_input = driver.find_element_by_id('password')  # 找到输入密码的框框
    pass_input.clear()
    pass_input.send_keys(password)  # 填写密码
    time.sleep(0.2)

    # 验证码
    ce = driver.find_element_by_id("imgId")  # 具体的id要用F12自行查看
    cex = ce.location['x'] + divx + 1
    cey = ce.location['y'] + divy
    right = ce.size['width'] + cex
    height = ce.size['height'] + cey

    filename = "yzm/code_full.png"
    driver.save_screenshot(filename)

    im = Image.open('yzm/code_full.png')
    img = im.crop((cex, cey, right, height))
    filename = "yzm/yzm_code.png"
    img.save(filename)

    # 解析验证码
    chaojiying = Chaojiying_Client('908968241', '908968241', '901929')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('yzm/yzm_code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    code_json = chaojiying.PostPic(im, 1902)
    yzm_code = code_json['pic_str']
    #yzm_code = '2222'
    print(yzm_code)

    yzm = driver.find_element_by_id("validateCode")
    yzm.clear()
    # 赋值
    yzm.send_keys(yzm_code)  # 填写验证码

    time.sleep(0.2)

    # 获取登陆按钮id进行模拟点击
    login_button = driver.find_element_by_id('login_btn')  # 找到登录按钮
    login_button.click()  # 点击登录
    return driver

#填写基本信息
def setInfo(driver):
    print('登陆成功')
    # 登陆成功
    time.sleep(2)
    # 登记入口
    driver.find_element_by_xpath("//a[@href='/rs/register/initreg.do']").click()
    time.sleep(2)
    if 1 == 2:
        print('应收账款质押登记')
    elif 2 == 2:
        print('应收账款转让登记')
        # 应收账款质押登记
        driver.find_element_by_id("A00200").click();
        time.sleep(2)
        # 选择是
        driver.find_element_by_xpath("//input[@value='yes']").click()
        time.sleep(2)
        driver.find_element_by_id("next").click()
        time.sleep(2)

        #设置基本信息 select_by_value() / select_by_visible_text()
        Select(driver.find_element_by_id("timelimit")).select_by_value('1.0')
        time.sleep(0.2)
        driver.find_element_by_id('title').send_keys('HTBH20191021')
        time.sleep(0.2)
        #保存 填表人/基本信息
        driver.find_element_by_xpath("//input[@type='submit']").click()

        time.sleep(2)
        #增加出让人
        driver.find_element_by_id("addDebtor").click()
        time.sleep(0.2)
        #设置出让人类型
        Select(driver.find_element_by_id("debtorType")).select_by_value('02')

    else:
        print('租赁登记')

def main():
    url = 'https://www.zhongdengwang.org.cn/zhongdeng/index.shtml'  # url中指明定位到中等网首页
    user = "lvjunfeng"
    pw = "lvjunfeng123"

    #打开浏览器
    driver = openUrl(url)
    #输入登陆信息
    driver = setFormData(driver,user,pw)
    #登陆失败时重复次数
    login_count = 6
    #登陆状态
    login_state = 0
    # for num in range(6):
    #     print('开始循环')
    #     # 判断是否成功
    #     login_button = driver.find_element_by_id('login_btn')
    #     print(login_button)
    #     if login_button:
    #         #登陆失败
    #         if num < login_count:
    #             time.sleep(8)
    #             setFormData(driver,user,pw)
    #     else:
    #         print('登陆成功')
    #         login_state = 1
    #         break
    if login_state == 0:
        setInfo(driver)

    time.sleep(10)
if __name__ == '__main__':
    main()

