#coding:utf8
from flask import *
import json
import time
from hashlib import md5
import redis
import threading

app =  Flask(__name__)
app.config.from_object("config")

user = {}
uid = 1
uidToName = {}
messages = []

def fetchMsg():
    rs = redis.Redis('localhost')
    ps = rs.pubsub()
    ps.subscribe('match_1')

    for item in ps.listen():
        print item['channel'], ':', item['data']
            
        

t = threading.Thread(target=fetchMsg)
t.daemon = True
t.start()


@app.route('/user/login', methods=['POST'])
def login():
    ln = request.args.get('loginName', None, type=str)
    pw = request.args.get('password', None, type=str)
    print ln
    if user.get(ln) == None:
        return json.dumps(dict(state=0, err='用户名错误'))
    if user.get(ln)['pw'] != pw:
        return json.dumps(dict(state=0, err='密码错误'))
    
    ud = user[ln]
    return json.dumps(dict(state=1, uid=user.get(ln)['uid'], udata=ud))


#store some token timeout used
@app.route('/user/register', methods=['POST'])
def register():
    ks = ['loginName', 'password']
    #'realName', 'phoneNumber', 'bio']
    regTime = int(time.time())
    res = {}
    for k in ks:
        res[k] = request.form.get(k, None, type=str)
    if user.get(res['loginName']) != None and user[res['loginName']]['stage'] == 1:
        return json.dumps(dict(state=0, err="该用户名已经被注册过了"))
    global uid
    k = str(uid)+str(int(time.time()))
    v = md5(k)
    user[res['loginName']] = {'uid':uid, 'pw':res['password'], 'stage':0, 'token':v.hexdigest(), 'loginName':res['loginName']}
    global uidToName
    uidToName[uid] = res['loginName']
    uid += 1
    return json.dumps(dict(state=1, uid=uid-1))

#need to fill nickName
#完成了注册流程 
@app.route('/user/finReg', methods=['POST'])
def finReg():
    uid = request.form.get('uid', None, type=int)
    nickname = request.form.get('nickname', None, type=str)
    head = request.form.get('head', None, type=str)

    global uidToName
    print uid, nickname
    print json.dumps(user)
    print json.dumps(uidToName)
    un = uidToName[uid]
    print un
    ud = user[un]
    ud['nickname'] = nickname
    ud['stage'] = 1
    #用户头像数据
    if head != None:
        ud['head'] = head

    return json.dumps(dict(state=1))

@app.route('/user/head', methods=['GET'])
def head():
    uid = request.args.get('uid', None, type=int)
    head = user[uidToName[uid]]['head']
    return json.dumps(dict(head=head))

channelInfo = {}
#获取频道用户信息 主要uid 昵称 头像信息
@app.route('/getChatInfo', methods=['GET'])
def getChatInfo():
    cid = request.args.get('cid', None, type=int)
    cha = channelInfo.get(cid, [])
    return json.dumps(dict(channel=cha))

@app.route('/enterChannel', methods=['POST'])
def enterChannel():
    uid = request.form.get('uid', None, type=int)
    cid = request.form.get('cid', None, type=int)
    users = channelInfo.setdefault(cid, [])
    users.append({'uid':uid})
    print 'enterChannel', uid, cid
    print channelInfo[cid]
    return json.dumps(dict(state=1))

@app.route('/match/<int:cid>', methods=['POST', 'PUT'])
def enterC(cid):
    if request.method == 'POST':
        uid = request.form.get('userid', None, type=int)
        users = channelInfo.setdefault(cid, [])
        users.append({'uid':uid})
        print 'enterChannel', uid, cid
        print channelInfo[cid]
        return json.dumps(dict(state=1))
    else:
        uid = request.form.get('userid', None, type=int)
        #cid = request.form.get('cid', None, type=int)
        cha = channelInfo.get(cid)
        if cha != None:
            i = 0
            for v in cha:
                if v['uid'] == uid:
                    cha.pop(i)
                    break
                i += 1
        return json.dumps(dict(state=1))



