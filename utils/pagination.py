# --> 分页器方法

class Pagination():
    def __init__(self, page_num, len_customer, url, max_show=10, per_num=10):
        try:
            self.page_num = int(page_num)  # --> 当前页面的 序号
            if self.page_num <= 0:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1

        self.url = url  # --> 页面的URl
        self.max_show = max_show  # --> 最多显示的页码数
        self.per_num = per_num  # --> 一页显示数据条数
        half_show = self.max_show // 2  # --> 取得两边分页的长度, // 向下取值

        self.all_count, more = divmod(len_customer, self.per_num)

        if more:
            self.all_count = self.all_count + 1
        if self.all_count < self.max_show:
            self.max_show = self.all_count
            half_show = 0


        if self.page_num <= half_show:  # -->  倘若请求的页面小于2边分页的长度
            self.page_start = 1  # --> 分页起始值写死为1
            self.page_end = self.max_show + 1  # --> 分页结束值设置为最大值, 再加上当前页面的分页, 一共是11个分页
            print('11')

        elif self.page_num >= self.all_count - half_show:  # --> 倘若请求的页面大于  (全部页面数 - 分页数)
            self.page_start = self.all_count - self.max_show  # --> 起始页面 设置为 页面总数 - 最大长度
            self.page_end = self.all_count  # --> 结尾设置总数即可


        else:  # --> 其他正常情况保证当前分页的两侧有对应的数量的分页即可
            self.page_start = self.page_num - half_show
            self.page_end = self.page_num + half_show

        print(self.page_start, self.page_end)
        if self.page_start < 1:
            self.page_start = 1
    @property
    def start(self):
        return (self.page_num - 1) * self.per_num

    @property
    def end(self):
        return self.page_num * self.per_num

    @property
    def show_html(self):
        # --> 生成HTML
        self.html_page = ''
        print(self.page_num)
        if self.page_num > 1:
            self.html_page = '<li><a href="{url}?page=1" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>' \
                             '<li><a href="{url}?page={count}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' \
                .format(url=self.url, count=self.page_num - 1)

        else:
            self.html_page += '<li class="disabled"><span aria-hidden="true">首页</span></li><li class="disabled"><span aria-hidden="true">&laquo;</span></li>'

        for count in range(self.page_start, self.page_end + 1):
            page_is_active = ''
            if self.page_num == count:
                page_is_active = 'class="active"'
            self.html_page += '<li {active}><a href="{url}?page={count}">{count}</a></li>' \
                .format(active=page_is_active, url=self.url, count=count)

        if self.page_num < self.all_count:
            self.html_page += '<li><a href="{url}?page={count}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>' \
                              '<li><a href="{url}?page={all_count}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>' \
                .format(url=self.url, count=self.page_num + 1, all_count=self.all_count)
        else:
            self.html_page += '<li class="disabled"><span aria-hidden="true">&raquo;</span></li><li class="disabled"><span aria-hidden="true">尾页</span></li>'

        return self.html_page
