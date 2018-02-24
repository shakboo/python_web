# -*- encoding:utf-8 -*-
import requests,sys

def get_codec(from_, to):
    """ create coding converter """
    if from_ == to: # just do nothing
        return lambda s: s
    if from_ == 'unicode': # just encode
        return lambda s: s.encode(to)
    if to == 'unicode': # just decode
        return lambda s: unicode(s, from_)
    else: # decode to unicode first, then encode
        return lambda s: unicode(s, from_).encode(to)


default_encoding = 'utf-8'
# init programming coding converters
unicode_to_default = get_codec('unicode', default_encoding)
default_to_unicode = get_codec(default_encoding, 'unicode')
gbk_to_default = get_codec('gbk', default_encoding)
default_to_gbk = get_codec(default_encoding, 'gbk')
default_to_utf8 = get_codec(default_encoding, 'utf-8')
utf8_to_default = get_codec('utf-8', default_encoding)
utf8_to_unicode = get_codec('utf-8', 'unicode')
unicode_to_utf8 = get_codec('unicode', 'utf-8')


def decode_to(s, dst_encoding):
    if type(s) == unicode:
        return get_codec('unicode', dst_encoding)(s)

    encodings = ['utf-8', 'gbk']
    for encoding in encodings:
        try:
            s.decode(encoding)
        except:
            continue
        return get_codec(encoding, dst_encoding)(s)
    return s

def sendMsg(receiver, message):
    '''
    receiver: 群号或popo账号, popo账号需为好友, 账号需要带后缀, 例@corp.netease.com
    '''
    codec_to_utf8 = lambda s: decode_to(s, 'utf-8')
    message = codec_to_utf8(message)
    requests.post('http://10.246.13.110:7001/api/popo/send', data=dict(to=receiver, content=message))


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print 'params too short'
        sys.exit()
    receiver = sys.argv[1]
    message = sys.argv[2]
    codec_to_utf8 = lambda s: decode_to(s, 'utf-8')
    message = codec_to_utf8(message)
    sendMsg(receiver,message)