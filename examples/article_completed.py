"""
In order for an article to be completed it must have the following rules
    1. ArticleStockUpdated where stock is > 0
    2. ArticleImageUploaded where the image url is present
    3. ArticlePriceUpdated where the price exists

"""
from collections import namedtuple
from typing import Union

from src.rules_engine import Otherwise, Rule, RulesEngine, then

Article = namedtuple("Article", "title price image_url stock")
article = Article(title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None)


def produce_article_completed_event():
    return None


def article_controller(article: Article) -> Union[bool, None]:
    if not article.stock:
        return False
    if not article.price:
        raise ValueError("Article price missing")
    if not article.image_url:
        raise ValueError("Article image_url missing")
    return produce_article_completed_event()


"""
To be able to change to rules engine
    1. We need to split the conditions
    2. And actions

    Rules engine is pretty simple if the condition is True
    The rules engine will run the action
"""

# Conditions
def no_article_stock(article):
    return not article.stock


def no_article_price(article):
    return not article.price


def no_article_image_url(article):
    return not article.image_url


# Actions
def article_price_missing_error(article):
    raise ValueError("Article price missing")


def article_image_missing_error(article):
    raise ValueError("Article image_url missing")


def article_complete_rules(article):
    RulesEngine(
        Rule(no_article_stock, then(False)),
        Rule(no_article_price, article_price_missing_error),
        Rule(no_article_image_url, article_image_missing_error),
        Otherwise(produce_article_completed_event()),
    ).run(article)
