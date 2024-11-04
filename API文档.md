# 基本数据格式

后端的接口格式一般情况下遵循相对统一的标准，采用JSON格式。数据结构大致如下：

- **success** `Boolean`格式，表示是否操作成功。
- **code**`Integer`格式，表示错误代码。
  - 当**success**为`true`时，一般错误代码为`0`
  - 当**success**为`false`时，错误代码为非零（一般大于零，少数情况下为负数）
- **message** `String`格式或者`null`，表示消息。
- **data** `Object`格式或者`null`，表示传递的数据信息。

例如：

```json
{
    "success": true,
    "code": 0,
    "message": "This is message!",
    "data": {
        "example1": "This is data1!",
        "example2": "This is data2!"
    }
}
```

# 用户API文档

## 用户注册（买家）

请求路径`/user/register/customer`

请求方法`POST`

请求数据格式

- `name` 用户名
- `phone` 电话号码
- `email` 用户邮箱（作为用户唯一标识）
- `password` 密码

返回数据格式

`null`

## 用户注册（商家）

请求路径`/user/register/seller`

请求方法`POST`

请求数据格式

- `name` 商家名称
- `phone` 联系方式
- `email` 用户邮箱（作为用户唯一标识）
- `password` 密码

返回数据格式

- `null`

## 登录登出

### 用户登录

- 请求路径`/user/login`
- 请求方法`POST`
- 请求数据格式
  - `email` 用户邮箱
  - `password` 登录密码
- 返回结果格式
  - `null`

### 用户登出

- 请求路径`user/logout`
- 请求方法`POST`
- 返回结果格式
  - `null`

## 用户信息

### 账户基本信息

- 请求路径`/user/profile`
- 请求方法`GET`
- 返回结果格式
  - `name` 用户名
  - `email` 用户邮箱（作为用户唯一标识）
  - `role` 用户类别（可取值为买家`CUSTOMER`、卖家`SELLER`）