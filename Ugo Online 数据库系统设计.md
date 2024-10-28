# Ugo Online 数据库系统设计

## 数据元素表设计

### **1. 商家表（Merchant）**

| 属性名   | 字段名            | 数据类型           | 数据说明             | 约束                      |
| -------- | ----------------- | ------------------ | -------------------- | ------------------------- |
| 商家ID   | merchant_id       | INT AUTO_INCREMENT | 商家的唯一标识       | PRIMARY KEY               |
| 商家名称 | name              | VARCHAR(255)       | 商家的名称           | NOT NULL                  |
| 联系方式 | contact_info      | VARCHAR(255)       | 商家的联系方式       |                           |
| 邮箱     | email             | VARCHAR(255)       | 商家的邮箱地址       | UNIQUE, NOT NULL          |
| 密码     | password          | VARCHAR(255)       | 登录密码（加密存储） | NOT NULL                  |
| 注册日期 | registration_date | DATETIME           | 注册时间             | DEFAULT CURRENT_TIMESTAMP |

---

### **2. 商铺表（Shop）**

| 属性名   | 字段名       | 数据类型           | 数据说明       | 约束                      |
| -------- | ------------ | ------------------ | -------------- | ------------------------- |
| 商铺ID   | shop_id      | INT AUTO_INCREMENT | 商铺的唯一标识 | PRIMARY KEY               |
| 商铺名称 | name         | VARCHAR(255)       | 商铺的名称     | NOT NULL                  |
| 地址     | address      | VARCHAR(255)       | 商铺的地址     |                           |
| 联系方式 | contact_info | VARCHAR(255)       | 商铺的联系方式 |                           |
| 商铺描述 | description  | TEXT               | 商铺的详细描述 |                           |
| 创建日期 | create_date  | DATETIME           | 商铺的创建时间 | DEFAULT CURRENT_TIMESTAMP |

**注意**：商铺与商家之间的关系通过 **商家商铺关联表（MerchantShop）** 来实现，以支持多对多关系。

---

### **3. 商家商铺关联表（MerchantShop）**

| 属性名 | 字段名      | 数据类型 | 数据说明 | 约束                                                   |
| ------ | ----------- | -------- | -------- | :----------------------------------------------------- |
| 商家ID | merchant_id | INT      | 商家的ID | FOREIGN KEY REFERENCES Merchant(merchant_id), NOT NULL |
| 商铺ID | shop_id     | INT      | 商铺的ID | FOREIGN KEY REFERENCES Shop(shop_id), NOT NULL         |

**约束**：

- **PRIMARY KEY (merchant_id, shop_id)**：确保同一商家和商铺的组合唯一。

---

### **3. 商品表（Product）**

| 属性名   | 字段名         | 数据类型           | 数据说明                          | 约束                                           |
| -------- | -------------- | ------------------ | --------------------------------- | ---------------------------------------------- |
| 商品ID   | product_id     | INT AUTO_INCREMENT | 商品的唯一标识                    | PRIMARY KEY                                    |
| 商铺ID   | shop_id        | INT                | 所属商铺的ID                      | FOREIGN KEY REFERENCES Shop(shop_id), NOT NULL |
| 商品名称 | name           | VARCHAR(255)       | 商品的名称                        | NOT NULL                                       |
| 商品描述 | description    | TEXT               | 商品的详细描述                    |                                                |
| 价格     | price          | DECIMAL(10,2)      | 商品的价格                        | NOT NULL                                       |
| 库存数量 | stock_quantity | INT                | 商品的库存数量                    | NOT NULL, DEFAULT 0                            |
| 商品类别 | category       | VARCHAR(255)       | 商品的类别                        |                                                |
| 状态     | status         | VARCHAR(50)        | 商品状态（Available/Unavailable） | NOT NULL, DEFAULT 'Available'                  |
| 创建日期 | create_date    | DATETIME           | 商品的创建时间                    | DEFAULT CURRENT_TIMESTAMP                      |

---

### **4. 用户表（User）**

| 属性名   | 字段名            | 数据类型           | 数据说明             | 约束                      |
| -------- | ----------------- | ------------------ | -------------------- | ------------------------- |
| 用户ID   | user_id           | INT AUTO_INCREMENT | 用户的唯一标识       | PRIMARY KEY               |
| 用户名   | username          | VARCHAR(255)       | 用户的登录名         | UNIQUE, NOT NULL          |
| 密码     | password          | VARCHAR(255)       | 登录密码（加密存储） | NOT NULL                  |
| 邮箱     | email             | VARCHAR(255)       | 用户的邮箱地址       | UNIQUE, NOT NULL          |
| 电话号码 | phone             | VARCHAR(50)        | 用户的联系电话       |                           |
| 注册日期 | registration_date | DATETIME           | 用户的注册时间       | DEFAULT CURRENT_TIMESTAMP |

