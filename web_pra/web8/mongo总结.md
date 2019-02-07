# mongodb 使用总结

## 安装

使用`homebrew`安装, 
安装以后需要配置环境变量, 在`.bash_profile`和`.zshrc`里面加上`export PATH=/usr/local/Cellar/mongodb/4.0.3_1/bin:$PATH`, 然后`source`使文件生效. 
同时需要在 root 目录下新建数据目录, 如下:

```bash
mkdir -p /data/db
```

## 使用
`mongod`用来开启服务器
`mongo`用来启动`mongodDB shell`, 命令行客户端

先使用`mongod`开启服务端, 再使用`mongo`打开命令行

## 错误

安装过程中出现的一些错误:

- `/data/db` 访问权限, 使用`sudo chmod -R 0777 /data/db`赋予权限
- 端口占用, `mongodb`使用`27017`, 使用`lsof -i:27017`查看占用的端口, `sudo killall -15 mongod`清除所有的端口(注意不要使用`kill -9 <PID>`)
- `mongod --repair`来修复错误
- `sudo service mongod start` 开启服务器

## Reference
- https://www.jianshu.com/p/40f8cc23af5d
- https://stackoverflow.com/questions/5798549/why-cant-i-start-the-mongodb
- https://stackoverflow.com/questions/6478113/unable-to-start-mongodb-local-server
- https://stackoverflow.com/questions/42446931/mongodb-exception-in-initandlisten-20-attempted-to-create-a-lock-file-on-a-rea
