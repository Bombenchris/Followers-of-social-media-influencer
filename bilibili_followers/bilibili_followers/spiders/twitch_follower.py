import scrapy
from ..items import FollowersItem

from twitchAPI.twitch import Twitch
from twitchAPI.types import SortMethod


class twitch_follower(scrapy.Spider):
    name = 'followers'
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    items = FollowersItem()

    twitch = Twitch('x5chjai5leju0kgmqu4fh8l6hc5ycu', 'csopzwzqls7ogl2e35jvjm089gbyth')
    twitch.authenticate_app([])
    pagination_cursor = []
    edgePage_cursor = []
    i = 1

    def parse(self, response):

        game = twitch_follower.twitch.get_games(names='The Legend of Zelda: Breath of the Wild')
        gaming_id = game['data'][0]['id']

        # page range
        # for i in range(500):
        if not twitch_follower.pagination_cursor:
            # video = twitch_follower.twitch.get_videos(game_id=gaming_id, sort=SortMethod.VIEWS)
            streams = twitch_follower.twitch.get_streams(first=100, game_id=gaming_id)
            twitch_follower.pagination_cursor.append(streams['pagination']['cursor'])
        else:
            # go to next page
            streams = twitch_follower.twitch.get_streams(after=twitch_follower.pagination_cursor.pop(), first=100,
                                                         game_id=gaming_id)
            twitch_follower.pagination_cursor.append(streams['pagination']['cursor'])
            print(twitch_follower.i)
            twitch_follower.i += 1

        list_streams = streams['data']
        UniqueList_streams = list({myObject['user_id']: myObject for myObject in list_streams}.values())

        for user in UniqueList_streams:
            user_id = user['user_id']
            user_follows = twitch_follower.twitch.get_users_follows(to_id=user_id)
            user_infos = twitch_follower.twitch.get_users(user_ids=user_id)

            if user_infos['data']:
                user_followers = user_follows['total']
                view_count = user_infos['data'][0]['view_count']

                twitch_follower.items['ID'] = int(user_id)
                twitch_follower.items['USER'] = int(user_id)
                twitch_follower.items['FOLLOWERS'] = int(user_followers)
                twitch_follower.items['view_count'] = int(view_count)
                yield twitch_follower.items

        if 'cursor' in twitch_follower.twitch.get_streams(after=twitch_follower.pagination_cursor[0], first=100,
                                                          game_id=gaming_id)['pagination']:
            yield scrapy.Request('http://quotes.toscrape.com', callback=self.parse)

