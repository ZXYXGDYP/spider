'''
影评比短评要麻烦很多 因为影评的界面想要得到完整的影评就必须要点展开 
所以就要异步处理
第一步通过影评的url把所有的影评id找到
然后重新构造url 爬取影评内容
'''
from requests_html import HTMLSession
from selenium import webdriver
import time
import pandas as pd 
import numpy as np
import re
# 登陆
def login(driver,username,password):
    '''
    
    '''
    driver = driver
    login_url = 'https://accounts.douban.com/passport/login'
    
    driver.get(login_url)
    # 切换到密码
    driver.find_element_by_css_selector('li.account-tab-account').click()
    # 输入
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    # 登录
    driver.find_element_by_class_name('btn').click()
    #拿cookies
    cookies= driver.get_cookies()
    time.sleep(5) 
    print("success")
    
#  获取id列表 
def get_id_list(driver,total_page,movie_url):
    id_list = []
    page = 1
    # 先get movie_url
    driver.get(movie_url) 
    driver.implicitly_wait(3)
    #搞 list
    while page <=total_page:
        try:
            results = driver.find_elements_by_class_name('review-list')[0].find_elements_by_class_name('review-short')
            for result  in results:
                id_list.append(re.search("-?[0-9]\d*",result.get_attribute("id")).group(0))

            driver.find_element_by_class_name('next').click()
            page += 1
            time.sleep(3)
        except Exception as e:
            print(e)
            break
    return id_list 

#判断是否有element
def isElementPresent(by,value):
    #从selenium.common.exceptions 模块导入 NoSuchElementException类
    from selenium.common.exceptions import NoSuchElementException
    try:
        element = driver.find_element_by_class_name(value)
    #原文是except NoSuchElementException, e:
    except NoSuchElementException as e:
        #打印异常信息
        print(e)
        #发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
        return False
    else:
        #没有发生异常，表示在页面中找到了该元素，返回True
        return True

#  重构urls并且爬取数据
def get_review_content(driver,id_list) :
    """
    """
    
    content_df =pd.DataFrame(columns=["title","author","time","content","vote","unvote"])
    counter = 1

    for ids in id_list:
        try:
            driver.get("https://movie.douban.com/review/{}/".format(ids))
            if isElementPresent('class','taboola-open-btn')==True:
                driver.find_element_by_class_name('taboola-open-btn').click()
            title=driver.find_elements_by_tag_name('h1')[0].text
            author =driver.find_elements_by_class_name("main-hd")[0].find_elements_by_tag_name('a')[0].text
            time = driver.find_elements_by_class_name("main-hd")[0].find_elements_by_tag_name('span')[3].text
            content = driver.find_elements_by_class_name("review-content")[0].text
            vote = re.search("-?[0-9]\d*",driver.find_elements_by_class_name("useful_count")[0].text).group(0)
            unvote =  re.search("-?[0-9]\d*",driver.find_elements_by_class_name("useless_count")[0].text).group(0)
            content_df.loc[counter-1]=[title,author,time,content,vote,unvote]
            counter+=1
            print(counter)
            driver.implicitly_wait(3)
        except Exception as e:
            print(e)
            break
    return content_df

if __name__ =="__main__" :
    driver = webdriver.Chrome() 
    username = "your username"       # 输入账号
    password = "your pwd"            # 输入密码
    total_page = 10                  # 想要的页数             
    movie_url = 'https://movie.douban.com/subject/1292001/reviews' # 目标url
    login(driver,username, password)
    id_list = get_id_list(driver,total_page,movie_url)
    content_df = get_review_content(driver,id_list)
    
    content_df.to_csv("the_legend_1900.csv")

