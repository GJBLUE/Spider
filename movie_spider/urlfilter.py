# -*- coding:utf-8 -*-# -*- coding:utf-8 -*-
import time
import os
import urlparse
import hashlib
import sys
sys.path.append("..")


reload(sys) 
sys.setdefaultencoding("utf-8") 

SIMILAR_SET = set()
REPEAT_SET = set()

def format(url):
    
    if urlparse.urlparse(url)[2] == '':
        url = url+'/'

    url_structure = urlparse.urlparse(url)
    netloc = url_structure[1]
    path = url_structure[2]
    query = url_structure[4]
    
    temp = (netloc,tuple([len(i) for i in path.split('/')]),tuple(sorted([i.split('=')[0] for i in query.split('&')])))
    #print temp
    return temp


def check_netloc_is_ip(netloc):
 
    flag =0
    t = netloc.split('.')
    for i in t:
        try:
            int(i)
            flag += 1
        except Exception, e:
            break
    if flag == 4:
        return True
    
    return False

def url_domain_control(url,keyword):

    t = format(url)
    if check_netloc_is_ip(t[0]):
        return True

    elif str(type(keyword)) == "<type 'list'>":
        for i in keyword:
            if i.lower() in t[0].lower():
                return True

    elif str(type(keyword)) == "<type 'str'>":
        if keyword.lower() in t[0].lower():
            return True
    return False

def url_domain_control_ignore(url,keyword):

    t = format(url)
    for i in keyword:
        if i in t[0].lower():
            return False
    return True

def url_similar_control(url):

    t = format(url)
    if t not in SIMILAR_SET:
        SIMILAR_SET.add(t)
        return True
    return False


def url_format_control(url):

    if '}' not in url and '404' not in url and url[0].lower() == 'h' and '/////' not in url and len(format(url)[1]) < 6:
        if len(format(url)[2]) > 0:
            for i in format(url)[2]:
                if len(i) > 20:
                    return False
        if 'viewthread' in url or 'forumdisplay' in url:
            return False
        return True
    return False

def url_custom_control(url):
   
    for i in CUSTOM_KEY:
        if i in url:
            return False
    return True

def url_custom_focus_control(url,focuskey):

    if len(focuskey) == 0:
        return True
    for i in focuskey:
        if i in url:
            return True
    return False

def url_repeat_control(url):

    if url not in REPEAT_SET:
        REPEAT_SET.add(url)
        return True
    return False

def url_filter_similarity(url,keyword,ignore_keyword,focuskey):
    if url_format_control(url) and url_similar_control(url) \
                and url_domain_control(url,keyword) and url_domain_control_ignore(url,IGNORE_KEY_WORD) \
                    and url_custom_control(url) and url_custom_focus_control(url,focuskey):
        return True
    else:
        return False

def url_filter_no_similarity(url,keyword,ignore_keyword,focuskey):
    if url_format_control(url) and url_repeat_control(url) \
                and url_domain_control(url,keyword) and url_domain_control_ignore(url,IGNORE_KEY_WORD) \
                    and url_custom_control(url) and url_custom_focus_control(url,focuskey):
        return True
    else:
        return False
