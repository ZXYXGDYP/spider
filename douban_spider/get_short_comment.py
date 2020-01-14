"""
目前豆瓣网密码登陆还没有接入验证所以比较好爬
使用selenium实现了豆瓣网短评爬虫
包括自动登陆模块 爬取短评内容（用户名 点赞数 短评内容） 翻页功能
并储存在dataframe 中 导出为csv
ex.《海上钢琴师》
目标url：https://movie.douban.com/subject/1292001/comments?status=P
"""
from selenium import webdriver
import time
import pandas as pd 
import numpy as np
def login(driver,username,password):

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

def get_comment(driver,movie_url,total_page):
    page = 1
    counter =1
    comment_df = pd.DataFrame(columns=["u_id","u_time","u_agree","u_comment"])
    
    #进入目标url
    driver.get(movie_url) 
    #加载几秒
    driver.implicitly_wait(3)
    #开搞
    while page<=total_page :
        try:
            results = driver.find_elements_by_class_name('comment')
            for result in results:

                # 用户名的标签里没有特殊的class或者id 但是每个comment里他都是第二个
                u_id = result.find_elements_by_tag_name('a')[1].text
                u_time = result.find_element_by_class_name('comment-info').find_elements_by_tag_name('span')[1].text 
                #正规的叫法应该是vote
                u_agree = result.find_element_by_class_name('comment-vote').find_element_by_tag_name('span').text 
                u_comment = result.find_element_by_tag_name('p').text 
                comment_df.loc[counter-1]=[u_id,u_time,u_agree,u_comment]
                # print(comment_df)
                print("第{}个评论".format(counter))
                counter  += 1
            #翻页
            driver.find_element_by_class_name('next').click() 
            print("第{}页结束".format(page))
            page += 1
            time.sleep(3)
        except Exception as e:
            print(e)
            break
    return comment_df
if __name__ == '__main__':
    driver = webdriver.Chrome() 
    username = ""
    password = ""
    movie_url = 'https://movie.douban.com/subject/1292001/comments?status=P'
    total_page = 25
    login(driver,username,password)
    c_df = get_comment(driver,movie_url,total_page)
    c_df.to_csv("short_comments.csv")
