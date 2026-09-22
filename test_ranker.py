from app.models import Product, ShoppingIntent
from app.services.ranker import rank_products

def test_ranker_returns_sorted():
    ps=[Product("A laptop",price=50000,rating=4.5,reviews=1000),
        Product("B laptop",price=70000,rating=4.0,reviews=100)]
    i=ShoppingIntent("laptop under 80000",category="laptop",product_query="laptop",budget=80000)
    r=rank_products(ps,i,{"x":0})
    assert len(r)==2
    assert r[0].final_score >= r[1].final_score
