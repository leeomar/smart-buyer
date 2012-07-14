#!/usr/bin/env python
#-*-coding:utf-8-*- 

"""汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。
"""

__author__="internetsweeper <zhengbin0713@gmail.com>; havywong <wanghewei@myhexin.com>"
__date__="2011-09-21"

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def is_qj_alphabet(uchar):
    """判断一个unicode是否是全角英文字母"""
    if (uchar >= u'\uFF21' and uchar<=u'\uFF3A') or (uchar >= u'\uFF41' and uchar<=u'\uFF5A'):
        return True
    else:
        return False

def is_qj_number(uchar):
    """判断一个unicode是否是全角数字"""
    if uchar >= u'\uFF10' and uchar <= u'\uFF19':
        return True
    else:
        return False

def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

def B2Q(uchar):
    """半角转全角"""
    inside_code=ord(uchar)
    if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
        return uchar
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code=0x3000
    else:
        inside_code+=0xfee0
    return unichr(inside_code)

def Q2B(uchar):
    """全角转半角"""
    inside_code=ord(uchar)
    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0
    if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)

def PartQ2B(uchar):
    """只对字母,数字和星号做全角转半角"""
    inside_code=ord(uchar)
    if inside_code==0xFF0A: #全角星号
        inside_code=0x002A
    elif is_qj_alphabet(uchar): #全角字母
        inside_code-=0xfee0
    elif is_qj_number(uchar): #全角数字
        inside_code-=0xfee0
        
#    if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
#        return uchar
    return unichr(inside_code)

def stringPartQ2B(ustring):
    """把字符串中字母和星号全角转半角"""
    return "".join([PartQ2B(uchar) for uchar in ustring])

def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()

def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""
    retList=[]
    utmp=[]
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp)==0:
                continue
            else:
                retList.append("".join(utmp))
            utmp=[]
        else:
            utmp.append(uchar)
    if len(utmp)!=0:
        retList.append("".join(utmp))
    return retList

if __name__=="__main__":
    ustring=u'中国 人名ａ高频Ａ１２３４５６７８９０'
    print ustring
    ret=stringPartQ2B(ustring)
    print ret
    print stringQ2B(ustring)
