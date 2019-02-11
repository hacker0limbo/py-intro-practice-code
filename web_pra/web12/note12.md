# 服务器和域名

## 服务器

使用`ssh keys`登录: 用`ssh root@ip`登录远程服务器, 在服务器新建`~/root/.ssh/authorised_keys`, 内容为公钥, 或者使用`cat id_dsa.pub >> ~/.ssh/authorized_keys`, `service ssh restart`重启服务器.

## linux 命令

pwd
    print working dir
    显示现在所处的目录

ls
    不带参数就显示当前目录下的所有文件
    程序可以加参数
    -l 显示详细信息
    -h 人性化显示文件尺寸
    -a 显示所有文件， 以 . 开头的文件是隐藏文件
    还可以带一个目录当参数，这样就会显示这个目录
下面两个是等价的
ls -l -h
ls -lh

cd
    cd Desktop
    改变当前目录
    . 代表当前目录
    .. 代表上级目录
    cd 不带参数就回到默认的家目录
    每个用户都有一个家目录，默认在 /home/用户名
    root 用户的家目录是 /root
cp
    复制出一个文件，用法如下
    cp a.txt b.txt
    复制 a.txt 并把新文件取名为 b.txt
    复制目录要加上 -r 参数
    cp -r a b
mkdir
    创建一个目录
    -p 可以一次性创建多层目录
    mkdir -p a/b/c
rmdir
    只能用来删除一个空目录
rm
    这个命令直接删除东西，很危险，一般不要用
    删除文件或者目录
    -f 强制删除
    -r 用来删除目录
mv
    移动文件或者文件夹
    也可以用来改名
    mv a.txt b.txt
    mv b.txt ../
    mv b.txt ../gua.txt
    可以用 mv xx /tmp 的方式来将文件放入临时文件夹
    （/tmp是操作系统提供的临时文件夹，重启会删除里面的所有文件）
cat
    显示文件内容
tac
    反过来显示文件内容
nl
    显示内容并附带行号
more less head tail
    more 可以分屏分批看文件内容
    less 比 more 更高级，可以前后退看文件
    head 可以显示文件的前 10 行
    tail 可以显示文件的后 10 行
    head 和 tail 有一个 -n 参数
    head -n 20 a.gua
touch
    touch a.gua
    如果 a.gua 存在就更新修改时间
    如果 a.gua 不存在就创建文件

目录分布


权限操作
sudo
    用管理员帐户执行程序
    比如安装程序或者修改一些系统配置都需要管理员权限
su
    switch user， 切换用户
    su gua
    su root

文件权限    文件类型 用户 用户组 文件大小  修改日期     文件名
-rw-rw-r--  1       gua gua     10      11/09 20:28 b.gua
drwxrwxr-x  2       gua gua     4096    11/09 20:28 tmp
文件类型    是否可读  是否可写  是否可执行
d           r       w           x
-           r       w           x
三组 rwx 分表代表 所属用户|同组用户|其他用户
rwx 可以用数字表示为 421
于是乎
r-- 就是 4
rw- 就是 6
rwx 就是 7
r-x 就是 5

chown
    改变文件的用户
    chown gua c.gua
    chown gua:gua c.gua
chmod
    改变文件权限
    chmod 666 root.gua
    chmod +x root.gua
    chmod -x tmp


信息查找
file
    显示文件的类型（不是百分之百准确）
uname
    显示操作系统的名字或者其他信息
    uname -r
    uname -a
which
    which pwd
    显示 pwd 的具体路径
whereis
    whereis ls
    显示更全面的信息
whoami
find . -name ""

奇怪符号
~   家目录快捷方式
>   覆盖式重定向
>>  追加重定向
|   管道, 很麻烦 以后说
``  获取命令执行的结果
&   后台执行
    python3 server.py &
    可以用 fg 命令把一个在后台的程序拉到前台来
    可以用 Ctrl-z 来把一个前台的程序放到后台去挂起
()  开新的子进程shell执行(不用掌握这一条, 因为几乎没人用)


history
    查看历史命令
grep
    查找
这两个一般配合使用
    history | grep touch

ps
    查看进程, 一般用下面的用法
    ps ax
ps ax | grep python
    查看带 python 字符串的进程

kill 和 killall 杀进程
    用 ps ax 找到进程id (pid)
    kill [pid]
    kill -9 [pid]
    kill -15 [pid]
    killall 是用进程名字来杀进程

后台前台
fg
jobs

快捷键
C-z 挂起到后台
C-c 中断程序



reboot
    重启
shutdown
    关机
    可以用参数指定时间
halt
    关机

