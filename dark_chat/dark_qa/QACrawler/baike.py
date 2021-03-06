# coding:utf8

import os

from dark_chat.dark_qa.tools import HtmlTools as To


def get_info(basicInfo_block):
    info = {}
    # basicInfo_left = basicInfo_block.contents[1]
    # basicInfo_right = basicInfo_block.contents[2]
    for bI_LR in basicInfo_block.contents[1:3]:
        for bI in bI_LR:
            if bI.name == None:
                continue
            # print bI.name
            # print bI.string
            if bI.name == 'dt':
                tempName = ''
                for bi in bI.contents:
                    tempName += bi.string.strip().replace(u" ",u"")
            elif bI.name == 'dd':
                # print bI.contents
                info[tempName] = bI.contents
    return info

'''
根据实体和属性查询百科列表中的属性值
'''
def query(entity,attr):
    soup = To.get_html_baidu("http://baike.baidu.com/item/"+entity)
    basicInfo_block = soup.find(class_= 'basic-info cmn-clearfix')
    if basicInfo_block == None:
        # print 'info None'
        return attr + "::找不到"
    else:
        info  = get_info(basicInfo_block)
        # for i in info:
        #     print i
        #     print info[i]
        # print '-----------'
        if attr in info:
            return info[attr]
        else:
            # print 'no key 进行同义词判断'
            # 同义词判断
            attr_list = T.load_baikeattr_name(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/Attribute_name.txt')
            attr = T.load_synonyms_word_inattr(attr,os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/SynonDic.txt',attr_list)
            if attr in info:
                return info[attr]
            else:
                return attr + "::找不到"

