from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import base64
import requests
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
def get_captcha_code(iter=3, label=False, annotation_path='data/annotation.csv'):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    img_name_list = []
    captcha_code_list = []
    cnt = 0
    if os.path.exists(annotation_path):
        df = pd.read_csv(annotation_path)
        cnt = df.shape[0]

    for i in range(iter):
        browser.get('https://npm.cpami.gov.tw/apply_2_1.aspx')
        img_base64 = browser.execute_script("""
            var ele = arguments[0];
            var cnv = document.createElement('canvas');
            cnv.width = ele.width; cnv.height = ele.height;
            cnv.getContext('2d').drawImage(ele, 0, 0);
            return cnv.toDataURL('image/jpeg').substring(22);    
            """, browser.find_element(By.XPATH, "//*[@id='xcode']/img"))
        img_name = 'captcha_' + str(cnt).zfill(4) + '.png'
        img_path = os.path.join('data/image', img_name)
        with open(img_path, 'wb') as image:
            image.write(base64.b64decode(img_base64))
        if label:
            img_name_list.append(img_name)
            captcha_code_list.append(input("please enter captcha code:"))
        cnt += 1

    if label:
        dict = {"img_name": img_name_list,  "label": captcha_code_list}
        df_new = pd.DataFrame(dict)
        if os.path.exists(annotation_path):
            df_new = pd.concat([df, df_new], axis=0)
        df_new.to_csv(annotation_path, index=False)

if __name__ == '__main__':
    get_captcha_code(iter=166, label=True)