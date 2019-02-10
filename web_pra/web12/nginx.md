# nginx 简介

- `sudo nginx -s reload` 重新加载配置文件
- `sudo service nginx restart` 重启 Nginx 服务
- `sudo nginx -s stop` 停止 Nginx 服务器

## 部署静态文件

`cd /etc/nginx`, 配置文件为`nginx.conf`


一个简单配置如下:

```js
server {
    listen 80;
    server_name [ip 地址];
    location / {
        # root 可以重新定义路径
        root /home/website;
    }

    location /img {
        root /home/website;
    }
}

```
假设网站为`www.example.com`, 输入`www.example.com/`会访问服务器文件`/home/website`, 访问`www.example.com/img`, 会访问服务器文件`/home/website/img`


## Reference

- https://fraserxu.me/2013/06/22/Nginx-for-developers/
- http://seanlook.com/2015/05/17/nginx-location-rewrite/
- https://showzeng.itscoder.com/nginx/2016/10/03/use-nginx-to-deploy-static-pages-easily.html
- https://blog.csdn.net/chinabestchina/article/details/73556785
- https://blog.csdn.net/name_is_wl/article/details/52958472