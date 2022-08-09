import base64


def encode(id, username, password):
    strs = str(id) + ' ' + username + ' ' + password
    token = base64.urlsafe_b64encode(strs.encode("utf-8")).decode()
    return token


def decode(token):
    info = base64.urlsafe_b64decode(token.encode("utf-8")).decode('utf-8')
    id, username, password = info.split(' ')
    print(id + username + password)
    return id, username


if __name__ == '__main__':
    token = encode(212, 'zhangsan', '123456')
    print("加密的token:" + token)
    print("解密后的原信息" + str(decode(token=token)))
