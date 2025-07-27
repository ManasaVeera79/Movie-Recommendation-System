import streamlit as st
import pandas as pd
import pickle
import ast

# Load data and similarity matrix
movies_cleaned_df = pd.read_csv('movies_cleaned.csv')
with open('similarity1.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Preprocess: Clean titles
movies_cleaned_df['original_title'] = movies_cleaned_df['original_title'].str.lower().str.strip()

# Extract genre names from JSON-like strings
def extract_genre_names(genre_str):
    try:
        genre_list = ast.literal_eval(genre_str)
        return [g['name'] for g in genre_list]
    except:
        return []

movies_cleaned_df['genre_names'] = movies_cleaned_df['genres'].apply(extract_genre_names)

# Mapping of movie title to index
indices = pd.Series(movies_cleaned_df.index, index=movies_cleaned_df['original_title'])

# 🎯 Recommendation function
def recommend(title, filtered_df=None):
    title = title.lower().strip()
    if title not in indices:
        return None
    
    idx = indices[title]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in scores[1:]]  # Skip itself

    recommended_titles = []
    for i in top_indices:
        movie = movies_cleaned_df.iloc[i]
        if filtered_df is not None and movie['original_title'] not in filtered_df['original_title'].values:
            continue
        recommended_titles.append(movie['original_title'].title())
        if len(recommended_titles) == 10:
            break

    return recommended_titles

# 🌟 Streamlit UI
st.title(" Movie Recommendation App")

# 📌 Sidebar filters
st.sidebar.markdown(" **Additional Filters**")

# Genre Filter
all_genres = sorted(set(genre for sublist in movies_cleaned_df['genre_names'] for genre in sublist))
selected_genres = st.sidebar.multiselect(" Filter by Genre", all_genres)

# Vote Count & Rating Range Filters
min_votes = int(movies_cleaned_df['vote_count'].min())
max_votes = int(movies_cleaned_df['vote_count'].max())
min_rating = float(movies_cleaned_df['vote_average'].min())
max_rating = float(movies_cleaned_df['vote_average'].max())

vote_count_range = st.sidebar.slider("Minimum Vote Count", min_value=min_votes, max_value=max_votes, value=(500, 10000))
rating_range = st.sidebar.slider("Rating Range", min_value=min_rating, max_value=max_rating, value=(6.0, 9.0))

# 🎛️ Filter DataFrame
filtered_movies = movies_cleaned_df[
    (movies_cleaned_df['vote_count'] >= vote_count_range[0]) &
    (movies_cleaned_df['vote_count'] <= vote_count_range[1]) &
    (movies_cleaned_df['vote_average'] >= rating_range[0]) &
    (movies_cleaned_df['vote_average'] <= rating_range[1])
]

# Apply genre filter
if selected_genres:
    filtered_movies = filtered_movies[filtered_movies['genre_names'].apply(lambda x: any(g in x for g in selected_genres))]

# 🔍 Movie Input
movie_name = st.text_input("Enter a movie name:")

# 🔁 Get Recommendations
if st.button("Get Recommendations"):
    if movie_name:
        recommendations = recommend(movie_name, filtered_df=filtered_movies)
        if recommendations:
            st.subheader(" Top 10 Similar Movies:")
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.error(" Movie not found or doesn't match selected filters.")
    else:
        st.warning(" Please enter a movie title.")

# 🎯 Show Top Movies Based on Filters
st.subheader(" Top Recommended Movies (Filtered):")

# Sort by weighted score if exists, else by rating
if 'score' in movies_cleaned_df.columns:
    top_movies = filtered_movies.sort_values("score", ascending=False).head(10)
else:
    top_movies = filtered_movies.sort_values("vote_average", ascending=False).head(10)

for _, row in top_movies.iterrows():
    st.write(f"🎬 {row['original_title'].title()} — ⭐ {row['vote_average']} (Votes: {row['vote_count']})")