---

### **5. 订单表（Order）**

| 属性名     | 字段名       | 数据类型           | 数据说明                                 | 约束                                                 |
| ---------- | ------------ | ------------------ | ---------------------------------------- | ---------------------------------------------------- |
| 订单ID     | order_id     | INT AUTO_INCREMENT | 订单的唯一标识                           | PRIMARY KEY                                          |
| 用户ID     | user_id      | INT                | 下单用户的ID                             | FOREIGN KEY REFERENCES User(user_id), NOT NULL       |
| 商品ID     | product_id   | INT                | 购买商品的ID                             | FOREIGN KEY REFERENCES Product(product_id), NOT NULL |
| 数量       | quantity     | INT                | 购买商品的数量                           | NOT NULL, CHECK (quantity > 0)                       |
| 单价       | unit_price   | DECIMAL(10,2)      | 购买时的商品单价                         | NOT NULL                                             |
| 总金额     | total_amount | DECIMAL(10,2)      | 订单的总金额                             | NOT NULL                                             |
| 订单日期   | order_date   | DATETIME           | 订单的创建时间                           | DEFAULT CURRENT_TIMESTAMP                            |
| 状态       | status       | VARCHAR(50)        | 订单状态（待支付，已支付待收货，已完成） | NOT NULL, DEFAULT 'Pending'                          |
| 收货地址ID | address_id   | INT                | 收货地址的ID                             | FOREIGN KEY REFERENCES Address(address_id)           |

### **6. 评价表（Review）**

| 属性名   | 字段名      | 数据类型           | 数据说明              | 约束                                                 |
| -------- | ----------- | ------------------ | --------------------- | ---------------------------------------------------- |
| 评价ID   | review_id   | INT AUTO_INCREMENT | 评价的唯一标识        | PRIMARY KEY                                          |
| 用户ID   | user_id     | INT                | 评价用户的ID          | FOREIGN KEY REFERENCES User(user_id), NOT NULL       |
| 商品ID   | product_id  | INT                | 被评价商品的ID        | FOREIGN KEY REFERENCES Product(product_id), NOT NULL |
| 订单ID   | order_id    | INT                | 所属订单的ID          | FOREIGN KEY REFERENCES Order(order_id), NOT NULL     |
| 评分     | rating      | INT                | 用户给出的评分（1-5） | NOT NULL, CHECK (rating BETWEEN 1 AND 5)             |
| 评论内容 | comment     | TEXT               | 用户的评价内容        |                                                      |
| 评价日期 | review_date | DATETIME           | 评价的提交时间        | DEFAULT CURRENT_TIMESTAMP                            |

---

### **7. 活动表（Activity）**

| 属性名   | 字段名      | 数据类型           | 数据说明         | 约束                                           |
| -------- | ----------- | ------------------ | ---------------- | ---------------------------------------------- |
| 活动ID   | activity_id | INT AUTO_INCREMENT | 活动的唯一标识   | PRIMARY KEY                                    |
| 商铺ID   | shop_id     | INT                | 举办活动的商铺ID | FOREIGN KEY REFERENCES Shop(shop_id), NOT NULL |
| 活动名称 | name        | VARCHAR(255)       | 活动的名称       | NOT NULL                                       |
| 活动描述 | description | TEXT               | 活动的详细描述   |                                                |
| 开始日期 | start_date  | DATETIME           | 活动的开始时间   | NOT NULL                                       |
| 结束日期 | end_date    | DATETIME           | 活动的结束时间   | NOT NULL                                       |

---

### **8. 活动商品表（ActivityProduct）**

| 属性名 | 字段名        | 数据类型     | 数据说明             | 约束                                                   |
| ------ | ------------- | ------------ | -------------------- | ------------------------------------------------------ |
| 活动ID | activity_id   | INT          | 所属活动的ID         | FOREIGN KEY REFERENCES Activity(activity_id), NOT NULL |
| 商品ID | product_id    | INT          | 参与活动的商品ID     | FOREIGN KEY REFERENCES Product(product_id), NOT NULL   |
| 折扣率 | discount_rate | DECIMAL(3,2) | 商品在活动中的折扣率 |                                                        |
| 备注   | note          | VARCHAR(255) | 其他说明             |                                                        |

**约束**：

- **PRIMARY KEY (activity_id, product_id)**：确保同一活动和商品的组合唯一。

