# 修改记录 - 前端



| 时间        | 修改                                                         | 修改人 |
| ----------- | ------------------------------------------------------------ | ------ |
| 11.12 14:15 | server.ts get、post的参数传递方式，errorHandler新增选项是否显示snackbar | UUQ    |
| 11.12 19:00 | 增加cart一系列内容，但是UI丑陋，也因为没有商品还未完成测试              |    UUQ    |
| 11.15 00:20 | 完善了cart，初步UI设计 **TODO: 全选逻辑（半选）；库存判断；下架失效；批量删除等待接口** | UUQ |
| 11.18 23:00 | 完善cart，删除、库存判断 | 


## TODO

### Cart页
1. Cart页面更合理的布局和移动端简单适配。
2. 结算时快捷取消选中商品。
3. -quantity到0时二次确认
4. 一键删除无效商品


### Checkout页
1. 创建订单
2. 管理地址（新增、修改），以及“默认标识”
3. 返回修改后的bug（改数量）：原因，刷新后获取购物车得到的item和存在store的不是一个。wait for fix

## 具体说明

### 11.12 14:15

修改server.get和server.post的参数传递方式为对象式传参，并增加`showSnackbar`参数，这里展示get方法：

```typescript
const get = async ({ url, params, showSnackbar = true }: { url: string, params?: any, showSnackbar?: boolean }): Promise<Response> => {
	try {
  	const res = await server.get(url, { params })
		return res.data
	} catch (error) {
		errorHandler(error, showSnackbar);
		...
	}
};
```

调用时需要传入一个对象，如：`get({url: '/user/profile', data: {something}})`，好处是传参时更加灵活，但其实是不知道怎么处理比较好，于是出此下策。



### 11.15 00: 15

server.ts中增加了PUT和DELETE方法，但是DELETE是关键字所以改成了_delete。
