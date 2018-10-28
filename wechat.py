#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import json
import fcntl

CorpId = "xxxxxxxxxx"
Secret = "yyyyyyyyyy"
AgentId = "1000002"
AccessTokenUri = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
AppMsgSendUri = "https://qyapi.weixin.qq.com/cgi-bin/message/send"


class AccessTokenError(BaseException):
    def __init__(self, err=None):
        super(AccessTokenError, self).__init__(err)


class WechatAlert(object):
    def __init__(self, subject, content):
        self.subject = subject
        self.content = content

    def get_access_token(self):
        params = {"corpid": CorpId,
                  "corpsecret": Secret
                  }
        params = urllib.urlencode(params)
        res = urllib.urlopen("%s?%s" % (AccessTokenUri,
                                        params)).read()
        # TODO： check urlopen is right response

        self.write_to_file(res)

    def write_to_file(self, access_token):
        with open('token.json', 'w') as fd:
            # 加排他锁，其他进程既不能读也不能写
            fcntl.flock(fd.fileno(), fcntl.LOCK_EX)
            fd.write(access_token)

    def get_from_file(self):
        with open('token.json', 'a+') as fd:
            # 加共享锁,多个进程可以同时读，但其他进程不能写
            fcntl.flock(fd.fileno(), fcntl.LOCK_SH)
            fd.seek(0)
            file_content = fd.read()
            if len(file_content) > 0:
                return json.loads(file_content)
            return dict()

    def send_message(self):
        access_token = self.get_from_file().get("access_token")
        params = {"touser": "@all",
                  "toparty": "@all",
                  "totag": "@all",
                  "msgtype": "text",
                  "agentid": AgentId,
                  "text": {"content": self.content},
                  }
        res = urllib.urlopen("%s?access_token=%s"
                             % (AppMsgSendUri,
                                access_token),
                             data=json.dumps(params)).read()
        errcode = json.loads(res).get('errcode')
        if errcode == 40014:
            raise AccessTokenError
        print(errcode)

    def main(self):
        try:
            self.send_message()
        except AccessTokenError:
            self.get_access_token()
            self.send_message()


if __name__ == '__main__':
    sys.exit(WechatAlert(
        sys.argv[1],
        sys.argv[2],
    ).main())
