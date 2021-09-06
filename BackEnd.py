# -*- coding: utf-8 -*-
import json
from flask import Flask,request
app = Flask(__name__)


# 浏览器向链接发送Post请求获取数据
@app.route('/getData',methods=['POST'])
def getData():
    responseDict = json.loads(str(request.get_data(), "utf8"))
    userid = responseDict.get('userid')
    print("userid: "+str(userid))
    return {
            'graph': {
                'nodes': ['Node 1', 'Node 2', 'Node 3', 'Node 4'],  # 节点 id 列表
                'edges': [['Node 2', 'Node 1', 'Edge 1'],           # 表示一条边：[起点、终点、边标签值]      
                          ['Node 1', 'Node 3', 'Edge 2'], 
                          ['Node 2', 'Node 3', 'Edge 3'], 
                          ['Node 1', 'Node 4', 'Edge 4']]
            },
            'options': ["Option 1", "Option 2", "Option 3"],
            'queryid': "111",
            'text': "This is some description text."
        }


# 浏览器将用户交互结果通过此链接Post至后端
@app.route('/returnResult',methods=['POST'])
def returnResult():
    responseDict = json.loads(str(request.get_data(), "utf8"))
    result = responseDict.get('result')
    userid = responseDict.get('userid')
    queryid = responseDict.get('queryid')
    print("result: "+str(result))
    print("userid: "+str(userid))
    print("queryid: "+str(queryid))
    return "OK"


# 开启服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 0.0.0.0代表本机任何地址均可访问