from zhipuai import ZhipuAI

# from message.models import Message


def get_error_message(errors):
    for field, error_list in errors.items():
        if isinstance(error_list, dict):
            return get_error_message(error_list)  # 递归找到第一个错误
        elif isinstance(error_list, list):
            for error in error_list:
                if isinstance(error, dict):
                    return get_error_message(error)  # 如果是嵌套的字典，继续递归
                else:
                    return str(error)  # 直接返回第一个错误信息
        else:
            return str(error_list)


def new_message(user, message, order_id, shop_id):
    # print(user, message)
    return Message.objects.create(
        user=user,
        content=message,
        order_id=order_id,
        shop_id=shop_id
    )


def generate_product_introduction(name):
    client = ZhipuAI(api_key="dd298178f76a36d1c261c6bdb5daa560.QdaFb4f3V327xa9C")

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "user",
                "content": f"请你为我的商品 \"{name}\" 撰写一段30字以上，50字以内的描述，尽可能描述商品的特性与优点，使得买家的购买欲上涨。\n\n"
                           f"注意，你生成的描述必须被放在一个代码框中，用```text```包裹。\n\n"
            }
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        stream=True,
        tools=[{"type": "web_search", "web_search": {"search_result": True}}],
    )

    res = ""
    for chunk in response:
        if chunk.choices[0].finish_reason == "stop":
            break
        res += chunk.choices[0].delta.content

    res = res.replace("```text\n", "").replace("\n```", "")

    return res


def betterize_introduction(name, introduction):
    client = ZhipuAI(api_key="dd298178f76a36d1c261c6bdb5daa560.QdaFb4f3V327xa9C")

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "user",
                "content": f"我正在为我的商品 \"{name}\" 撰写商品描述，请你对现有的商品描述进行润色，使其尽可能描述商品的特性与优点，使得买家的购买欲上涨，必要时可以进行扩写。注意，润色后的商品描述字数必须限制在30字以上，50字以内。\n\n"
                           f"现有的商品描述：{introduction}\n\n"
                           f"注意，你生成的描述必须被放在一个代码框中，用```text```包裹。\n\n"
            }
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        stream=True,
        tools=[{"type": "web_search", "web_search": {"search_result": True}}],
    )

    res = ""
    for chunk in response:
        if chunk.choices[0].finish_reason == "stop":
            break
        res += chunk.choices[0].delta.content

    res = res.replace("```text\n", "").replace("\n```", "")

    return res

if __name__ == '__main__':
    print(betterize_introduction("iphone 16", "苹果手机，拍照清晰，使用流畅，非常好用！"))
    print(generate_product_introduction("iphone 16"))
