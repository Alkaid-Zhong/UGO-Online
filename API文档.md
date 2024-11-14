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
- `200` 商品错误
- `300` 商店错误
- `301` 商店权限错误
- `302` 邀请码错误
- `400` 表示用户身份错误
- `401` 表示用户未登录
- `402` 表示注册失败
- `403` 表示用户名或密码错误（登陆失败）

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
  - 'shop' 管理的商铺的id，没有则为null

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
- 查询参数
  - page 整数，请求的页码
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
                    },
                    {
                        "name": "seller3",
                        "email": "seller3@buaa.edu.cn",
                        "role": "SELLER"
                    }
                ]
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
  - page 整数，请求的页码
  - category 字符串，类别筛选（放id）
  - **以下后端 TODO**
  - min_price, max_price 浮点数，最高最低价格筛选
  - ordering 字符串，排序字段
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
        "shops": [
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
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_2OLYpvf.png"
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
                "image": "http://127.0.0.1:8000/media/product_images/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_2024-02-05_101216_nXqr0kW.png"
            },
            {
                "id": 24,
                "shop": 1,
                "name": "Iphone 666",
                "description": "最牛逼的苹果手机！",
                "price": "99999.99",
                "stock_quantity": 3,
                "category": 1,
                "status": "Available",
                "create_date": "2024-11-11T03:30:05.174259Z",
                "image": "http://127.0.0.1:8000/media/product_images/%E4%B8%8A%E6%B5%B7%E4%B8%9C%E4%BA%9A%E5%B7%B2%E5%A4%84%E7%90%86.png",
                "category_name": "电子产品"
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
