# -*-coding:utf-8-*-

import csv
import time
import pyautogui
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

filename = "E:\\作业\\互联网+\\spider\\zhenbaoguan\\shuhua_info.csv"

with open(filename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    data.pop(0)

for dad in data[90:100]:
    print(dad)
    # 实例化一个Options
    chrome_options = Options()

    # 用于定义下载不弹窗和默认下载地址（默认下载地址还要再后面的commands里启动，默认是不开启的）
    # prefs = {"download.default_directory": "E:/作业/计算机设计大赛/图片/书画", "download.prompt_for_download": False, }
    prefs = {"download.prompt_for_download": True, }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path='E:/作业/互联网+/spider/zhenbaoguan/chromedriver', chrome_options=chrome_options)
    # 窗口最大化
    driver.maximize_window()
    driver.get(dad[2])

    pyautogui.rightClick(x=1000, y=500)
    pyautogui.moveRel(100, 20, duration=0.25)
    # 输入V
    pyautogui.typewrite(['V'])

    # 将地址以及文件名复制
    pic_dir = '%s.jpg' % dad[0]
    pyperclip.copy(pic_dir)

    # 等待窗口打开，以免命令冲突，粘贴失败，试过很多次才有0.8，具体时间自己试
    time.sleep(1)

    # 粘贴
    pyautogui.hotkey('ctrlleft', 'V')
    # 确认保存
    pyautogui.press('enter')

    dad[3] = 'zchsakura.top/static/painting/' + '%s.jpg' % dad[0]
    # 写入csv
    with open('../../shuhua_info_new.csv', 'a', encoding="utf-8", newline='') as file_obj:
        writer = csv.writer(file_obj)
        row = [dad[0], dad[1], dad[2], dad[3], dad[4], dad[5], dad[6], dad[7], dad[8]]
        writer.writerow(row)
    # 退出浏览器
    time.sleep(4)
    driver.quit()
