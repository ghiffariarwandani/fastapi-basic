from sqlmodel import Session, select

from app.models.database import Category, Product
from app.models.engine import engine
from app.types.enums import Currency

CATEGORY_SEEDS = [
    {"name": "Espresso Machine", "description": "Machines for making espresso shots"},
    {"name": "Grinder", "description": "Coffee grinders for espresso and manual brew"},
    {"name": "Dripper", "description": "Manual pour-over drippers"},
    {"name": "Beans", "description": "Coffee beans from various origins"},
    {"name": "Cup", "description": "Coffee cups and serving ware"},
]

PRODUCT_SEEDS = [
    {
        "sku": 1001,
        "name": "Breville Bambino Plus BES500",
        "description": "Compact espresso machine with PID and auto milk texturing",
        "price": 10999000.0,
        "currency": Currency.IDR,
        "stock": 10,
        "categories": ["Espresso Machine"],
    },
    {
        "sku": 1002,
        "name": "Gaggia Classic Pro",
        "description": "Single-boiler espresso machine with commercial style portafilter",
        "price": 8750000.0,
        "currency": Currency.IDR,
        "stock": 6,
        "categories": ["Espresso Machine"],
    },
    {
        "sku": 1003,
        "name": "Baratza Encore ESP",
        "description": "Burr grinder tuned for both espresso and filter coffee",
        "price": 3250000.0,
        "currency": Currency.IDR,
        "stock": 14,
        "categories": ["Grinder"],
    },
    {
        "sku": 1004,
        "name": "1Zpresso JX-Pro",
        "description": "Premium manual grinder with precise external adjustment",
        "price": 2650000.0,
        "currency": Currency.IDR,
        "stock": 18,
        "categories": ["Grinder"],
    },
    {
        "sku": 1005,
        "name": "Hario V60 Plastic Dripper 02",
        "description": "Iconic cone dripper for manual pour-over brewing",
        "price": 125000.0,
        "currency": Currency.IDR,
        "stock": 42,
        "categories": ["Dripper"],
    },
    {
        "sku": 1006,
        "name": "Kalita Wave 185 Stainless",
        "description": "Flat-bottom dripper designed for even extraction",
        "price": 620000.0,
        "currency": Currency.IDR,
        "stock": 16,
        "categories": ["Dripper"],
    },
    {
        "sku": 1007,
        "name": "Onyx Geometry Beans 10oz",
        "description": "Popular blend with notes of berries and milk chocolate",
        "price": 320000.0,
        "currency": Currency.IDR,
        "stock": 30,
        "categories": ["Beans"],
    },
    {
        "sku": 1008,
        "name": "Stumptown Hair Bender Beans 12oz",
        "description": "Classic espresso blend with chocolate and citrus profile",
        "price": 285000.0,
        "currency": Currency.IDR,
        "stock": 22,
        "categories": ["Beans"],
    },
    {
        "sku": 1009,
        "name": "Loveramics Egg Cappuccino Cup 200ml",
        "description": "Competition style porcelain cup for cappuccino",
        "price": 215000.0,
        "currency": Currency.IDR,
        "stock": 26,
        "categories": ["Cup"],
    },
    {
        "sku": 1010,
        "name": "ACME Evolution Latte Cup 280ml",
        "description": "Cafe-grade latte cup used by specialty coffee shops",
        "price": 235000.0,
        "currency": Currency.IDR,
        "stock": 27,
        "categories": ["Cup"],
    },
]


def seed_categories(session: Session) -> dict[str, Category]:
    categories_by_name: dict[str, Category] = {}

    for data in CATEGORY_SEEDS:
        existing = session.exec(select(Category).where(Category.name == data["name"])).first()
        if existing:
            existing.description = data["description"]
            categories_by_name[data["name"]] = existing
            continue

        category = Category(**data)
        session.add(category)
        session.flush()
        categories_by_name[data["name"]] = category

    return categories_by_name


def seed_products(session: Session, categories_by_name: dict[str, Category]) -> None:
    for data in PRODUCT_SEEDS:
        category_names = data["categories"]
        category_objects = [categories_by_name[name] for name in category_names]

        product_payload = {
            "sku": data["sku"],
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "currency": data["currency"],
            "stock": data["stock"],
        }

        existing = session.exec(select(Product).where(Product.sku == data["sku"])).first()
        if existing:
            existing.name = product_payload["name"]
            existing.description = product_payload["description"]
            existing.price = product_payload["price"]
            existing.currency = product_payload["currency"]
            existing.stock = product_payload["stock"]
            existing.categories = category_objects
            continue

        product = Product(**product_payload, categories=category_objects)
        session.add(product)


def seed() -> None:
    with Session(engine) as session:
        categories_by_name = seed_categories(session)
        seed_products(session, categories_by_name)
        session.commit()

    print("Seeding completed: categories and products are ready.")


if __name__ == "__main__":
    seed()
