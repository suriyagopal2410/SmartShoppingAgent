from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ShoppingIntent:
    raw_query: str
    category: Optional[str] = None
    product_query: Optional[str] = None
    budget: Optional[float] = None
    currency: str = "INR"
    min_rating: Optional[float] = None
    preferences: List[str] = field(default_factory=list)
    required_features: List[str] = field(default_factory=list)

@dataclass
class Product:
    title: str
    price: Optional[float] = None
    currency: str = "INR"
    source: str = ""
    product_link: str = ""
    thumbnail: str = ""
    rating: Optional[float] = None
    reviews: Optional[int] = None
    description: str = ""
    features: List[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)
    relevance: float = 0.0
    feature_match: float = 0.0
    price_value: float = 0.0
    rating_score: float = 0.0
    review_score: float = 0.0
    final_score: float = 0.0
