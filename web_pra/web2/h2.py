def path_with_query(path: str, query: dict):
    """
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url, 见测试

    # 注意, 字典是无序的, 不知道哪个参数在前面
    """
    u = path + '?'
    for k, v in query.items():
        u += f'{k}={v}&'
    u = u[:-1]
    return u


def header_from_dict(headers: dict):
    """
    headers 是一个字典
    范例如下
    对于
    {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    """
    header = ''
    for k, v in headers.items():
        header += f'{k}: {v}\r\n'
    return header


def value_from_element(html: str, element: str):
    """
    返回一段 html 里面的所有子元素, html 为该元素所在的 html 结构, 实例如下:

    html =
        <ol>
            <li class="name">gua</li>
        </ol>

    value_from_element(html, '<li class="name">gua</li>') -> gua
    """
    elm_start_index = html.find(element)
    elm_end_index = html.find('</', elm_start_index)
    elm = html[elm_start_index:elm_end_index]
    value = elm.split('>')[1]
    return value


def parsed_films(html: str):
    """
    https://movie.douban.com/top250
    client_ssl.py 获取数据, 解析出:

    1，电影名
    2，分数
    3，评价人数
    4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）
    """
    films = []

    ol_start = html.find('<ol class="grid_view">')
    ol_end = html.find('</ol>')
    # s = <ol class="grid_view"> <li>...</li>
    items = html[ol_start:ol_end].split('<li>')[1:]
    for item in items:
        title_elm = '<span class="title">'
        title = value_from_element(item, title_elm)

        rating_elm = '<span class="rating_num" property="v:average">'
        rating = value_from_element(item, rating_elm)
        rating = float(rating)

        comments_elm = '<span>'
        comments = value_from_element(item, comments_elm)
        comments = int(comments.split('人评价')[0])

        quote_elm = '<span class="inq">'
        quote = value_from_element(item, quote_elm)

        films.append({
            'title': title,
            'rating': rating,
            'comments': comments,
            'quote': quote,
        })

    return films


def main():
    with open('douban.txt', 'r') as f:
        html = f.read()
        films = parsed_films(html)
        print(films)


if __name__ == '__main__':
    main()
