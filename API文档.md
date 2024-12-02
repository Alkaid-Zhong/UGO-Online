# 基本数据格式

**除了GET，所有url末尾都需要带'/'**

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
- `200` 商品错误
- `201` 订单错误
- `300` 商店错误
- `301` 商店权限错误
- `302` 邀请码错误
- `400` 表示用户身份错误
- `401` 表示用户未登录
- `402` 表示注册失败
- `403` 表示用户名或密码错误（登陆失败）
- `500` 地址相关错误

# API文档

## 用户注册登录

### 用户注册（买家）

请求路径`/user/register/customer`

请求方法`POST`

请求数据格式

- `name` 用户名
- `phone` 电话号码
- `email` 用户邮箱（作为用户唯一标识）
- `password` 密码

返回数据格式

`null`

### 用户注册（商家）

请求路径`/user/register/seller`

请求方法`POST`

请求数据格式

- `name` 商家名称
- `phone` 联系方式
- `email` 用户邮箱（作为用户唯一标识）
- `password` 密码

返回数据格式

- `null`

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
  - `shop` 管理的商铺的id，没有则为null
  - `money` 余额
  - `phone` 手机号

### 修改密码

- 请求路径`/user/change-password`
- 请求方法`POST`
- 请求数据格式：
```json
{
    "old_password": "旧密码",
    "password": "新密码",
    "password_confirm": "确认新密码"
}
```
- 保证了更改密码后用户仍然在登陆状态

### 充值

- 请求路径`/user/add-money`
- 请求方法`POST`
- 请求数据格式：
```json
{
    "add_money": "100.05"
}
```

## 地址管理

### 新建地址

- 请求路径`/user/address/create/`
- 请求方法`POST`
- 请求数据格式
```json
{
    "recipient_name": "默认地址check",
    "province": "北京市",
    "city": "海淀区",
    "address": "学院路37号北航111",
    "phone": "17770793406",
    "is_default": "true/false, 默认为false"
}
```

### 获取地址列表

- 请求路径`/user/address/list/`
- 请求方法`GET`
- 返回结果格式
默认地址（如果有）一定在第一个
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": [
        {
            "id": 8,
            "recipient_name": "默认地址check",
            "address": "学院路37号北航111",
            "city": "海淀区",
            "province": "北京市",
            "phone": "17770793406",
            "is_default": true,
            "user": 5
        },
        {
            "id": 1,
            "recipient_name": "czx",
            "address": "学院路37号北航",
            "city": "海淀区",
            "province": "北京市",
            "phone": "17770793406",
            "is_default": false,
            "user": 5
        },
        {
            "id": 2,
            "recipient_name": "czx",
            "address": "学院路37号北航",
            "city": "海淀区",
            "province": "北京市",
            "phone": "17770793406",
            "is_default": false,
            "user": 5
        },
        {
            "id": 3,
            "recipient_name": "czx",
            "address": "学院路37号北航",
            "city": "海淀区",
            "province": "北京市",
            "phone": "17770793406",
            "is_default": false,
            "user": 5
        }
    ]
}
```

### 获取默认地址

- 请求路径`/user/address/default/`
- 请求方法`GET`
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "id": 8,
        "recipient_name": "默认地址check",
        "address": "学院路37号北航111",
        "city": "海淀区",
        "province": "北京市",
        "phone": "17770793406",
        "is_default": true,
        "user": 5
    }
}
```
- 如果没有默认地址，返回`null`
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": null
}
```

### 删除地址

- 请求路径`/user/address/<int:address_id>/delete/`
- 请求方法`DELETE`

### 获取地址详情

- 请求路径`/user/address/<int:address_id>/`
- 请求方法`GET`
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "id": 2,
        "recipient_name": "czx",
        "address": "学院路37号北航",
        "city": "海淀区",
        "province": "北京市",
        "phone": "17770793406",
        "is_default": false,
        "user": 5
    }
}
```

### 修改地址
- 请求路径`/user/address/<int:address_id>/update/`
- 请求方法`PUT`
- 请求参数
  和新建地址一样，可以传部分，则部分修改。

## 商店相关

### 获取所有商铺