---

### **9. 购物车表（ShoppingCart）**

| 属性名   | 字段名      | 数据类型           | 数据说明         | 约束                                                   |
| -------- | ----------- | ------------------ | ---------------- | ------------------------------------------------------ |
| 购物车ID | cart_id     | INT AUTO_INCREMENT | 购物车的唯一标识 | PRIMARY KEY                                            |
| 用户ID   | user_id     | INT                | 所属用户的ID     | FOREIGN KEY REFERENCES User(user_id), UNIQUE, NOT NULL |
| 创建日期 | create_date | DATETIME           | 购物车创建时间   | DEFAULT CURRENT_TIMESTAMP                              |

**约束**：

- **UNIQUE (user_id)**：每个用户只有一个购物车。

---

### **10. 购物车商品表（CartItem）**

| 属性名     | 字段名       | 数据类型           | 数据说明             | 约束                                                   |
| ---------- | ------------ | ------------------ | -------------------- | ------------------------------------------------------ |
| 购物车项ID | cart_item_id | INT AUTO_INCREMENT | 购物车项的唯一标识   | PRIMARY KEY                                            |
| 购物车ID   | cart_id      | INT                | 所属购物车的ID       | FOREIGN KEY REFERENCES ShoppingCart(cart_id), NOT NULL |
| 商品ID     | product_id   | INT                | 加入购物车的商品ID   | FOREIGN KEY REFERENCES Product(product_id), NOT NULL   |
| 数量       | quantity     | INT                | 购物车中商品的数量   | NOT NULL, CHECK (quantity > 0)                         |
| 添加日期   | added_date   | DATETIME           | 商品加入购物车的时间 | DEFAULT CURRENT_TIMESTAMP                              |

---

### **11. 地址表（Address）**

| 属性名       | 字段名         | 数据类型           | 数据说明       | 约束                                           |
| ------------ | -------------- | ------------------ | -------------- | ---------------------------------------------- |
| 地址ID       | address_id     | INT AUTO_INCREMENT | 地址的唯一标识 | PRIMARY KEY                                    |
| 用户ID       | user_id        | INT                | 所属用户的ID   | FOREIGN KEY REFERENCES User(user_id), NOT NULL |
| 收件人姓名   | recipient_name | VARCHAR(255)       | 收货人的姓名   | NOT NULL                                       |
| 地址         | address_line1  | VARCHAR(255)       | 地址信息       | NOT NULL                                       |
| 城市         | city           | VARCHAR(255)       | 所在城市       | NOT NULL                                       |
| 省/州        | state          | VARCHAR(255)       | 所在省份或州   |                                                |
| 邮政编码     | zip_code       | VARCHAR(20)        | 邮编           |                                                |
| 电话号码     | phone          | VARCHAR(50)        | 收货人联系电话 | NOT NULL                                       |
| 是否默认地址 | is_default     | BOOLEAN            | 是否为默认地址 | DEFAULT FALSE                                  |

---

### **12. 用户反馈表（Feedback）**

| 属性名   | 字段名        | 数据类型           | 数据说明       | 约束                                                       |
| -------- | ------------- | ------------------ | -------------- | ---------------------------------------------------------- |
| 反馈ID   | feedback_id   | INT AUTO_INCREMENT | 反馈的唯一标识 | PRIMARY KEY                                                |
| 评价ID   | review_id     | INT                | 被回复的评价ID | FOREIGN KEY REFERENCES Review(review_id), UNIQUE, NOT NULL |
| 商家ID   | merchant_id   | INT                | 回复的商家ID   | FOREIGN KEY REFERENCES Merchant(merchant_id), NOT NULL     |
| 回复内容 | content       | TEXT               | 商家的回复内容 | NOT NULL                                                   |
| 回复日期 | feedback_date | DATETIME           | 回复的时间     | DEFAULT CURRENT_TIMESTAMP                                  |

**约束**：

- **UNIQUE (review_id)**：每条评价只能有一个商家回复。

## 功能与数据流

**1. 商家注册和登录**

- **功能描述**：商家可以注册账户并登录系统。
- **发起实体**：商家
- **数据流**：
  - **注册**：
    - 商家填写注册信息（商家名称、联系方式、邮箱、密码）。
    - 系统在 **Merchant** 表中插入一条新记录。
  - **登录**：
    - 商家提供邮箱和密码。
    - 系统验证 **Merchant** 表中的记录。

---

**2. 商家创建商铺**

