import jwt
import hashlib

SECRECT_KEY = 'louyanqi147'


def md5Encoding(youstr):
    m = hashlib.md5()
    m.update(youstr)
    encodingstr = m.hexdigest()
    print(encodingstr)


# 生成jwt 信息
def jwt_encoding(some, aud='webkit'):
    option = {
        'aud': aud,
        'some': some
    }
    encoded2 = jwt.encode(option, SECRECT_KEY, algorithm='HS256')
    return encoded2


# 解析jwt 信息
def jwt_decoding(token, aud='webkit'):
    decoded = jwt.decode(token, SECRECT_KEY, audience=aud, algorithms=['HS256'])
    return decoded


if __name__ == '__main__':
    d = jwt_encoding({
            "id":1,
            "username":'louyanqi',
            "email":'778617'
        })
    print(d.decode())

