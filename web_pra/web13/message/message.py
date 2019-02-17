from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask(__name__)

message_list = []


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'


# GET 方法默认
@app.route('/message')
def message_view():
    print('请求方法', request.method)
    # request.args 保存 URL 中的参数的属性
    print('request, query 参数', request.args)
    return render_template('message_index.html', messages=message_list)


@app.route('/message/add', methods=['POST'])
def message_add():
    msg = {
        # 使用 get 获得 post 数据, 若无数据, 会报错
        'content': request.form.get('msg_post', ''),
    }
    message_list.append(msg)
    return redirect(url_for('message_view'))


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)

