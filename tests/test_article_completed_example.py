from collections import namedtuple

import pytest

from src.rules_engine import Otherwise, Rule, RulesEngine, not_, then, Result

Article = namedtuple("Article", "title price image_url stock")


def article_stock_missing(article):
    return not article.stock


def article_price_missing(article):
    return not article.price


def article_image_missing(article):
    return not article.image_url


@pytest.mark.parametrize(
    "article, expected_result, message",
    [
        (
            Article(
                title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None
            ),
            False,
            "article stock missing",
        ),
        (
            Article(title="Iphone Case", price=None, image_url="http://image", stock=10),
            False,
            "article_price_missing",
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="", stock=10),
            False,
            "article_image_missing",
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="http://image", stock=10),
            True,
            None,
        ),
    ],
)
def test_article_complete_rules(article, expected_result, message):
    result = RulesEngine(
        Rule(article_stock_missing, then(False), message="article stock missing"),
        Rule(article_price_missing, then(False)),
        Rule(article_image_missing, then(False)),
        Otherwise(then(True)),
    ).run(article)

    result.value = expected_result
    result.message = message


@pytest.mark.parametrize(
    "article, expected_result",
    [
        (
            Article(
                title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None
            ),
            [
                Result(value='B', message='article price missing'),
                Result(value='C', message='article image missing'),
            ],
        ),
        (
            Article(title="Iphone Case", price=None, image_url="http://image", stock=10),
            [
                Result(value='A', message='article stock missing'),
                Result(value='C', message='article image missing'),
            ],
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="", stock=10),
            [
                Result(value='A', message='article stock missing'),
                Result(value='B', message='article price missing'),
            ],
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="http://image", stock=10),
            [
                Result(value='A', message='article stock missing'),
                Result(value='B', message='article price missing'),
                Result(value='C', message='article image missing'),
            ],
        ),
    ],
)
def test_article_complete_all_rules(article, expected_result):
    result = RulesEngine(
        Rule(not_(article_stock_missing), then("A"), message="article stock missing"),
        Rule(not_(article_price_missing), then("B"), message="article price missing"),
        Rule(not_(article_image_missing), then("C"), message="article image missing"),
    ).run_all(article)
    assert result == expected_result
