# 微博程序

运行`localhost:3000`访问主页

几个路由:

- `/`: 主页
- `/login`: 登录
- `/register`: 注册
- `/profile`: 个人信息
- `/todo`: todo 页面
- `/todo/edit`: todo 编辑界面
- `/weibo/index?id=[xxx]` 个人微博
- `/weibo/edit` 更新微博
- `/weibo/new` 添加新微博

其余路由在`routes`文件夹下面

## 总结

数据库使用`sqlite3`, 模板使用`jinja`, 该程序第一次使用数据库保存数据, 密码均使用摘要算法存储

### 数据库
可以使用`with`来自动提交数据, 或者可以自己写一个上下文管理器来管理数据库的开关

测试方法为在测试开始前新建临时表并插入数据, 结束时删除该表, 代码均在`test`目录下

### 问题

有时候数据库出错以后再次插入一条数据, id 不会接着原始数据继续增长, 而是从上条数据的 id 地方开始记录, 目前暂时不清楚原因,
删除重建该表恢复正常, 猜测是和缓存有关. 