- **功能描述**：商家可以创建新的商铺。
- **发起实体**：商家
- **数据流**：
  - 商家填写商铺信息（商铺名称、地址、联系方式、描述）。
  - 系统在 **Shop** 表中插入一条新记录。
  - 在 **MerchantShop** 表中插入一条新记录，关联商家和商铺。

---

**3. 商家管理商铺**

- **功能描述**：商家可以编辑、更新商铺信息。
- **发起实体**：商家
- **数据流**：
  - 商家修改商铺信息。
  - 系统更新 **Shop** 表中的对应记录。

---

**4. 商家添加商品**

- **功能描述**：商家可以在商铺中添加新商品。
- **发起实体**：商家
- **数据流**：
  - 商家填写商品信息（商品名称、描述、价格、库存、类别、状态等）。
  - 系统在 **Product** 表中插入一条新记录，关联到对应的商铺（shop_id）。

---

**5. 商家管理商品**

- **功能描述**：商家可以编辑、更新商品信息，如价格、库存、状态等。
- **发起实体**：商家
- **数据流**：
  - 商家修改商品信息。
  - 系统更新 **Product** 表中的对应记录。

---

**6. 用户注册和登录**

- **功能描述**：用户可以注册账户并登录系统。
- **发起实体**：用户
- **数据流**：
  - **注册**：
    - 用户填写注册信息（用户名、密码、邮箱、电话号码）。
    - 系统在 **User** 表中插入一条新记录。
  - **登录**：
    - 用户提供用户名和密码。
    - 系统验证 **User** 表中的记录。

---

**7. 用户浏览商品**

- **功能描述**：用户可以浏览商品列表和详情。
- **发起实体**：用户
- **数据流**：
  - 系统从 **Product** 表中读取商品信息，展示给用户。

---

**8. 用户添加商品到购物车**

- **功能描述**：用户可以将商品加入购物车。
- **发起实体**：用户
- **数据流**：
  - 如果用户没有购物车，系统在 **ShoppingCart** 表中为该用户创建一条新记录。
  - 在 **CartItem** 表中插入一条新记录，包含购物车ID、商品ID、数量等信息。

---

**9. 用户查看和管理购物车**

- **功能描述**：用户可以查看、修改购物车中的商品数量，或移除商品。
- **发起实体**：用户
- **数据流**：
  - 系统从 **CartItem** 表中读取用户购物车中的商品列表。
  - 用户更新商品数量或删除商品。
  - 系统更新或删除 **CartItem** 表中的对应记录。

---

**10. 用户下订单**

- **功能描述**：用户可以对购物车中的商品下订单。
- **发起实体**：用户
- **数据流**：
  - 用户选择购物车中的商品，确认订单信息和收货地址。
  - 系统在 **Order** 表中插入一条新记录，包含订单详情（用户ID、商品ID、数量、单价、总金额、订单日期、状态、地址ID等）。
  - 更新 **Product** 表中的库存数量（减去购买的数量）。
  - 从 **CartItem** 表中删除已下单的商品。

---

**11. 用户支付订单**

- **功能描述**：用户可以支付已下的订单。
- **发起实体**：用户
- **数据流**：
  - 用户选择待支付的订单。
  - 系统更新 **Order** 表中的订单状态为“已支付待收货”。

---

**12. 用户确认收货**

- **功能描述**：用户确认订单收货，完成交易。
- **发起实体**：用户
- **数据流**：
  - 用户在订单详情中确认收货。
  - 系统更新 **Order** 表中的订单状态为“已完成”。

---

**13. 用户管理收货地址**

- **功能描述**：用户可以添加、编辑、删除收货地址，并设置默认地址。
- **发起实体**：用户
- **数据流**：
  - **添加地址**：
    - 用户填写地址信息。
    - 系统在 **Address** 表中插入一条新记录。
  - **编辑地址**：
    - 用户修改地址信息。
    - 系统更新 **Address** 表中的对应记录。
  - **删除地址**：
    - 用户选择要删除的地址。
    - 系统从 **Address** 表中删除对应记录。
  - **设置默认地址**：
    - 用户选择默认地址。
    - 系统更新 **Address** 表，设置对应记录的 `is_default` 字段为 `TRUE`，并将其他地址的 `is_default` 设为 `FALSE`。

---

**14. 用户查看订单历史**

- **功能描述**：用户可以查看自己的订单历史记录。
- **发起实体**：用户
- **数据流**：
  - 系统从 **Order** 表中读取该用户的所有订单记录，展示给用户。

---

**15. 用户对商品进行评价**

