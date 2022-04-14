import os

import pytest

from crawler.umamusume import *


@pytest.fixture(scope="module")
def soup():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/266048")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, 'lxml')


def test_umamusume_info_table(soup):
    data = get_umamusume_info_table(soup)
    expect = {
        "初期レア": "星3",
        "名称": "エンド・オブ・スカイ",
        "入手方法": "ウマ娘ガチャから入手",
        "固有二つ名": "名優",
        "おすすめ距離": "長距離、中距離",
        "おすすめ脚質": "逃げ、先行"
    }
    assert data == expect


def test_umamusume_name(soup):
    actual = get_umamusume_name(soup)
    expect = "メジロマックイーン(新衣装)"
    assert actual == expect


def test_umamusume_event(soup):
    actual = get_umamusume_event(soup)
    expect = {
        "title": "孤島の女王",
        "event_choice": {
            "食料": "スピード+10",
            "体力": "スタミナ+10"
        }
    }
    assert actual[0] == expect
    assert len(actual) == 24


def test_umamusume_event_choice():
    fixture = '<div class="uma_choice_table">' \
              '<table><tr><th>やった、やったぞーっ！！</th>' \
              '<td>体力-15<br/>5種ステータスからランダムに1種を+5<br/>スキルPt+30</td></tr>' \
              '<tr><th>更なる高みを目指そう！</th>' \
              '<td>体力-5~20<br/>5種ステータスからランダムに1種を+5~10<br/>スキルPt+30~45</td></tr>' \
              '</table></div>'

    soup = BeautifulSoup(fixture, 'lxml')
    actual = get_umamusume_event_choice(soup)
    expect = {
        "やった、やったぞーっ！！": "体力-15\n5種ステータスからランダムに1種を+5\nスキルPt+30",
        "更なる高みを目指そう！": "体力-5~20\n5種ステータスからランダムに1種を+5~10\nスキルPt+30~45"
    }

    assert actual == expect


def test_umamusume_illust_url(soup):
    actual = get_umamusume_illust_url(soup)
    expect = 'https://img.gamewith.jp/article_tools/uma-musume/gacha/i_30.png'

    assert actual == expect


def test_integration():
    crawl_new_umamusume("https://gamewith.jp/uma-musume/article/show/266048")