@app.route('/exitChannel', methods=['POST'])
def exitChannel():
    uid = request.form.get('uid', None, type=int)
    cid = request.form.get('cid', None, type=int)
    cha = channelInfo.get(cid)
    if cha != None:
        i = 0
        for v in cha:
            if v['uid'] == uid:
                cha.pop(i)
                break
            i += 1
    return json.dumps(dict(state=1))

@app.route('/getUserCount', methods=['GET'])
def getUserCount():
    cid = request.args.get('cid', None, type=int)
    cha = channelInfo.get(cid)
    print cid
    if cha != None:
        print 'channel not empty'
        return json.dumps(dict(count=len(cha)))

    return json.dumps(dict(count=0))



#每个用户加一个timer 回调函数 超过时间没有心跳就认为退出了游戏了



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


@app.route('/match/<int:cid>/user', methods=['GET'])
def matchuser(cid):
    return json.dumps(dict(state=1, data=[
        {'user_id':1, 'real_name':'小明', 'avatar':'abc', 'like_team': 1},
        {'user_id':2, 'real_name':'小王', 'avatar':'abc', 'like_team': 2},
        {'user_id':3, 'real_name':'小勇', 'avatar':'abc', 'like_team': 3},
        ]))


@app.route('/match/<int:startTime>/<int:endTime>', methods=['GET'])
def getMatches(startTime, endTime):   
    print startTime, endTime
    '''
    return json.dumps(dict(state=1, matches=[
        {'id':1, 'name1':'巴西', 'name2':'克罗地亚', 'score1':0, 'score2':0, 'week':'周五', 'date':'6月13日', 'time':'04：00', 'title':'世界杯 第1轮', 'online':19}, 
        {'id':2, 'name1':'巴西', 'name2':'美国', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'00:00', 'title':'世界杯 第1轮', 'online':20},
        {'id':3, 'name1':'西班牙', 'name2':'荷兰', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'03:00', 'title':'世界杯 第1轮', 'online':22},
        {'id':4, 'name1':'智利', 'name2':'澳大利亚', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'06:00', 'title':'世界杯 第1轮', 'online':21},
        ]))
    '''

    return json.dumps(dict(state=1, data=[
        {'id':1, 'start_time':1399688620000, 'end_time':1399688720000, 'cate_name':'世界杯', 'title':'第一轮', 'host_name':'中国', 'guest_name':'巴西'}, 
        {'id':2, 'start_time':1399688730000, 'end_time':1399688820000, 'cate_name':'世界杯', 'title':'第一轮', 'host_name':'中国', 'guest_name':'巴西'}, 
        {'id':3, 'start_time':1399688830000, 'end_time':1399688920000, 'cate_name':'世界杯', 'title':'第一轮', 'host_name':'中国', 'guest_name':'巴西'}, 
        {'id':4, 'start_time':1399688830000, 'end_time':1399688920000, 'cate_name':'世界杯', 'title':'第一轮', 'host_name':'中国', 'guest_name':'巴西'}, 
        {'id':5, 'start_time':1399688830000, 'end_time':1399688920000, 'cate_name':'世界杯', 'title':'第一轮', 'host_name':'中国', 'guest_name':'巴西'}, 
        #{'id':2, 'name1':'巴西', 'name2':'美国', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'00:00', 'title':'世界杯 第1轮', 'online':20},
        #{'id':3, 'name1':'西班牙', 'name2':'荷兰', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'03:00', 'title':'世界杯 第1轮', 'online':22},
        #{'id':4, 'name1':'智利', 'name2':'澳大利亚', 'score1':0, 'score2':0, 'week':'周六', 'date':'6月14日',  'time':'06:00', 'title':'世界杯 第1轮', 'online':21},
        ]))

import base64


@app.route('/message/<int:cid>/<int:startTime>/<int:endTime>', methods=['GET'])
def message(cid, startTime, endTime):
    return json.dumps(dict(state=1, data=[
        {'user_id':1, 'type':'text', 'content':base64.b64encode('我是中国人')},
        {'user_id':2, 'type':'text', 'content':base64.b64encode('你为什么不来呢')},
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
