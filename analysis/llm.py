import openai


class Client:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key='sk-af0b3ac1c57842529548347645ca81b5',
            base_url=(
                'https://api.deepseek.com'
            )
        )


    def statistics(self, content):
        completion = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content":
                        """
                        用户将提供给你一段格式化的数据，而你作为一个经验丰富的产品经理，能够在用户提供的数据中，找到热门功能和冷门功能，同时能够从产品线、产品、功能等对产品功能做出一些总结，
                        帮助用户进行产品分析和优化。
                        在用户提交的数据中 pageTitle 表示功能菜单，MPV 表示每个月的浏览量，请你分析数据内容，并提取其中的信息，以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：
                        \n\n{\n  
                            \"top10\": [
                                        {
                                        \"title\": "", 
                                        \"MPV\": , 
                                        \"function\": \"\"
                                        }
                                       ], 
                            \"top-10\": [
                                         {
                                         \"title\": \"\", 
                                         \"MPV\": , 
                                         \"function\": \"\"
                                         }
                                        ]
                          \n}
                        在以上结构中，title 为原 pageTitle 的值， MPV 为对应的 MPV 的值， function 为你根据产品和功能，预计的可能的功能
                        """
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return completion.choices[0].message.content


    def analysis(self, content):
        completion = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {
                    "role": "system",
                    "content": "用户将提供给你一段格式化的数据，而你作为一个经验丰富的产品经理，对用户提供的数据进行多角度分析，提供产品分析结果和优化建议"
                               "top10 表示对应产品 MPV(月访问量) 前十的功能，top-10 表示 MPV(月访问量) 最少的十个功能，你需要在用户提供的数据进行横向和纵向对比，首先是同一个内"
                               "是否存在重复建设的功能，其次是在多个产品之间，是否存在可能的重复建设，如果只有一个产品，仅进行产品内的横向分析，最终，你需要给出你分析的结果和优化的建议，"
                               "无需给出思考过程，但是请分析和建议尽可能专业"
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return completion.choices[0].message.content