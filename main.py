import streamlit as st
from app.config import settings
from app.models import ShoppingIntent
from app.services.intent import extract_intent
from app.services.search_provider import SerpApiShoppingProvider
from app.services.recommender import Recommender
from app.services.database import init_db, save_search
from app.ui.components import render_product_card

st.set_page_config(page_title="Smart Shopping Agent",page_icon="🛒",layout="wide")
init_db()

st.title("🛒 Smart Shopping Agent")
st.caption("Live product search + personalized comparison + AI explanation")

with st.sidebar:
    st.header("Filters")
    budget_override=st.number_input("Maximum budget (optional)",min_value=0.0,value=0.0,step=1000.0)
    min_rating=st.slider("Minimum rating",0.0,5.0,0.0,0.5)
    result_count=st.slider("Products to retrieve",5,30,15)
    top_n=st.slider("Recommendations to show",3,10,5)
    st.info("Live data is fetched through SerpApi Google Shopping. Prices and availability can change.")

query=st.text_input("What are you looking for?",placeholder="Example: laptop under ₹80,000 for Power BI, Python and office work")
search=st.button("🔎 Search live products",type="primary")

if search:
    if not query.strip():
        st.error("Please enter a product or search term.")
        st.stop()
    try:
        with st.spinner("Understanding your requirements..."):
            intent=extract_intent(query)
        if budget_override>0: intent.budget=budget_override
        if min_rating>0: intent.min_rating=min_rating

        st.subheader("Detected requirements")
        st.json({"category":intent.category,"budget":intent.budget,"currency":intent.currency,
                 "preferences":intent.preferences,"required_features":intent.required_features})

        with st.spinner("Fetching live shopping results..."):
            products=SerpApiShoppingProvider().search(intent.product_query or query,result_count)

        if not products:
            st.warning("No products found. Try a broader product description or a different budget.")
            save_search(query,intent,0)
            st.stop()

        recommendations=Recommender().recommend(products,intent,top_n)
        save_search(query,intent,len(products))

        if not recommendations:
            st.warning("No products matched the selected budget/rating filters. Try relaxing a filter.")
            st.stop()

        st.success(f"Found {len(products)} live results; showing {len(recommendations)} recommendations.")
        st.subheader("Recommended products")
        for p in recommendations:
            render_product_card(p,intent)

        st.subheader("Comparison")
        rows=[]
        for p in recommendations:
            rows.append({"Product":p.title,"Source":p.source,"Price":p.price,"Rating":p.rating,
                         "Reviews":p.reviews,"Score":round(p.final_score,3)})
        st.dataframe(rows,use_container_width=True,hide_index=True)

    except Exception as e:
        st.error(str(e))
        st.info("Check your SERPAPI_API_KEY and internet connection. If Ollama is unavailable, the app can still run using its fallback intent/explanation logic.")
else:
    st.markdown("""
### Try these examples
- **Laptop:** Find a laptop under ₹80,000 for Power BI and Python
- **Headphones:** Noise cancelling headphones under ₹20,000 for travel
- **Shoes:** Running shoes under ₹8,000 for daily road running
- **TV:** 55 inch 4K TV under ₹60,000 with good reviews

The workflow follows the supplied project presentation: user query → intent extraction → product search → evaluation → ranking → recommendation → comparison.
""")
