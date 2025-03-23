import json
import os
import requests
import re
import textwrap
from excel_handler import Product, ProductGroup, ProductHolder, ExcelParser
from llm import Client

def url_cleaning(url):
    # 域名剥离
    path = re.sub(r'^(?:https?:\/\/)?[^\/]+', '', url)

    # 路径清洗
    parts = path.strip('/').split('/')
    for i in range(len(parts)):
        # 替换数字ID
        parts[i] = re.sub(r'\d+', '', parts[i])
        # 标准化版本
        if re.match(r'^v\d+$', parts[i]):
            parts[i] = '_version'
        # 过滤通用词
        if parts[i] in ['index', 'home']:
            parts[i] = ''
    # 重新组合路径，去掉空字符串
    cleaned_parts = [p for p in parts if p]
    cleaned_path = '/' + '/'.join(cleaned_parts) if cleaned_parts else ''

    # 处理可能的空路径
    if not cleaned_path:
        return 'root'

    # 语义提取
    parts = cleaned_path.strip('/').split('/')
    if len(parts) <= 3:
        semantic = '/'.join(parts)
    else:
        first_two = parts[:2]
        last_two = parts[-2:]
        combined = first_two + last_two
        semantic = '/'.join(combined)

    # 处理多余的 /
    semantic = re.sub(r'/+', '/', semantic)

    return semantic

if __name__ == '__main__':
    src = os.path.join('../source', 'data.xlsx')
    src_parser = ExcelParser(src)
    # 得到所有 sheet 页
    sheet_names = src_parser.get_sheet_names()
    # 拿到大语言模型 Client
    client = Client()
    # role = '经验丰富的产品经理，善于分析产品的热门功能和冷门功能，同时能够在多个产品直接找到一些相似功能，优化产品设计'
    role = 'user'
    # product_line product_name page_id mpv
    # 循环 sheet 页
    for sheet_name in sheet_names:
        holder = ProductHolder(src_parser.work_book, sheet_name)
        data=''
        for group in holder.product_groups:
            des = f'产品 {group.name} 共计有 {len(group.products)} 个功能页面，其详细信息如下：'
            for product in group.products:
                des += f'page_id 为 {product.page_id} 的 mpv 是 {product.mpv},'
            # 去掉最后一个逗号
            des = des[:-1]
            print(des)
        # 调用第一次大模型，让其对产品进行总结
        # for product in holder.products:
        #     # data.append(product.__dict__)
        #     product.page_id = url_cleaning(product.page_id)
        #     data += 'product_name:' + product.product_name + ',page_id:' + product.page_id +',mpv:' + str(product.mpv) + ' '
        # print(data)
        # content = json.dumps(data, indent=4, ensure_ascii=False)
        # url = "https://api.example.com/post-endpoint"
        # headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": "Bearer YOUR_TOKEN"
        # }
        # # 发送 POST 请求
        # response = requests.post(
        #     url,
        #     headers=headers,
        #     json=data  # 自动序列化为 JSON 并设置 Content-Type
        # )
        #
        # # 处理响应
        # print("状态码:", response.status_code)
        # print("响应内容:", response.json())  # 假设返回的是 JSON
        # print(content)
        # for group in holder.product_groups:
        #     for product in group.products:
        #         des += f'page_id 为 {product.page_id} 的 mpv 是 {product.mpv},'
        #     content = f'产品 {group.name} 有 {len(group.products)} 个功能页面，{des} 请告诉我当前产品他的功能菜单使用量 top10 和是使用量倒数的 top10'
        #     print(content)
        # response = client.statistics(content)
        # print(textwrap.fill(
        #     response,
        #     50
        # ))
        # 去掉一些奇怪的标记
        # response = response.replace('```', '').replace('json', '')
        # print(response)
        # data.append(response)
        # 调用第二次大模型，让其对产品进行分析，是否存在重复建设的功能
        # result = client.analysis(json.dumps(data, indent=4, ensure_ascii=False))
        # print(textwrap.fill(
        #     result,
        #     50
        # ))