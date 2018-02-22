# coding: utf-8


def add_one(value):
    return int(value) + 1


def format_time(time_obj):
    return time_obj.strftime('%m-%d')


def html_to_text(html):
    import re
    replace_list = re.findall('<.*?>', html)
    for r in replace_list:
        html = html.replace(r, '')
    return html


def time_human(t):
    from datetime import datetime
    try:
        t_now = datetime.now()
        t_obj = t
        if t_obj > t_now:
            return t
        dist = t_now-t_obj
        dist_days = dist.days
        dist_seconds = dist.seconds
        if dist_days == 0:
            if dist_seconds < 60:
                return '刚刚'
            if dist_seconds/60 < 60:
                return '{}分钟前'.format(int(dist_seconds/60))
            if dist_seconds/3600 < 24:
                return '{}小时前'.format(int(dist_seconds/3600))
        else:
            if dist_days < 30:
                return '{}天前'.format(dist_days)
            if dist_days < 365:
                return '{}个月前'.format(int(dist_days/30))
            else:
                return t
    except:
        return t


if __name__ == '__main__':
    t = '2018-01-17 21:56:40'
    print(time_human(t))