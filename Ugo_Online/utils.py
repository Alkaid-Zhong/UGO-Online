from message.models import Message


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
