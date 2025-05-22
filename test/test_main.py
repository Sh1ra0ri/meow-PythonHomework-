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
    assert isinstance(category_sample.products, str)
    assert len(category_sample.products.split("\n")) == 2
    assert "Сковорода, 1200.0 руб. Остаток: 10 шт." in category_sample.products
    assert "Кастрюля, 1800.0 руб. Остаток: 7 шт." in category_sample.products


def test_category_counter():
    Category.category_count = 0
    Category("Одежда", "Товары для взрослых")
    Category("Обувь", "Обувь для всех сезонов")
    assert Category.category_count == 2


def test_product_counter(category_sample, product_sample):
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
    assert "Чайник, 1500.0 руб. Остаток: 5 шт." in category_sample.products
    assert Category.product_count == initial + 1


def test_empty_category():
    Category.product_count = 0
    Category.category_count = 0
    empty = Category("Пустая", "Без товаров")
    assert empty.products == "Категория пуста"
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_price_setter(product_sample, capsys):
    product_sample.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_sample.price == 1500.0
    product_sample.price = 2000.0
    assert product_sample.price == 2000.0


def test_new_product_no_duplicates():
    product_data = {
        "name": "Тостер",
        "description": "Тостер для хлеба",
        "price": 2500.0,
        "quantity": 3,
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Тостер"
    assert new_product.description == "Тостер для хлеба"
    assert new_product.price == 2500.0
    assert new_product.quantity == 3


def test_new_product_with_duplicates():
    existing_products = [Product("Тостер", "Тостер для хлеба", 2000.0, 3)]
    product_data = {
        "name": "Тостер",
        "description": "Тостер для хлеба",
        "price": 2500.0,
        "quantity": 2,
    }
    updated_product = Product.new_product(product_data, existing_products)
    assert updated_product.quantity == 5  # 3 + 2
    assert updated_product.price == 2500.0


def test_add_product_subclass(category_sample):
    class SubProduct(Product):
        pass

    sub_product = SubProduct("Тостер", "Тостер для хлеба", 2000.0, 3)
    category_sample.add_product(sub_product)
    assert "Тостер, 2000.0 руб. Остаток: 3 шт." in category_sample.products
