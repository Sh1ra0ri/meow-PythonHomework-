import pytest
from src.main import Product, Category


@pytest.fixture
def product_sample():
    return Product("Чайник", "Электрический чайник", 1500.0, 5)


@pytest.fixture
def category_sample():
    Category.category_count = 0
    Category.product_count = 0
    products = [
        Product("Сковорода", "Сковорода с антипригарным покрытием", 1200.0, 10),
        Product("Кастрюля", "Кастрюля 3 литра", 1800.0, 7),
    ]
    return Category("Кухня", "Товары для кухни", products)


def test_product_init(product_sample):
    assert product_sample.name == "Чайник"
    assert product_sample.description == "Электрический чайник"
    assert product_sample.price == 1500.0
    assert product_sample.quantity == 5


def test_category_init(category_sample):
    assert category_sample.name == "Кухня"
    assert category_sample.description == "Товары для кухни"
    assert len(category_sample.products) == 2
    assert isinstance(category_sample.products[0], Product)


def test_category_counter():
    Category.category_count = 0
    Category("Одежда", "Товары для взрослых")
    Category("Обувь", "Обувь для всех сезонов")
    assert Category.category_count == 2


def test_product_counter(category_sample):
    assert Category.product_count == 2
    Category(
        "Книги",
        "Художественная литература",
        [Product("Роман", "Книга в твёрдой обложке", 500.0, 15)],
    )
    assert Category.product_count == 3


def test_add_product(category_sample, product_sample):
    initial = Category.product_count
    category_sample.add_product(product_sample)
    assert len(category_sample.products) == 3
    assert Category.product_count == initial + 1


def test_empty_category():
    Category.product_count = 0
    Category.category_count = 0
    empty = Category("Пустая", "Без товаров")
    assert empty.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0
