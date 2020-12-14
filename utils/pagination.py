# --> 分页器方法

class Pagination():
    def __init__(self, search_params, page_num, all_count, url, max_show=10, per_num=10):
        try:
            self.page_num = int(page_num)  # --> 当前页面的 序号
            if self.page_num <= 0:
                self.page_num = 1

        except Exception as e:
            self.page_num = 1

        self.url = url  # --> 页面的URl
        self.search_params = search_params #--> 深copy过来的request.GET, 用于生成查询条件

        self.max_show = max_show  # --> 最多显示的页码数
        half_show = max_show // 2

        self.per_num = per_num  # --> 一页显示数据条数

        self.all_count, more = divmod(all_count, self.per_num)
        if more:
            self.all_count = self.all_count + 1

        if self.max_show > self.all_count:     #--> 当前数据的分页数小于最大分页数, 从第一页开始显示, 到当前数据的总数结束
            self.page_start = 1
            self.page_end = self.all_count
        else:   #--> 其他情况则为当前数据的分页数大于最大分页数
            if self.page_num <= half_show:  #--> 当前分页小于或等于 half_show, 意味着左边不需要处理
                self.page_start = 1 #--> 从1开始显示
                self.page_end = self.max_show   #--> 到最大分页数结束
            elif self.page_num + half_show > self.all_count:    #--> 当前分页 + half_show大于数据的总分页, 意味着数据的右边不需要处理
                self.page_start = self.all_count - max_show + 1 #--> 左边使用最大分页减去最大分页数+ 1得到左边的值
                self.page_end = self.all_count      #--> 右边使用all_count即可
            else:       #--> 其他则为左右都需要处理,
                self.page_start = self.page_num - half_show
                self.page_end = self.page_num + half_show
        #
        # if self.all_count < self.max_show:  # --> 倘若 数据不足以支撑指定的分页数, 那么最大分页数将设置为能够支撑的分页数
        #     self.max_show = self.all_count
        # #
        # elif self.all_count == self.max_show:   #--> 修复 当 数据量支撑的分页数和 最大分页数一样时, 避免额外加上自身导致多出来一个分页
        #     self.max_show = self.all_count - 1
        #
        # half_show = self.max_show // 2  # --> 取得两边分页的长度, // 向下取值
        # print('half_show', half_show)
        #
        # if self.page_num <= half_show:  # -->  倘若请求的页面小于2边分页的长度
        #     self.page_start = 1  # --> 分页起始值写死为1
        #     self.page_end = self.max_show + 1  # --> 分页结束值设置为最大值, 再加上当前页面的分页, 一共是11个分页
        #     if half_show == 1:      #--> 避免全部的分页数满足不了 half_show的长度,  额外加上自身导致多出来一个分页
        #         self.page_end = self.page_end -1
        #     print('a1')
        #
        # elif self.page_num >= self.all_count - half_show:  # --> 倘若请求的页面大于  (全部页面数 - 分页数)
        #     self.page_start = self.all_count - self.max_show  # --> 起始页面 设置为 页面总数 - 最大长度
        #     self.page_end = self.all_count  # --> 结尾设置总数即可
        #     print('a2')
        #
        #
        # else:  # --> 其他正常情况保证当前分页的两侧有对应的数量的分页即可
        #     self.page_start = self.page_num - half_show
        #     self.page_end = self.page_num + half_show
        #     print('a3')

        # if self.page_start < 1:
        #     self.page_start = 1
        # print(self.page_start , self.page_end )

    @property
    def start(self):
        return int((self.page_num - 1) * self.per_num)

    @property
    def end(self):
        return int(self.page_num * self.per_num)

    def _get_html(self, content, params=None): #--> 生成HTML的方法
        if not params:
            return '<li class="disabled"><span aria-hidden="true">{content}</span></li>'.format(content=content)
        return '<li><a href="{url}?{params}" aria-label="Previous"><span aria-hidden="true">{content}</span></a></li>'.format(
            url=self.url, params=params, content=content)

    @property
    def show_html(self):
        # --> 生成HTML
        self.html_page = ''
        if self.page_num > 1:
            self.search_params['page'] = 1 #--> 将分页的id传递到 request.GET中,
            #--> #--> self.search_params.urlencode() 使用 urlencode将全部的参数生成为url参数, 然后传递给生成HTML的方法里
            self.html_page += self._get_html('首页', self.search_params.urlencode())

            self.search_params['page'] = self.page_num - 1
            self.html_page += self._get_html('&laquo;', self.search_params.urlencode())

        else:
            self.html_page += self._get_html(content='首页')
            self.html_page += self._get_html(content='&laquo;')

        for count in range(self.page_start, self.page_end + 1):
            page_is_active = ''
            if self.page_num == count:
                page_is_active = 'class="active"'
            self.search_params['page'] = count
            self.html_page += '<li {active}><a href="{url}?{params}">{count}</a></li>'.format(active=page_is_active,
                                                                                              url=self.url,
                                                                                              params=self.search_params.urlencode(),
                                                                                              count=count
                                                                                              )

        if self.page_num < self.all_count:
            self.search_params['page'] = self.page_num + 1
            self.html_page += self._get_html('&raquo;', self.search_params.urlencode())

            self.search_params['page'] = self.all_count
            self.html_page += self._get_html('尾页', self.search_params.urlencode())
        else:
            self.html_page += self._get_html(content='&raquo;')
            self.html_page += self._get_html(content='尾页')
        return self.html_page