- **功能描述**：用户可以对已购买的商品进行评价和评分。
- **发起实体**：用户
- **数据流**：
  - 用户在订单完成后，对商品进行评价，填写评分和评论内容。
  - 系统在 **Review** 表中插入一条新记录，包含用户ID、商品ID、订单ID、评分、评论内容、评价日期等。

---

**16. 商家回复用户评价**

- **功能描述**：商家可以回复用户的商品评价。
- **发起实体**：商家
- **数据流**：
  - 商家查看用户的评价。
  - 商家填写回复内容。
  - 系统在 **Feedback** 表中插入一条新记录，包含评价ID、商家ID、回复内容、回复日期等。

---

**17. 商家创建活动**

- **功能描述**：商家可以为商铺创建促销活动。
- **发起实体**：商家
- **数据流**：
  - 商家填写活动信息（活动名称、描述、开始日期、结束日期等）。
  - 系统在 **Activity** 表中插入一条新记录，关联到对应的商铺（`shop_id`）。

---

**18. 商家添加商品到活动**

- **功能描述**：商家可以将商品添加到活动中，设置折扣率等信息。
- **发起实体**：商家
- **数据流**：
  - 商家选择活动和商品，设置折扣率、备注等。
  - 系统在 **ActivityProduct** 表中插入一条新记录，包含活动ID、商品ID、折扣率、备注等。

---

**19. 用户浏览活动和促销商品**

- **功能描述**：用户可以浏览商铺的促销活动及其商品。
- **发起实体**：用户
- **数据流**：
  - 系统从 **Activity** 表和 **ActivityProduct** 表中读取活动和促销商品信息，展示给用户。

---

**20. 用户重置密码**

- **功能描述**：用户可以重置登录密码。
- **发起实体**：用户
- **数据流**：
  - 用户申请重置密码，验证身份（如通过邮箱验证）。
  - 系统更新 **User** 表中的密码字段。

---

**21. 商家重置密码**

- **功能描述**：商家可以重置登录密码。
- **发起实体**：商家
- **数据流**：
  - 商家申请重置密码，验证身份（如通过邮箱验证）。
  - 系统更新 **Merchant** 表中的密码字段。

---

**22. 用户申请退款或退货**

- **功能描述**：用户可以对已购买的商品申请退款或退货。
- **发起实体**：用户
- **数据流**：
  - 用户在订单详情中申请退款或退货，填写原因。
  - 系统更新 **Order** 表中的状态为“退款中”或“退货中”（此功能需要在 **Order** 表中添加相应的状态字段）。

---

**23. 商家处理退款或退货申请**

- **功能描述**：商家可以处理用户的退款或退货申请。
- **发起实体**：商家
- **数据流**：
  - 商家查看退款或退货申请。
  - 商家同意或拒绝申请。
  - 系统更新 **Order** 表中的状态（如“退款完成”、“退货完成”或“申请拒绝”）。
  - 如果退款或退货完成，需要调整 **Product** 表中的库存数量（退货时）。

---

**24. 系统发送通知**

- **功能描述**：系统在订单状态变化、评价回复等情况下，向用户或商家发送通知。
- **发起实体**：系统
- **数据流**：
  - 根据触发事件，系统生成通知内容。
  - （需要新增 **Notification** 表，记录通知信息）。

---

**25. 数据统计和报表（可选）**

- **功能描述**：商家可以查看销售数据、商品销量等统计信息。
- **发起实体**：商家
- **数据流**：
  - 系统从 **Order**、**Product** 等表中汇总统计数据，生成报表。

---

**26. 用户搜索商品**

- **功能描述**：用户可以根据关键字、类别等搜索商品。
- **发起实体**：用户
- **数据流**：
  - 用户输入搜索条件。
  - 系统从 **Product** 表中查询符合条件的商品，展示给用户。

---

**27. 用户收藏商品或商铺（可选）**

- **功能描述**：用户可以收藏感兴趣的商品或商铺。
- **发起实体**：用户
- **数据流**：
  - （需要新增 **收藏表**，如 **Favorite** 表）。
  - 用户收藏商品或商铺。
  - 系统在 **Favorite** 表中插入记录。



---

**28. 商家添加其他商家为合伙人**

- **功能描述**：商家可以与其他商家共同管理商铺（通过生成一个邀请码？）。
- **发起实体**：商家
- **数据流**：
  - 商家邀请其他商家加入商铺管理。
  - 系统在 **MerchantShop** 表中插入新的关联记录。

---

**29. 用户查看商家回复**

- **功能描述**：用户可以查看商家对自己评价的回复。
- **发起实体**：用户
- **数据流**：
  - 系统从 **Feedback** 表中读取与用户评价相关的回复，展示给用户。
