#coding:utf8

from dark_chat.dark_qa.tools import HtmlTools as To

'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def kwquery(query):
    answer = {}
    text = ''
    # 找到答案就置1
    flag = 0


    # 抓取百度前10条的摘要
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd='+query)

    for i in range(1,10):
        if soup_baidu == None:
            break
        results = soup_baidu.find(id=i)

        if results == None:
            break
        # print '============='
        # print results.attrs
        # print type(results.attrs)
        # print results['class']
        #判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
        if 'mu' in results.attrs and i == 1 and 'nourl.baidu.com' in results.attrs["mu"] and len(results.findAll(class_='op_exactqa_item_img'))>0:
            # print results.attrs["mu"]
            answer = {'value': [], 'type': 'text', 'from': '百度图谱'}
            for result in results.findAll(class_='op_exactqa_item_img'):
                answer['value'].append(result.find("a").attrs['title'].strip())
            flag = 1
            break


        #古诗词判断
        if 'mu' in results.attrs and i == 1 and 'hanyu.baidu.com/shici' in results.attrs["mu"]:
            r = results.find(class_="op_exactqa_detail_s_answer")
            answer = {'value': r.get_text().strip(), 'type': 'text', 'from': '古诗词'}
            flag = 1
            break

        #万年历 & 日期
        # if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/calendar'):
        #     r = results.find(class_="op-calendar-content")
        #     answer.append(r.get_text().strip().replace("\n","").replace(" ",""))
        #     flag = 1
        #     break
        #
        # if 'tpl' in results.attrs and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
        #     r = results.attrs['fk'].replace("6018_","")
        #     answer.append(r)
        #     flag = 1
        #     break


        #计算器
        if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/static/calculator/calculator.html'):
            # r = results.find('div').find_all('td')[1].find_all('div')[1]
            r = results.find(class_="op_new_val_screen_result")
            answer = {'value': r.get_text().strip(), 'type': 'text', 'from': '计算器'}
            flag = 1
            break

        if results.find("h3") != None:
            # 百度知道
            if "_百度知道" in results.find("h3").text and (i == 1 or i ==2):
                url = results.find("h3").find("a")['href']
                if url == None:
                    continue
                else:
                    zhidao_soup = To.get_html_zhidao(url)

                    r = zhidao_soup.find(class_='bd answer')
                    if r == None:
                        continue
                    else:
                        r = r.find('pre')
                        if r == None :
                            r = ""
                            for prob in zhidao_soup.find(class_="answer-text"):
                                if 'class=' in str(prob) or str(prob).replace('\n','').strip() == '':
                                    continue
                                r+=(str(prob))
                    answer = {'value':str(r),'type':'text', 'from': '百度知道'}
                    flag = 1
                    break

            # 百度百科
            if "_百度百科" in results.find("h3").text:
                url = None
                if results.find(class_="wenda-abstract-showurl-link") is not None:
                    url = results.find(class_="wenda-abstract-showurl-link").attrs['href']
                if 'mu' in results.attrs:
                    url = results.attrs['mu']
                if url == None:
                    continue
                else:
                    baike_soup = To.get_html_baike(url)

                    r = baike_soup.find(class_='lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer = {'value': str(r), 'type': 'text', 'from': '百度百科'}
                    flag = 1
                    break

            # 百度图片
            if "_百度图片" in results.find("h3").text:
                for img in results.findAll("a"):
                    if 'data-objurl' in img.attrs:
                        answer = {'value': [], 'type': 'img', 'from': '百度图片'}
                        answer['value'].append(img.attrs['data-objurl'])
                        flag = 1
                        break
        text += results.get_text()

    if flag == 1:
        return answer

    #可能是百度自己的百度百科竟然不在第一页，比如袁隆平，呵呵
    baike_soup = To.get_html_baike('https://baike.baidu.com/item/' + query.strip())
    r = baike_soup.find(class_='lemma-summary')
    if r != None:
        r = r.get_text().replace("\n", "").strip()
        if len(r) > 0:
            return {'value':str(r).strip(),'type':'text', 'from': '百度百科'}

    #获取bing的摘要
    soup_bing = To.get_html_bing('https://www.bing.com/search?q='+query)
    # 判断是否在Bing的知识图谱中
    # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    bingbaike = soup_bing.find(class_="bm_box")

    if bingbaike != None:
        if bingbaike.find_all(class_="b_vList")[1] != None:
            if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
                flag = 1
                return {'value': bingbaike.get_text(), 'type': 'text', 'from': '必应百科'}
    else:
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        answer = {'value': [], 'type': 'text',  'from': '必应网典'}
        for bl in bing_list:
            temp =  bl.get_text()
            if temp.__contains__(u" - 必应网典"):
                url = bl.find("h2").find("a")['href']
                if url == None:
                    continue
                else:
                    bingwd_soup = To.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                        answer['value'].append(r)
                    flag = 1
                    break

        if flag == 1:
            return answer
    # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就放弃
    if flag == 0:
        answer = {'value': "我不知道你想问什么，会说你就多说点？", 'type': 'text', 'from': '智能分析词频'}

    return answer


# if __name__ == '__main__':
#     pass
#     query = "9*234"
#     ans = kwquery(query)
