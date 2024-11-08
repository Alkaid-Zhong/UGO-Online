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

错误码约定：
- `0`表示操作成功
- `300` 商店错误
- `301` 商店权限错误
- `302` 邀请码错误
- `400` 表示用户身份错误
- `401` 表示用户未登录
- `402` 表示注册失败
- `403` 表示用户名或密码错误（登陆失败）

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

### 修改密码

- 请求路径`/user/change-password`
- 请求方法`POST`
- 请求数据格式：
```json
{
    "old_password": "旧密码",
    "new_password": "新密码",
    "confirm_new_password": "确认新密码"
}
```
- 保证了更改密码后用户仍然在登陆状态

## 商店相关

### 获取所有商铺

- 请求路径：`/shop`
- 请求方法：`GET`
- 权限要求：无
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "查询所有商铺成功",
    "data": [
        {
            "id": 1,
            "name": "李四的商铺",
            "address": "上海市浦东新区",
            "description": "主营服装鞋帽",
            "create_date": "2024-11-06T11:39:56.620678Z",
            "sellers": [
                {
                    "name": "测试商家0",
                    "email": "seller1@buaa.edu.cn",
                    "role": "SELLER"
                }
            ]
        },
        {
            "id": 2,
            "name": "张三的商铺",
            "address": "北京市朝阳区",
            "description": "主营电子产品",
            "create_date": "2024-11-07T10:11:29.139915Z",
            "sellers": [
                {
                    "name": "seller2",
                    "email": "seller2@buaa.edu.cn",
                    "role": "SELLER"
                }
            ]
        }
    ]
}
```


### 创建商铺

- 请求路径：`/shop/create`
- 请求方法：`POST`
- 权限要求：需要登录，且用户角色为商家（`SELLER`），**一个商家只能管理一个商铺**
- 请求数据格式
  - `name`（字符串，必填）：商铺名称
  - `address`（字符串，可选）：商铺地址
  - `description`（字符串，可选）：商铺描述
```json
{
    "name": "张三的商铺",
    "address": "北京市朝阳区",
    "description": "主营电子产品"
}
```
- 返回结果格式
```json
{
    "success": true,
    "code": 0
}
```

### 商铺信息

- 请求路径：`/shop/<int:id>/info`
- 请求方法：`GET`
- 权限要求：无
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "id": 1,
        "name": "李四的商铺",
        "address": "上海市浦东新区",
        "description": "主营服装鞋帽",
        "create_date": "2024-11-06T11:39:56.620678Z",
        "sellers": [
            {
                "name": "测试商家0",
                "email": "seller1@buaa.edu.cn",
                "role": "SELLER"
            }
        ]
    }
}
```

## 邀请加入商店

### 商家生成商店的邀请码

- 请求路径：`/shop/<int:id>/create_invitation_code`
- 请求方法：`POST`
- 权限要求：需要认证，且用户角色为商家，并且是商铺的现有管理者
- 请求数据格式：
  - expires_in_days: 有效期，不填默认永久，填的话以天为单位
  - usage_limit：使用次数限制，不填默认为 1
- 返回数据格式
  ```json
  {
      "success": true,
      "code": 0,
      "message": "邀请码生成成功",
      "data": {
          "code": "Doz4T7pdhK4RkHUY",
          "shop": 2,
          "creator": 3,
          "is_active": true,
          "created_at": "2024-11-07T12:11:07.207874Z",
          "expires_at": null,
          "usage_limit": 1,
          "usage_count": 0
      }
  }
  ```

### 新商家使用邀请码加入商铺

- 请求路径：/shop/join_by_code
- 请求方法：POST
- 权限要求：用户为商家，且目前不是任何商铺的管理者
- 请求数据：
  ```json
  {
      "invitation_code": "ABCD1234"
  }
  ```

## 商品相关

### 创建商品

- 请求路径：`/shop/<int:id>/product/add`
- 请求方法：`POST`
- 权限要求：需要认证，且用户角色为商家，并且是商铺的现有管理者
- 请求数据格式
```json
{
  "name": ,
  "description":, 
  "price":  ,
  "stock_quantity":,
  "image": ,
}
```
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "商品创建成功",
    "data": {
        "id": 23,
        "shop": 1,
        "name": "oppo A11 pro max",
        "description": "安卓手机",
        "price": "19.90",
        "stock_quantity": 2,
        "status": "Available",
        "create_date": "2024-11-08T08:02:53.330448Z",
        "image": "/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_nXqr0kW.png"
    }
}
```

### 获取店内所有商品

- 请求路径：`/shop/<int:shop_id>/products`
- 请求方法：`GET`
- 权限要求：无
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 22,
        "next": "http://127.0.0.1:8000/shop/1/products?page=2",
        "previous": null,
        "products": [
            {
                "id": 2,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 16",
                "price": "9999.98",
                "stock_quantity": 999,
                "status": "Available",
                "create_date": "2024-11-08T07:50:08.812633Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_duckoBC.png"
            },
            {
                "id": 3,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 17",
                "price": "99999.98",
                "stock_quantity": 999,
                "status": "Available",
                "create_date": "2024-11-08T07:51:46.622904Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_revjsGx.png"
            },
            {
                "id": 4,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 19",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T07:51:58.375138Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_gcfx5Wr.png"
            },
            {
                "id": 5,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 1",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T07:58:38.213936Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_ccPqlss.png"
            },
            {
                "id": 6,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 2",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T07:58:44.121058Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_ilTYWcG.png"
            },
            {
                "id": 7,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 3",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T07:58:46.855643Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_W3GX29i.png"
            },
            {
                "id": 8,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 4",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T07:58:49.671959Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_7tJgPDF.png"
            },
            {
                "id": 9,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 5",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T08:01:32.476365Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_1umvd1q.png"
            },
            {
                "id": 10,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 6",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T08:01:36.489290Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_7NYYJ6b.png"
            },
            {
                "id": 11,
                "shop": 1,
                "name": "苹果手机",
                "description": "Iphone 7",
                "price": "99999.98",
                "stock_quantity": 2,
                "status": "Available",
                "create_date": "2024-11-08T08:01:39.735627Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_8X8qJgv.png"
            }
        ]
    }
}
```

### 获取所有商品

- 请求路径：`/shop/products`
- 其余和上面一样
