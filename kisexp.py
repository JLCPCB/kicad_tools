# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:08:59 2020
"""

import io

QUOTE = {
        "'":"'",
        '"':'"',        
        }
BRACKETS = {'(': ')'}
BRACKETS_END = {')':1}
SPACE = {' ':1, '\t':1, '\r':1, '\n':1}
STRING_ESCAPES = {'\\': '\\', 'n': '\n', 'r': '\r'}

def quoteData(content, index):
    data = ""
    q_e = QUOTE[content[index]]
    c_len = len(content)
    escape = False
    index+=1;
    while index < c_len:
        c = content[index]
        if escape:
            data += STRING_ESCAPES.get(c, c)
            escape = False
        elif c == '\\':
            escape = True
        elif c == q_e:
            return data, index+1
        else:
            data += c
        index+=1
    return data, index+1

def normalData(content, index):
    data = ""
    c_len = len(content)
    while index < c_len:
        c = content[index]
        if c in SPACE:
            index +=1
            break
        elif c in BRACKETS:
            break
        elif c in BRACKETS_END:
            break
        else:
            data += c
            index+=1
    return data, index

def parseSexp(content, index = 0):
    res = []
    c_len = len(content)
    data = ""
    bracket_end = ""
    while index < c_len:
        c = content[index]
        if c in BRACKETS:
            bracket_end = BRACKETS[c]
            data, index = parseSexp(content, index+1)
            res.append(data)
        elif c in QUOTE:
            data, index = quoteData(content, index)
            res.append(data)
        elif c in SPACE:
            index+=1;
        elif c in BRACKETS_END:
            index+=1
            break
        else:
            data, index = normalData(content, index)
            res.append(data)
    return res, index
        

def loadKicadNet(filename):
    file = io.open(filename, "r", encoding="utf-8")
    data = file.read()
    res = parseSexp(data)
    return res[0][0]
