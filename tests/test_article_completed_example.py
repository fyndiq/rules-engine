from collections import namedtuple

import pytest

from src.rules_engine import Otherwise, Rule, RulesEngine, not_, then

Article = namedtuple("Article", "title price image_url stock")


def article_stock_missing(article, message):
    return not article.stock


def article_price_missing(article, message):
    return not article.price


def article_image_missing(article, message):
    return not article.image_url


@pytest.mark.parametrize(
    "article, result",
    [
        (
            Article(
                title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None
            ),
            False,
        ),
        (
            Article(title="Iphone Case", price=None, image_url="http://image", stock=10),
            False,
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="", stock=10),
            False,
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="http://image", stock=10),
            True,
        ),
    ],
)
def test_article_complete_rules(article, result):
    assert result == RulesEngine(
        Rule(article_stock_missing, then(False)),
        Rule(article_price_missing, then(False)),
        Rule(article_image_missing, then(False)),
        Otherwise(then(True)),
    ).run(article)


@pytest.mark.parametrize(
    "article, result",
    [
        (
            Article(
                title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None
            ),
            ["B", "C"],
        ),
        (
            Article(title="Iphone Case", price=None, image_url="http://image", stock=10),
            ["A", "C"],
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="", stock=10),
            ["A", "B"],
        ),
        (
            Article(title="Iphone Case", price=1000, image_url="http://image", stock=10),
            ["A", "B", "C"],
        ),
    ],
)
def test_article_complete_all_rules(article, result):
    assert result == RulesEngine(
        Rule(not_(article_stock_missing), then("A")),
        Rule(not_(article_price_missing), then("B")),
        Rule(not_(article_image_missing), then("C")),
    ).run_all(article)
