import streamlit as st
import pickle
import numpy as np

# ---------------- Load Data ----------------
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
score = pickle.load(open('score.pkl', 'rb'))
book = pickle.load(open('books.pkl', 'rb'))

# ---------------- Helper Functions ----------------
def recommend(book_name):
    if book_name not in pt.index:
        st.warning(f"Book '{book_name}' not found in pivot table.")
        return []

    index = np.where(pt.index == book_name)[0][0]
    score_items = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:6]

    suggestions = []
    for i in score_items:
        b = book[book['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        if not b.empty:
            suggestions.append({
                "title": b['Book-Title'].values[0],
                "author": b['Book-Author'].values[0],
                "image": b['Image-URL-M'].values[0] if 'Image-URL-M' in b.columns else None
            })
    return suggestions

def show_book(image_url, title, author):
    if image_url and str(image_url).startswith("http"):
        st.image(image_url, width=120)
    else:
        st.image("https://via.placeholder.com/120x180.png?text=No+Image", width=120)
    st.caption(f"**{title}**\nby {author}")

# ---------------- Streamlit UI ----------------
st.title("📚 Book Recommender System")

tab1, tab2 = st.tabs(["🔥 Popular Books", "🤝 Collaborative Filtering"])

with tab1:
    st.subheader("Top 50 Popular Books")

    # Display Popular Books in rows of 5
    for i in range(0, len(popular_df), 5):
        cols = st.columns(5)
        for j, (_, row) in enumerate(popular_df.iloc[i:i+5].iterrows()):
            with cols[j % 5]:
                show_book(row.get('Image-URL-M'), row['Book-Title'], row['Book-Author'])

with tab2:
    selected_book = st.selectbox("Choose a book you like:", pt.index)
    if st.button("Show Recommendations"):
        recommendations = recommend(selected_book)
        if recommendations:
            # Display Recommendations in rows of 5
            for i in range(0, len(recommendations), 5):
                cols = st.columns(5)
                for j, rec in enumerate(recommendations[i:i+5]):
                    with cols[j % 5]:
                        show_book(rec["image"], rec["title"], rec["author"])
        else:
            st.info("No recommendations found for this book.")