- 请求路径：`/shop`
- 请求方法：`GET`
- 权限要求：无
- 查询参数
  - page 整数，请求的页码
  - search 字符串，搜索关键词
  - ordering：['average_rating', 'name', 'create_date']
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "shops": [
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
                        "role": "SELLER",
                        "shop": 1,
                        "money": "0.00",
                        "phone": "1234567891"
                    }
                ],
                "total_income": "30.00",
                "average_rating": 4.0
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
                        "role": "SELLER",
                        "shop": 2,
                        "money": "0.00",
                        "phone": "1111111111"
                    },
                    {
                        "name": "seller3",
                        "email": "seller3@buaa.edu.cn",
                        "role": "SELLER",
                        "shop": 2,
                        "money": "0.00",
                        "phone": "0000000000"
                    }
                ],
                "total_income": "65.00",
                "average_rating": null
            }
        ],
        "total_count": 2,
        "total_page": 1,
        "cur_page": 1
    }
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
                "role": "SELLER",
                "shop": 1,
                "money": "0.00",
                "phone": "1234567891"
            }
        ],
        "total_income": "30.00",
        "average_rating": 4.0
    }
}
```

### 查看商店所有流水

- 请求路径：`/shop/<int:id>/transactions`
- 请求方法：`GET`
- 权限要求：需要认证，且用户角色为商家，并且是商铺的现有管理者
- 查询参数
  - page 整数，请求的页码
  - transaction_type 交易类型，Income/Refund
  - date 日期，格式为YYYY-MM-DD
  - ordering 排序字段，可选：'date', 'amount'，在前面加‘-’表示降序
  - 默认按照最近到最远排序
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "transactions": [
            {
                "id": 3,
                "shop": 2,
                "shop_name": "张三的商铺",
                "order": 23,
                "order_id": 23,
                "amount": "-10.00",
                "transaction_type": "Refund",
                "date": "2024-11-19T07:37:50.232500Z",
                "description": "Refund for Order 订单 23 - 用户 customer1@buaa.edu.cn, Items: 26"
            },
            {
                "id": 1,
                "shop": 2,
                "shop_name": "张三的商铺",
                "order": 23,
                "order_id": 23,
                "amount": "25.00",
                "transaction_type": "Income",
                "date": "2024-11-19T07:32:10.199759Z",
                "description": "Payment for 订单 23 - 用户 customer1@buaa.edu.cn"
            }
        ],
        "total_count": 2,
        "total_page": 1,
        "cur_page": 1
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
  "name": "Iphone 6s",
  "description": "最新款苹果手机", 
  "price":  "1888.99",
  "category": "这里传入对应category的id！",
  "stock_quantity": "999",
  "image": "?"
}
```
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "商品创建成功",
    "data": {
        "id": 25,
        "shop": 1,
        "name": "Iphone 6669",
        "description": "最牛逼的苹果手机！",
        "price": "99999.99",
        "stock_quantity": 3,
        "category": 1,
        "status": "Available",
        "create_date": "2024-11-11T03:36:25.446511Z",
        "image": "/media/product_images/%E4%B8%8A%E6%B5%B7%E4%B8%9C%E4%BA%9A%E5%B7%B2%E5%A4%84%E7%90%86_te3siEu.png",
        "category_name": "电子产品"
    }
}
```

### 获取店内所有商品

- 请求路径：`/shop/<int:shop_id>/products`
- 请求方法：`GET`
- 权限要求：无
- 查询参数
| 参数名           | 类型   | 是否必填 | 默认值       | 描述                                                                                   | 示例                                            |
|------------------|--------|----------|--------------|----------------------------------------------------------------------------------------|------------------------------------------------|
| `category`       | int    | 否       | 无           | 按商品分类筛选，传入分类的ID。                                                        | `/products/?category=3`                   |
| `price__gte`     | float  | 否       | 无           | 筛选价格大于等于指定值的商品。                                                        | `/products/?price__gte=100`               |
| `price__lte`     | float  | 否       | 无           | 筛选价格小于等于指定值的商品。                                                        | `/products/?price__lte=500`               |
| `search`         | string | 否       | 无           | 搜索关键字，支持按商品名称、描述或商铺名称模糊匹配。                                    | `/products/?search=手机`                  |
| `ordering`       | string | 否       | `-average_rating` | 排序字段，支持多种字段排序。字段前加`-`表示降序，不加`-`表示升序。支持的排序字段包括：`price`（价格）、`name`（名称）、`create_date`（创建时间）、`average_rating`（平均评价得分）。 | `/products/?ordering=price`               |
| `shop_id`        | int    | 否       | 无           | 筛选某个商铺下的商品。传入商铺的ID。                                                  | `/products/?shop_id=1`                    |
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 23,
        "next": null,
        "previous": "http://127.0.0.1:8000/shop/1/products?page=2",
        "products": [
            {
                "id": 22,
                "shop": 1,
                "name": "oppo A11",
                "description": "安卓手机",
                "price": "9.90",
                "stock_quantity": 2,
                "category": null,
                "status": "Available",
                "create_date": "2024-11-08T08:02:45.534134Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_2OLYpvf.png",
                "average_rating": 4.0,
                "sales_volume": 0
            },
            {
                "id": 23,
                "shop": 1,
                "name": "oppo A11 pro max",
                "description": "安卓手机",
                "price": "19.90",
                "stock_quantity": 2,
                "category": null,
                "status": "Available",
                "create_date": "2024-11-08T08:02:53.330448Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_nXqr0kW.png",
                "average_rating": null,
                "sales_volume": 0
            }
        ],
        "total_count": 23,
        "total_page": 3,
        "cur_page": 3
    }
}
```

