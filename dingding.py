import json
import requests

baseUrl = "https://oapi.dingtalk.com/robot/send?access_token=308d1b6cff9a59c273f5e2fab4d34fbf33d9e394b6b616e71e741aca0e84cff7"

HEADERS = {"Content-Type": "application/json; charset=utf-8"}

message = "republicty"
stringBody = {"msgtype": "text",
              "text": {"content": '{0}{1}'.format(message, "\n触发提醒")},
              "at" :{
                  "atMobiles": ["13331886953"],
                  "isAtAll":False
                    }
              }

MessageBody = json.dumps(stringBody)

try:
    result = requests.post(url=baseUrl, data=MessageBody, headers=HEADERS)
    print(result.text)
except Exception as e:
    print("消息发送失败", e)