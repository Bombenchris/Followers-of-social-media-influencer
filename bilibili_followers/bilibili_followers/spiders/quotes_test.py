import scrapy
import json
from scrapy.http import FormRequest
from ..items import BilibiliFollowersItem


class FollowerSpider(scrapy.Spider):
    name = 'followers'
    start_urls = [
        # 'https://www.bilibili.com/v/douga/other/' # Animation others
        #  'https://www.bilibili.com/v/douga/mad/'  # Animation MAD.AMV
        # 'https://www.bilibili.com/v/cinephile/montage/'  # cinephile/montage
        'https://www.bilibili.com/v/ent/star/'
    ]
    headers = {
        "accept": "*/*",
        "cache-control": "no-cache",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referer": "{}".format(start_urls[0]),
        "cookie": "bsource=seo_google; _uuid=1B06E8DC-4261-4F4F-E7EF-8641AD24200691958infoc; buvid3=27774F2D-C97D-4758-A45B-FFC63740895A155830infoc; PVID=1; CURRENT_FNVAL=16; sid=6rsp66f6",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    items = BilibiliFollowersItem()

    def parse(self, response):
        callback = 'jqueryCallback_bili_9774461024721197'
        pagesize = '20'
        cate_id = '137'  # different tag chanel id, music_others(130),  music_original(28) douga/other(27)
        # Movie_montage (183) # ent/star 137

        for month in range(4):
            time_from = '20200{}01'.format(month+1)
            time_to = '20200{}29'.format(month+1)
            # from page 1 to 500, 20 items per page
            for i in range(200):
                # url = 'https://api.bilibili.com/x/relation/followers?vmid=546195&pn=1&ps=20&order=desc'
                url = 'https://s.search.bilibili.com/cate/search?callback=' + callback \
                      + '&search_type=video&view_type=hot_rank' \
                      + '&order=click&copy_right=-1&cate_id=' + cate_id + '&page=' \
                      + str(i+1) + '&pagesize=' \
                      + pagesize + '&time_from=' + time_from + '&time_to=' + time_to

                request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
                # FollowerSpider.page_n += 1
                yield request

    def parse_api(self, response):
        LOAD = json.loads(response.body)
        LOAD = LOAD['result']
        for candidate in LOAD:
            mid = candidate['mid']
            follower_url = 'https://api.bilibili.com/x/relation/followers?vmid=' + str(mid) + '&pn=1&ps=20&order=desc'
            request = scrapy.Request(follower_url, callback=self.parse_follower)
            request.cb_kwargs['mid'] = mid  # add more arguments for the callback
            yield request

    def parse_follower(self, response, mid):
        followings = json.loads(response.body)
        followings = followings['data']
        followings_total = followings['total']

        FollowerSpider.items['USER'] = mid
        FollowerSpider.items['FOLLOWERS'] = followings_total

        yield FollowerSpider.items

        # followings_info = followings['list']
        # mid_uname = []
        # for x in followings_info:
        #     mid_uname.append({'mid': x['mid'], 'uname': x['uname']})
