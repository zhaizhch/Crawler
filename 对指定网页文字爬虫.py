import requests
from bs4 import BeautifulSoup
import json
import time
#使用cookie登录网页
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","Cookie": "XSRF-TOKEN=783dbfa2-dd07-4b2c-a875-9041e36b9bb2; PRODSESSION=c3594b62-2260-4517-ac44-5c7170cc842c"}
#所要爬虫的页面
url_first="http://wsxy.chinaunicom.cn/api/exam/question/getQuestionListAndAnswerList?knowledgeId=4205&userGroupId=11392008&page="
url_end="&size=1000"
#文件所写入内容保存的位置
f=open('题库.txt','w',encoding='utf-8')
questionNumber=0
dict={}
#循环遍历，直至保存题目总数与题库中总数相同（每次访问访问会随机刷新题目序号）
flag=1
pagNum=0
while(True):    
    print("pagNum:")
    print(++pagNum)
    print("程序启动")
    #每页最多有两千条信息，所以必须分页查询，共9995条数据，1000条（size)*10页
    for url_middle in range(10):
        url=url_first+str(url_middle)+url_end
        respone=requests.get(url=url,headers=headers)
        html = respone.text
        Json=json.loads(html)
        print(url_middle)
        content=Json['content']
        for i in range(len(content)):
            #判断该题目是否已经写入文件中
            if content[i]['queId'] in dict:
                continue
            dict[content[i]['queId']]=1
            #题目序号
            f.writelines(str(questionNumber+1))
            print(questionNumber)
            questionNumber=questionNumber+1
            if questionNumber==9995:
                flag=0
            f.writelines(".")
            #判断题
            if content[i]['typeCode']=="PD":
                f.writelines(content[i]['casual']+"\n")
                f.writelines("答案：")
                f.writelines(content[i]['answerList'][0]['answerText']+"\n")
                f.writelines("答案是否正确（Y为正确，N为错误）：")
                f.writelines(content[i]['answerList'][0]['isCorrect']+"\n")
            #单选题
            if content[i]['typeCode']=="DANX":
                f.writelines(content[i]['casual']+"\n")    
                for j in range(len(content[i]['answerList'])):
                    if j==0:
                        f.writelines("A. ")
                    if j==1:
                        f.writelines("B. ")
                    if j==2:
                        f.writelines("C. ")
                    if j==3:
                        f.writelines("D. ")
                    f.writelines(content[i]['answerList'][j]['answerText']+"\t")
                    if j==len(content[i]['answerList'])-1:
                         f.writelines("\n")
                f.writelines("答案：")
                for j in range(len(content[i]['answerList'])):
                    if(content[i]['answerList'][j]['isCorrect']=="Y"):
                        if j==0:
                            f.writelines("A")
                        if j==1:
                            f.writelines("B")
                        if j==2:
                            f.writelines("C")
                        if j==3:
                            f.writelines("D")
                    if j==len(content[i]['answerList'])-1:
                         f.writelines("\n")
            #多选题
            if content[i]['typeCode']=="DUOX":
                f.writelines(content[i]['casual']+"\n")    
                for j in range(len(content[i]['answerList'])):
                    if j==0:
                        f.writelines("A. ")
                    if j==1:
                        f.writelines("B. ")
                    if j==2:
                        f.writelines("C. ")
                    if j==3:
                        f.writelines("D. ")
                    f.writelines(content[i]['answerList'][j]['answerText']+"\t")
                    if j==len(content[i]['answerList'])-1:
                         f.writelines("\n")
                f.writelines("答案：")
                for j in range(len(content[i]['answerList'])):
                    if(content[i]['answerList'][j]['isCorrect']=="Y"):
                        if j==0:
                            f.writelines("A")
                        if j==1:
                            f.writelines("B")
                        if j==2:
                            f.writelines("C")
                        if j==3:
                            f.writelines("D")
                    if j==len(content[i]['answerList'])-1:
                         f.writelines("\n")
    #程序休眠，短时间内题目序号不会乱序
    if flag==0:
        break
    print("sleee")
    time.sleep(180)
    
#关闭文件    
f.close()