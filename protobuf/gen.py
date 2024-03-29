# coding=utf8

import os
import datetime
from collections import OrderedDict

ProtocFileCsv = 'game.csv'
toFileName = os.path.join('..', 'src', 'proto', 'pn.py')

protoNoMap = OrderedDict()
protocolNoMapStr = ""

codeStr = """# coding=utf8
# Generated file time {nowTime} DO NOT EDIT!

import json
from proto import xx_pb2


{protoDefineStr}

class DictGpb(dict):
    def SerializeToString(self):
        return json.dumps(self).encode()
    
    def MergeFromString(self, data):
        tmp = json.loads(data)
        self.update(tmp)


ruleMap = {{
{protocolNoMapStr}
}}


def getProtocolReq(no):
    req = ruleMap[no][0]
    return req() if req else req
    

def getProtocolResp(no):
    resp = ruleMap[no][1]
    return resp() if resp else resp 


def getProtocFunc(no):
    return ruleMap[no][2]


def registerProtocol(no):
    def registerHandler(handler):
        rule = ruleMap.get(no)
        if not rule:
            raise ValueError('No such protocol', no)
        if rule[2]:
            raise ValueError('Protocol already registered', no)
        rule[2] = handler            
        return handler

    return registerHandler

"""


def doLine(line, lineNo):
    global protocolNoMapStr
    # print(line)
    no, protoName, req, resp, pbFile = line.split(',')
    no = int(no)
    pbName = pbFile.split('.')[0]
    pbName = pbName + '_pb2'

    noName = 'protoc{protoName}'.format(protoName=protoName)
    if no in protoNoMap:
        raise ValueError("protocol double define", no, line, lineNo)
    protoNoMap[no] = noName

    if req in ('DictGpb',):
        reqName = req
    else:
        reqName = '{pbName}.{req}'.format(pbName=pbName, req=req) if req else None
    if resp in ('DictGpb',):
        respName = resp
    else:
        respName = '{pbName}.{resp}'.format(pbName=pbName, resp=resp) if resp else None

    _str = "    {noName}: [{reqName}, {respName}, None],\n".format(
        noName=noName,
        reqName=reqName,
        respName=respName,
    )

    protocolNoMapStr += _str
    return


def doFile():
    lineNo = 0
    with open(ProtocFileCsv) as f:
        for line in f:
            lineNo += 1
            if lineNo == 1:
                continue
            line = line.strip()
            if not line:
                continue
            doLine(line, lineNo)
    doCache()
    return


def doCache():
    # protocol Define
    protoDefineStr = ""
    for no, noName in protoNoMap.items():
        line = '{noName} = {no}\n'.format(noName=noName, no=no)
        protoDefineStr += line

    # format code
    _str = codeStr.format(
        nowTime=datetime.datetime.now(),
        protoDefineStr=protoDefineStr,
        protocolNoMapStr=protocolNoMapStr,
    )
    with open(toFileName, 'w') as f:
        f.write(_str)
    return


if __name__ == '__main__':
    doFile()
