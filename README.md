# Movie Recommendation System

This is a **Content-Based Movie Recommendation System** built using a dataset of movies along with their metadata such as titles, overviews, genres, and credits. The system uses **TF-IDF vectorization** and a **sigmoid kernel** to recommend movies similar to the one selected by the user. Additionally, users can refine recommendations using **genre** and **vote rating filters**.

##  Features

-  Recommends similar movies based on a selected movie title
-  Uses **TF-IDF vectorizer** + **sigmoid kernel** for measuring content similarity
-  **Genre filtering** to tailor results to a specific genre
-  **Vote rating filter** to limit results to higher-rated movies
-  Interactive web interface using **Streamlit**

##  Dataset

The dataset includes:
- `movies.csv` – movie titles, overviews, genres, vote averages
- `credits.csv` – information about cast and crew

These files are merged and preprocessed to extract relevant metadata for recommendation.

##  Tech Stack

- Python
- Pandas & NumPy
- Scikit-learn (TF-IDF, sigmoid kernel)
- Streamlit (for UI)

##  Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system


# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
