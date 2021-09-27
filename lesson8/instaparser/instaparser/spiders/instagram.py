import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from lesson8.instaparser.instaparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']

    insta_login = '+79217259493'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1632723798:AdtQAOTZBJDUDk2ZMdFjJMBDs5+MWW7PQm10w2C4VO/mvCZ5m4U2y/h+aU3ypr0biZB2Qd3fdfvgyjV4H6pheQnTghBOwbM80O8EEaZnaVeSeayhVCXK/E4juU6O1lJWwO8oeNTyyQRlEw=='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    parse_users = ['pipetka797', 'nemov_foto']
    posts_hash = 'JRbKLhxwJ0bITqMOInf0eKT4rUjEtsyi'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    api_url = 'https://i.instagram.com/api/v1/friendships/'
    api_hash = 'JRbKLhxwJ0bITqMOInf0eKT4rUjEtsyi'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'X-CSRFToken': csrf}
                                 )
    def login(self, response: HtmlResponse):  # логинимся
        j_data = response.json()
        if j_data['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.follow_parse,
                    cb_kwargs={'username': user}    #передача пользователя с которым работаем
                )

    def follow_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'max_id': 12
        }
        api_followers = f'{self.api_url}{user_id}/followers/?count=12&{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(
            api_followers,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'source': 'followers',
                       'variables': deepcopy(variables)}
                       )

        api_following = f'{self.api_url}{user_id}/following/?count=12&{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(
            api_following,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'source': 'following',
                       'variables': deepcopy(variables)}
        )

    def user_follow_parse(self, response: HtmlResponse, username, user_id, source, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] += 12

            api_follow = f'{self.api_url}{user_id}/{source}/?count=12&{urlencode(variables)}&search_surface=follow_list_page'
            print()
            yield response.follow(
                api_follow,
                callback=self.user_follow_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'source': source,
                           'variables': deepcopy(variables)}
            )


        for follow in j_data['users']:
            item = InstaparserItem(
                username=username,
                source=source,
                user_id=follow.get('pk'),
                follow_name=follow.get('username'),
                follow_photo=follow.get('profile_pic_url')
            )
            yield item

    def fetch_csrf_token(self, text):
        # Получаем токен для авторизации
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username): #вызывается для каждого юзера
        # get user ID from the JavaScript in HTML
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
