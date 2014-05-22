curl --data "uid=1&cid=1" http://localhost:5000/enterChannel
curl --data "uid=1&cid=1" http://localhost:5000/exitChannel
curl http://localhost:5000/match/1/user -X GET
curl -x GET http://172.17.0.45:91/message/1/1402603200000/1402604200000 
