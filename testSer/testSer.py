#coding:utf8
from flask import *
import json
import time

app =  Flask(__name__)
app.config.from_object("config")

@app.route('/login', methods=['GET'])
def login():
    ln = request.args.get('loginName', None, type=str)
    print ln

    return json.dumps(dict(state=0, id=1, loginName='xiaoming'))


@app.route('/register', methods=['POST'])
def register():
    ks = ['loginName', 'password', 'realName', 'phoneNumber', 'bio']
    regTime = int(time.time())
    res = {}
    for k in ks:
        res[k] = request.form.get(k, None, type=str)
    return json.dumps(dict(state=1, id=1, loginName='xiaoming'))

@app.route('/saveProfile', methods=['POST'])
def saveProfile():
    return json.dumps(dict(state=1))

#old password check 
#then new password
@app.route('/changePassword', methods='POST')
def changePassword():
    uid = request.form.get('uid', None, type=int)
    return json.dumps(dict(state=1))

#根据方法不同来实现 获取数据 或者 确认结果
@app.route('/confirmRequest', methods=['GET'])
def confirmRequest():
    return json.dumps(dict(request=[1, 2, 3]))

@app.route('/confirmReference', methods=['POST'])
def confirmReference():
   return json.dumps(dicti(state=1))


@app.route('/getMatches', methods=['GET'])
def getMatches():   
    return json.dumps(dict(matches=[
        {'id':1, 'name1':'巴西', 'name2':'克罗地亚', 'score1':0, 'score2':0, 'week':'周五', 'date':'6月13日', 'time':'04：00', 'title':'世界杯 第1轮', 'online':19}, 
        {'id':2, 'name1':'巴西', 'name2':'美国', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'00:00', 'title':'世界杯 第1轮', 'online':20},
        {'id':3, 'name1':'西班牙', 'name2':'荷兰', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'03:00', 'title':'世界杯 第1轮', 'online':22},
        {'id':4, 'name1':'智利', 'name2':'澳大利亚', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'06:00', 'title':'世界杯 第1轮', 'online':21},
        ]))

#@app.route('/matches', methods=['GET'])
#def getMatches():   
#    return json.dumps(dict(matches=[{'id':1, 'name1':'巴西', 'name2':'中国', 'score1':0, 'score2':0, 'status':'比赛结束', 'date':'3月5日'}, {'id':2, 'name1':'罗马尼亚', 'name2':'阿根廷', 'score1':0, 'score2':0, 'date':'今日赛程', 'status':'直播中' }]))


@app.route('/getMatchById', methods=['GET'])
def getMatchById():
    return json.dumps(dict(match={'id':3, 'name1':'巴西', 'name2':'中国', 'score1':100, 'score2':1, 'status':'比萨结束', 'date':'3月6日'}))


#join a room 
@app.route('/enterRoom', methods=['POST'])
def enterRoom():
    uid = request.form.get('uid', None, type=int)
    return json.dumps(dict(state=1))

#update online Time in channel
#after a time clear user channel information
#更新用户在线时间 心跳维持
@app.route('/updateTime', methods=['POST'])
def updateTime():
    return json.dumps(dict(state=1))


#redis 发送消息
#redis 接收消息显示
#消息格式包括用户name 名称








    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
