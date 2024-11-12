# 修改记录 - 前端



| 时间        | 修改                                                         | 修改人 |
| ----------- | ------------------------------------------------------------ | ------ |
| 11.12 14:15 | server.ts get、post的参数传递方式，errorHandler新增选项是否显示snackbar | UUQ    |
|             |                                                              |        |



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