### 获取所有商品

- 请求路径：`/shop/products`
- 其余和上面一样

### 获取所有的商品类别

- 请求路径：`/shop/category_list`
- 请求方法：`GET`
- 权限要求：无
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "categories": [
            {
                "id": 1,
                "name": "电子产品"
            },
            {
                "id": 2,
                "name": "服装"
            }
        ]
    }
}
```

### 获取指定商店的所有类别

- 请求路径：`/shop/<int:shop_id>/category_list`
- 其余同上

### 获取指定商品的详细信息

- 请求路径：`/shop/product/<int:product_id>`
- 请求方法：`GET`
- 权限要求：无
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "id": 28,
        "shop": 1,
        "name": "测试物品2",
        "description": "",
        "price": "15.00",
        "stock_quantity": 8,
        "category": null,
        "status": "Available",
        "create_date": "2024-11-19T07:05:13.828545Z",
        "image": null,
        "average_rating": 4.0,
        "sales_volume": 0
    }
}
```

### 更改指定商品的信息

- 请求路径：`/shop/<int:id>/product/update/`
- 请求方法：`PUT`
- 权限要求：登录用户，是卖家
- 请求参数：
```json
{
  "product_id": "114514",
  "name": "Iphone 6s",
  "description": "最新款苹果手机", 
  "price":  "1888.99",
  "category": "这里传入对应category的id！",
  "stock_quantity": "999",
  "status": "Unavailable",
  "image": "?"
}
```
product_id是必须要传的，其它内容选传。
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "商品修改成功",
    "data": {
        "id": 28,
        "shop": 6,
        "name": "[我不是急b]",
        "description": "嵌入式，中西结合，苍劲有力，错落有致",
        "price": "19999.00",
        "stock_quantity": 100,
        "category": 6,
        "status": "Unavailable",
        "create_date": "2024-11-29T16:18:36.747895+08:00",
        "image": "http://8.152.218.70:8000/media/product_images/eiou_DUDFFpT.jpg",
        "category_name": "玩具",
        "average_rating": null,
        "sales_volume": 0
    }
}
```

### 删除商品

- 请求路径：`/shop/<int:id>/product/delete/`
- 请求方法：`DELETE`
- 权限要求：登录用户，是卖家
- 请求参数：
```json
{
    "product_id": "28"
}
```

## 购物车相关

### 向购物车里添加商品

- 在商店浏览商品的时候，点击加入购物车，调用这个，前端限制一下quantity不能为0或者负数
- 请求路径：`/cart/add`
- 请求方法：`POST`
- 权限要求：登录用户，是买家
- 请求参数：
    - product_id：商品id. *注意区分product_id和item_id*
    - quantity：数量
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "加入购物车成功",
    "data": {
        "id": 2,
        "product": {
            "id": 1,
            "shop": 2,
            "name": "苹果手机",
            "description": "Iphone 16",
            "price": "9999.98",
            "stock_quantity": 999,
            "category": null,
            "status": "Available",
            "create_date": "2024-11-08T07:49:58.707722Z",
            "image": "/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216.png"
        },
        "product_id": 1,
        "quantity": 0,
        "updated_time": "2024-11-11T09:50:34.854501Z"
    }
}
```

### 修改购物车里的商品数量

- 请求路径：`/cart/update`
- 请求方法：`PUT`
- 权限要求：登录用户，是买家
- 请求参数：
    - item_id：购物车里的商品id
    - quantity：修改为的数量
- 返回结果格式
  - 如果quantity非0
  ```json
  {
      "success": true,
      "code": 0,
      "message": "购物车已更新",
      "data": {
          "id": 2,
          "product": {
              "id": 1,
              "shop": 2,
              "name": "苹果手机",
              "description": "Iphone 16",
              "price": "9999.98",
              "stock_quantity": 999,
              "category": null,
              "status": "Available",
              "create_date": "2024-11-08T07:49:58.707722Z",
              "image": "/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216.png"
          },
          "product_id": 1,
          "quantity": 1,
          "updated_time": "2024-11-11T09:56:18.116843Z"
      }
  }
  ```
  - 如果quantity为0，则删除该商品
  ```json
  {
    "success": true,
    "code": 0,
    "message": "商品已成功从购物车移除",
    "data": {
        "id": null,
        "product": {
            "id": 1,
            "shop": 2,
            "name": "苹果手机",
            "description": "Iphone 16",
            "price": "9999.98",
            "stock_quantity": 999,
            "category": null,
            "status": "Available",
            "create_date": "2024-11-08T07:49:58.707722Z",
            "image": "/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216.png"
        },
        "product_id": 1,
        "quantity": 1,
        "updated_time": "2024-11-11T09:56:18.116843Z"
    }
  }
  ```
  
