from app.services.text_utils import extract_budget, infer_category

def test_budget():
    assert extract_budget("laptop under ₹80,000") == 80000

def test_budget_lakh():
    assert extract_budget("TV up to 1.2 lakh") == 120000

def test_category():
    assert infer_category("noise cancelling headphones") == "headphones"
