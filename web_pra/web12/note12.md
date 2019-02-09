# 服务器和域名

## 服务器

使用`ssh keys`登录: 用`ssh root@ip`登录远程服务器, 在服务器新建`~/root/.ssh/authorised_keys`, 内容为公钥, 或者使用`cat id_dsa.pub >> ~/.ssh/authorized_keys`, `service ssh restart`重启服务器.

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