### 从购物车中移除商品

- 请求路径：`/cart/delete`
- 请求方法：`DELETE`
- 权限要求：登录用户，是买家
- 请求参数：
    - item_id：购物车里的商品id
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "商品已成功从购物车移除",
    "data": null
}
```

### 获取购物车详情

- 请求路径：`/cart`
- 请求方法：`GET`
- 权限要求：登录用户，是买家
- 返回结果格式：按商店分的列表
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "shops": [
            {
                "shop_id": 1,
                "shop_name": "李四的商铺",
                "items": [
                    {
                        "item_id": 5,
                        "product_id": 4,
                        "product_name": "苹果手机",
                        "product_stock_quantity": 2,
                        "product_status": "Available",
                        "quantity": 1,
                        "price": "99999.98",
                        "total_price": "99999.98",
                        "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_gcfx5Wr.png"
                    },
                    {
                        "item_id": 6,
                        "product_id": 5,
                        "product_name": "苹果手机",
                        "product_stock_quantity": 2,
                        "product_status": "Available",
                        "quantity": 2,
                        "price": "99999.98",
                        "total_price": "199999.96",
                        "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_ccPqlss.png"
                    },
                    {
                        "item_id": 8,
                        "product_id": 2,
                        "product_name": "苹果手机",
                        "product_stock_quantity": 999,
                        "product_status": "Available",
                        "quantity": 2,
                        "price": "9999.98",
                        "total_price": "19999.96",
                        "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_duckoBC.png"
                    },
                    {
                        "item_id": 9,
                        "product_id": 3,
                        "product_name": "苹果手机",
                        "product_stock_quantity": 999,
                        "product_status": "Available",
                        "quantity": 2,
                        "price": "99999.98",
                        "total_price": "199999.96",
                        "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_revjsGx.png"
                    }
                ]
            },
            {
                "shop_id": 2,
                "shop_name": "张三的商铺",
                "items": [
                    {
                        "item_id": 7,
                        "product_id": 1,
                        "product_name": "苹果手机",
                        "product_stock_quantity": 999,
                        "product_status": "Available",
                        "quantity": 2,
                        "price": "9999.98",
                        "total_price": "19999.96",
                        "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216.png"
                    }
                ]
            }
        ]
    }
}
```

## 订单相关

后端todo: 预览页面需要获取的信息。传入和创建订单传入的数据一样，传出一个按shop分类的列表（和购物车一样）

（这个需要吗？*等前端*）

传进来的是list，返回的是一个order的list。可以根据这个order的list，去搞一个支付的页面（虽然可能有多个订单，但是是一起支付的）。支付就可以传一个order_id的list过来获取支付的逻辑。

### 创建订单

- 请求路径：`/order/create/`
- 请求方式：POST
- 请求参数：
```json
{
    "address_id": 2,
    "items": [
        {
            "product_id": 23,
            "quantity": 1
        },
        {
            "product_id": 22,
            "quantity": 2
        }
    ]
}
```
- 返回结果格式
```json
{
    "success": true,
    "code": 0,
    "message": "订单创建成功",
    "data": {
        "orders": [
            {
                "order_id": 19,
                "user": 5,
                "shop_id": 2,
                "order_date": "2024-11-18T11:00:28.531487+00:00",
                "status": "Pending Payment",
                "address": {
                    "recipient_name": "czx",
                    "address": "学院路37号北航",
                    "city": "海淀区",
                    "province": "北京市",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 20,
                        "product": {
                            "id": 1,
                            "shop": 2,
                            "name": "苹果手机",
                            "description": "Iphone 16",
                            "price": "9999.98",
                            "stock_quantity": 990,
                            "category": null,
                            "status": "Available",
                            "create_date": "2024-11-08T07:49:58.707722Z",
                            "image": "/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216.png"
                        },
                        "quantity": 1,
                        "unit_price": "9999.98",
                        "total_price": "9999.98",
                        "is_cancelled": false
                    }
                ],
                "total_price": 9999.98
            },
            {
                "order_id": 20,
                "user": 5,
                "shop_id": 1,
                "order_date": "2024-11-18T11:00:28.533491+00:00",
                "status": "Pending Payment",
                "address": {
                    "recipient_name": "czx",
                    "address": "学院路37号北航",
                    "city": "海淀区",
                    "province": "北京市",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 21,
                        "product": {
                            "id": 25,
                            "shop": 1,
                            "name": "Iphone 6669",
                            "description": "最牛逼的苹果手机！",
                            "price": "99999.99",
                            "stock_quantity": 3,
                            "category": 1,
                            "status": "Available",
                            "create_date": "2024-11-11T03:36:25.446511Z",
                            "image": "/media/product_images/%E4%B8%8A%E6%B5%B7%E4%B8%9C%E4%BA%9A%E5%B7%B2%E5%A4%84%E7%90%86_te3siEu.png",
                            "category_name": "电子产品"
                        },
                        "quantity": 3,
                        "unit_price": "99999.99",
                        "total_price": "299999.97",
                        "is_cancelled": false
                    }
                ],
                "total_price": 299999.97
            }
        ]
    }
}
```

