#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response



def Pager(page,all_page_count):
    page_html = []

    first_page = '<a href="%d">首页</a>' % (1)
    page_html.append(first_page)
    if page <= 1:
        prev_page = '<a href="#">上一页</a>'
    else:
        prev_page = '<a href="%d">上一页</a>' % (page - 1)

    page_html.append(prev_page)

    for h in range(all_page_count):

        if page == h + 1:
            a_html = '<a class="selected" href="%d">%d</a>' % (h + 1, h + 1)
        else:
            a_html = '<a  href="%d">%d</a>' % (h + 1, h + 1)
        page_html.append(a_html)

    next_page = '<a href="%d">下一页</a>' % (page + 1)
    page_html.append(next_page)

    end_page = '<a href="%d">尾页</a>' % (all_page_count)
    page_html.append(end_page)

    page = mark_safe(''.join(page_html))
    return page
