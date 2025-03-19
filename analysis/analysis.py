import json
import os

import textwrap
from excel_handler import Product, ProductGroup, ProductHolder, ExcelParser
from llm import Client

if __name__ == '__main__':
    src = os.path.join('../source', 'data.xlsx')
    src_parser = ExcelParser(src)
    # 得到所有 sheet 页
    sheet_names = src_parser.get_sheet_names()
    # 拿到大语言模型 Client
    client = Client()
    # role = '经验丰富的产品经理，善于分析产品的热门功能和冷门功能，同时能够在多个产品直接找到一些相似功能，优化产品设计'
    role = 'user'
    # 循环 sheet 页
    for sheet_name in sheet_names:
        holder = ProductHolder(src_parser.work_book, sheet_name)
        data=[]
        for group in holder.product_groups:
            # 调用第一次大模型，让其对产品进行总结
            des = ''
            for product in group.products:
                des += f'pageTitle={product.pageTitle} 的 MPV={product.MPV},'
            content = (f'产品 {group.code} 有 {len(group.products)} 个功能页面，{des} 请告诉我当前产品他的功能菜单使用量 top10 和是使用量倒数的 top10，'
                       + '跳过思考过程，直接告诉我结构化的结果')
            response = client.statistics(content)
            print(textwrap.fill(
                response,
                50
            ))
            # 去掉一些奇怪的标记
            response = response.replace('```', '').replace('json', '')
            data.append(response)
        # 调用第二次大模型，让其对产品进行分析，是否存在重复建设的功能
        result = client.analysis(json.dumps(data, indent=4, ensure_ascii=False))
        print(textwrap.fill(
            result,
            50
        ))