### 用户获取订单列表

- 请求路径：`/order/user_orders/`
- 请求方式：GET
- 请求参数
  - page：页码，默认为1
  
  - status：订单状态，可选参数，默认为所有状态
    STATUS_CHOICES = (
        ('Pending Payment', '待支付'),
        ('Payment Received', '已支付待发货'),
        ('Shipped', '商家已发货')
    ​    ('Completed', '已完成'),
    ​    ('Refund Requested', '申请退款中'),
    ​    ('Refund Successful', '退款成功'),
    ​    ('Cancelled', '已取消'),
    )
- 响应数据：
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 10,
        "next": null,
        "previous": null,
        "orders": [
            {
                "order_id": 88,
                "user": 18,
                "shop_id": 6,
                "total_price": "334618.44",
                "order_date": "2024-12-02T07:45:40.086820+00:00",
                "status": "Pending Payment",
                "address": {
                    "recipient_name": "Zhixin Cai is god",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 127,
                        "product": {
                            "id": 7,
                            "shop": 6,
                            "name": "【孤独摇滚】 喜多郁代 色纸",
                            "description": "【ぼっち・ざ・ろっく】 喜多 郁代   色紙",
                            "price": "15.00",
                            "stock_quantity": 945,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-24T21:58:51.432201+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E8%89%B2%E7%BA%B8.jpg",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 54
                        },
                        "quantity": 8,
                        "unit_price": "15.00",
                        "total_price": "120.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    },
                    {
                        "id": 128,
                        "product": {
                            "id": 22,
                            "shop": 6,
                            "name": "『我是UUQ』书画作品 独家限量",
                            "description": "由15-427特邀书法家aiou创作。“我是UUQ”几个字，苍白无力却结构紧凑，处处体现出427的张弛有度。这这幅作品内涵深厚，“我是UUQ”体现出作者的自信风采。\"Q\"采取未封口结构，展现出一种不被定义、不被限制的愿望和期许。U与Q相连，同时展现出人的差异性但又彼此互联互通的社会特点。",
                            "price": "1.88",
                            "stock_quantity": 99973,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-28T13:38:55.658167+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/1000216726.jpg",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 26
                        },
                        "quantity": 13,
                        "unit_price": "1.88",
                        "total_price": "24.44",
                        "is_cancelled": false,
                        "has_reviewed": false
                    },
                    {
                        "id": 129,
                        "product": {
                            "id": 23,
                            "shop": 6,
                            "name": "大虎鲸",
                            "description": "斯哈",
                            "price": "88.00",
                            "stock_quantity": 62,
                            "category": 5,
                            "status": "Available",
                            "create_date": "2024-11-28T16:34:56.610090+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20230313204552.jpg",
                            "category_name": "食品",
                            "average_rating": null,
                            "sales_volume": 26
                        },
                        "quantity": 13,
                        "unit_price": "88.00",
                        "total_price": "1144.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    },
                    {
                        "id": 130,
                        "product": {
                            "id": 24,
                            "shop": 6,
                            "name": "uuuuqqqqqq",
                            "description": "辛勤工作",
                            "price": "66666.00",
                            "stock_quantity": 55555550,
                            "category": 3,
                            "status": "Available",
                            "create_date": "2024-11-29T00:27:14.752801+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/IMG20241129002553.jpg",
                            "category_name": "家居用品",
                            "average_rating": null,
                            "sales_volume": 5
                        },
                        "quantity": 5,
                        "unit_price": "66666.00",
                        "total_price": "333330.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 87,
                "user": 18,
                "shop_id": 5,
                "total_price": "1919810.00",
                "order_date": "2024-12-02T07:43:49.843394+00:00",
                "status": "Pending Payment",
                "address": {
                    "recipient_name": "Zhixin Cai is god",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 126,
                        "product": {
                            "id": 3,
                            "shop": 5,
                            "name": "UUQ",
                            "description": "UGO",
                            "price": "1919810.00",
                            "stock_quantity": 124124239,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-21T19:23:49.746815+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-11-21_192314.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 201
                        },
                        "quantity": 1,
                        "unit_price": "1919810.00",
                        "total_price": "1919810.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 77,
                "user": 18,
                "shop_id": 6,
                "total_price": "0.00",
                "order_date": "2024-11-28T16:51:44.107012+00:00",
                "status": "Cancelled",
                "address": {
                    "recipient_name": "Zhixin Cai is god",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 101,
                        "product": {
                            "id": 24,
                            "shop": 6,
                            "name": "uuuuqqqqqq",
                            "description": "辛勤工作",
                            "price": "66666.00",
                            "stock_quantity": 55555550,
                            "category": 3,
                            "status": "Available",
                            "create_date": "2024-11-29T00:27:14.752801+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/IMG20241129002553.jpg",
                            "category_name": "家居用品",
                            "average_rating": null,
                            "sales_volume": 5
                        },
                        "quantity": 5,
                        "unit_price": "66666.00",
                        "total_price": "333330.00",
                        "is_cancelled": true,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 75,
                "user": 18,
                "shop_id": 5,
                "total_price": "1919810.00",
                "order_date": "2024-11-28T11:36:55.733207+00:00",
                "status": "Payment Received",
                "address": {
                    "recipient_name": "Zhixin Cai is god4",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 99,
                        "product": {
                            "id": 3,
                            "shop": 5,
                            "name": "UUQ",
                            "description": "UGO",
                            "price": "1919810.00",
                            "stock_quantity": 124124239,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-21T19:23:49.746815+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-11-21_192314.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 201
                        },
                        "quantity": 1,
                        "unit_price": "1919810.00",
                        "total_price": "1919810.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 74,
                "user": 18,
                "shop_id": 6,
                "total_price": "1288.44",
                "order_date": "2024-11-28T11:36:35.326018+00:00",
                "status": "Shipped",
                "address": {
                    "recipient_name": "Zhixin Cai is god",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 96,
                        "product": {
                            "id": 7,
                            "shop": 6,
                            "name": "【孤独摇滚】 喜多郁代 色纸",
                            "description": "【ぼっち・ざ・ろっく】 喜多 郁代   色紙",
                            "price": "15.00",
                            "stock_quantity": 945,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-24T21:58:51.432201+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E8%89%B2%E7%BA%B8.jpg",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 54
                        },
                        "quantity": 8,
                        "unit_price": "15.00",
                        "total_price": "120.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    },
                    {
                        "id": 97,
                        "product": {
                            "id": 22,
                            "shop": 6,
                            "name": "『我是UUQ』书画作品 独家限量",
                            "description": "由15-427特邀书法家aiou创作。“我是UUQ”几个字，苍白无力却结构紧凑，处处体现出427的张弛有度。这这幅作品内涵深厚，“我是UUQ”体现出作者的自信风采。\"Q\"采取未封口结构，展现出一种不被定义、不被限制的愿望和期许。U与Q相连，同时展现出人的差异性但又彼此互联互通的社会特点。",
                            "price": "1.88",
                            "stock_quantity": 99973,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-28T13:38:55.658167+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/1000216726.jpg",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 26
                        },
                        "quantity": 13,
                        "unit_price": "1.88",
                        "total_price": "24.44",
                        "is_cancelled": false,
                        "has_reviewed": false
                    },
                    {
                        "id": 98,
                        "product": {
                            "id": 23,
                            "shop": 6,
                            "name": "大虎鲸",
                            "description": "斯哈",
                            "price": "88.00",
                            "stock_quantity": 62,
                            "category": 5,
                            "status": "Available",
                            "create_date": "2024-11-28T16:34:56.610090+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20230313204552.jpg",
                            "category_name": "食品",
                            "average_rating": null,
                            "sales_volume": 26
                        },
                        "quantity": 13,
                        "unit_price": "88.00",
                        "total_price": "1144.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 55,
                "user": 18,
                "shop_id": 5,
                "total_price": "88.00",
                "order_date": "2024-11-28T03:04:19.586575+00:00",
                "status": "Completed",
                "address": {
                    "recipient_name": "111",
                    "address": "111",
                    "city": "11",
                    "province": "11",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 75,
                        "product": {
                            "id": 15,
                            "shop": 5,
                            "name": "优秀宿舍",
                            "description": "荣誉",
                            "price": "88.00",
                            "stock_quantity": 1,
                            "category": 2,
                            "status": "Available",
                            "create_date": "2024-11-25T12:01:32.924757+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/IMG20241125120047.jpg",
                            "category_name": "服装",
                            "average_rating": 4.0,
                            "sales_volume": 1
                        },
                        "quantity": 1,
                        "unit_price": "88.00",
                        "total_price": "88.00",
                        "is_cancelled": false,
                        "has_reviewed": true
                    }
                ]
            },
            {
                "order_id": 54,
                "user": 18,
                "shop_id": 8,
                "total_price": "854854.00",
                "order_date": "2024-11-28T03:04:19.564522+00:00",
                "status": "Payment Received",
                "address": {
                    "recipient_name": "Zhixin Cai is god2",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "13021173406"
                },
                "items": [
                    {
                        "id": 74,
                        "product": {
                            "id": 17,
                            "shop": 8,
                            "name": "我来助你！",
                            "description": "CAIGOU",
                            "price": "427427.00",
                            "stock_quantity": 218,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-25T12:03:11.036149+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/48f0a64a9308ae2d90f8fb9d5786825.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 4
                        },
                        "quantity": 2,
                        "unit_price": "427427.00",
                        "total_price": "854854.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 53,
                "user": 18,
                "shop_id": 8,
                "total_price": "854854.00",
                "order_date": "2024-11-28T03:01:00.312544+00:00",
                "status": "Payment Received",
                "address": {
                    "recipient_name": "Zhixin Cai",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 73,
                        "product": {
                            "id": 17,
                            "shop": 8,
                            "name": "我来助你！",
                            "description": "CAIGOU",
                            "price": "427427.00",
                            "stock_quantity": 218,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-25T12:03:11.036149+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/48f0a64a9308ae2d90f8fb9d5786825.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 4
                        },
                        "quantity": 2,
                        "unit_price": "427427.00",
                        "total_price": "854854.00",
                        "is_cancelled": false,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 52,
                "user": 18,
                "shop_id": 8,
                "total_price": "0.00",
                "order_date": "2024-11-27T15:56:20.889621+00:00",
                "status": "Cancelled",
                "address": {
                    "recipient_name": "111",
                    "address": "111",
                    "city": "11",
                    "province": "11",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 72,
                        "product": {
                            "id": 17,
                            "shop": 8,
                            "name": "我来助你！",
                            "description": "CAIGOU",
                            "price": "427427.00",
                            "stock_quantity": 218,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-25T12:03:11.036149+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/48f0a64a9308ae2d90f8fb9d5786825.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 4
                        },
                        "quantity": 4,
                        "unit_price": "427427.00",
                        "total_price": "1709708.00",
                        "is_cancelled": true,
                        "has_reviewed": false
                    }
                ]
            },
            {
                "order_id": 35,
                "user": 18,
                "shop_id": 5,
                "total_price": "0.00",
                "order_date": "2024-11-25T02:38:42.693394+00:00",
                "status": "Cancelled",
                "address": {
                    "recipient_name": "Zhixin Cai",
                    "address": "bj",
                    "city": "Ganzhou",
                    "province": "Jiangxi",
                    "phone": "17770793406"
                },
                "items": [
                    {
                        "id": 49,
                        "product": {
                            "id": 3,
                            "shop": 5,
                            "name": "UUQ",
                            "description": "UGO",
                            "price": "1919810.00",
                            "stock_quantity": 124124239,
                            "category": 6,
                            "status": "Available",
                            "create_date": "2024-11-21T19:23:49.746815+08:00",
                            "image": "http://8.152.218.70:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-11-21_192314.png",
                            "category_name": "玩具",
                            "average_rating": null,
                            "sales_volume": 201
                        },
                        "quantity": 1,
                        "unit_price": "1919810.00",
                        "total_price": "1919810.00",
                        "is_cancelled": true,
                        "has_reviewed": false
                    }
                ]
            }
        ],
        "total_count": 10,
        "total_page": 1,
        "cur_page": 1
    }
}
```

### 商家获取订单列表

- 请求路径：`order/seller_orders/`
- 请求方法：GET
- 其余和上面用户那个一样

### 用户支付订单

刚下单的时候是多个order杂糅在一起的（此时是传列表），如果刚下单的时候没有支付，那么之后就只能在订单界面浏览订单列表，一个一个支付（传列表大小为1即可）。

- **请求路径**：`/order/pay/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为 **买家**
- **请求数据格式**：

```json
{
  "order_ids": [1, 2, 3]
}
```

- **请求参数说明**：
  - `order_ids`：整数数组，表示需要支付的订单 ID 列表。这些订单必须属于当前用户，且状态为“待支付”。
- **响应**：
```json
{
  "success": true,
  "code": 0,
  "message": "支付成功",
  "data": null
}
```

### 用户取消订单

用户未支付时，可以一整个订单一起取消掉

- **请求路径**：`/order/<int:order_id>/cancel/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为 **买家**
- **请求数据格式**：

无需额外数据，`order_id` 在请求路径中提供。

- **响应**：
```json
{
  "success": true,
  "code": 0,
  "message": "订单已取消",
  "data": null
}
```

### 部分商品退款

对于一个已经支付但商家未发货的订单，用户可以申请部分商品退款，不需要商家审核，秒退。

- **请求路径**：`/order/<int:order_id>/refund/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为 **买家**
- **请求数据格式**：

```json
{
  "item_ids": [101, 102]
}
```

- **请求参数说明**：
  - `item_ids`：整数数组，表示需要退款的订单项（商品）ID 列表。这些订单项必须属于指定的订单，且订单状态为“已支付待发货”。

- **响应**：
```json
{
    "success": true,
    "code": 0,
    "message": "退款成功",
    "data": null
}
```

### 商家发货

- **请求路径**：`/orders/<int:order_id>/ship/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为 **卖家**，并且是订单所属商店的管理者
- **请求数据格式**：

无需额外数据，`order_id` 在请求路径中提供。

- **响应**：
```json
{
    "success": true,
    "code": 0,
    "message": "订单状态已更新为已发货",
    "data": null
}
```

### 用户确认收货

- **请求路径**：`/order/<int:order_id>/complete/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为对应订单的 **买家**
- **请求数据格式**：
  无需额外数据，`order_id` 在请求路径中提供。
- **响应**：
```json
{
    "success": true,
    "code": 0,
    "message": "订单状态已更新为已完成",
    "data": null
}
```


### 修改订单地址

- **请求路径**：`/order/<int:order_id>/update_address/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为对应订单的 **买家**
- **请求数据格式**：
```json
{
  "address_id": 1
}
```

## 评价相关

### 用户评价商品

- **请求路径**：`/shop/review/create/`
- **请求方法**：`POST`
- **权限要求**：需要认证，且用户角色为 **买家**，且该用户购买了该商品
- **请求数据格式**：
```json
{
    "order": 55,
    "product": 28,
    "rating": 4,
    "comment": "非常好的商品！"
}
```
order传对应orderItem的id
- **响应**：
```json
{
    "success": true,
    "code": 0,
    "message": "评价提交成功",
    "data": {
        "id": 1,
        "user": 5,
        "product": 28,
        "rating": 4,
        "comment": "非常好的商品！",
        "create_date": "2024-11-19T14:54:35.926455Z",
        "merchant_reply": null,
        "reply_date": null
    }
}
```

### 商家回复评价

- **请求路径**：`/shop/review/<int:review_id>/reply/`
- **请求方法**：`PUT`
- **权限要求**：需要认证，且用户角色为 **卖家**，且该用户是该商品的商家
- **请求数据格式**：
```json
{
    "merchant_reply": "感谢您的支持！"
}
```
- **响应**：
```json
{
    "success": true,
    "code": 0,
    "message": "回复成功",
    "data": null
}
```

### 获取商品的评价
- **请求路径**：`/shop/product/<int:product_id>/reviews/`
- **请求方法**：GET
- **权限要求**：无需认证
- **返回数据格式**：
```json
{
    "success": true,
    "code": 0,
    "message": "查询返回成功",
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "reviews": [
            {
                "id": 1,
                "user": {
                    "name": "customer1",
                    "email": "customer1@buaa.edu.cn",
                    "role": "CUSTOMER",
                    "shop": null,
                    "money": "345.25",
                    "phone": "1234567899"
                },
                "product": 28,
                "rating": 4,
                "comment": "非常好的商品！",
                "create_date": "2024-11-19T14:54:35.926455Z",
                "merchant_reply": "感谢您的支持！",
                "reply_date": "2024-11-19T15:08:54.135512Z"
            }
        ],
        "total_count": 1,
        "total_page": 1,
        "cur_page": 1
    }
}
```

### 查看对订单项的评价

- **请求路径**：`/shop/order_item/<int:order_item_id>/review/`
- **请求方法**：GET
- **权限要求**：需要认证
- **返回数据格式**：
```json
{
    "success": false,
    "code": 404,
    "message": "评论不存在",
    "data": null
}
```
```json
{
    "success": true,
    "code": 0,
    "message": "",
    "data": {
        "id": 1,
        "user": 18,
        "product": 15,
        "rating": 4,
        "comment": "nice!",
        "create_date": "2024-12-02T16:14:41.464490+08:00",
        "merchant_reply": null,
        "reply_date": null,
        "order": 75
    }
}
```
