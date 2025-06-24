import streamlit as st
import pickle
import pandas as pd
import requests


# Function to set background image
def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://raw.githubusercontent.com/Shaishta-Anjum/Movie-Recommender-System/main/Image%20File/bg8.png");
             background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


# Set background image
set_bg_hack_url()

# Load the movie dataset
movies_df = pd.read_pickle('movies.pkl')


# Function to fetch movie poster using The Movie Database (TMDb) API
def fetch_poster(movie_id):
    api_key = "4777e4b7e8f357ce848eb6b294ffccab"  # Replace with your API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-us'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")


# Function to recommend similar movies
def recommend(movie):
    try:
        movie_index = movies_df.loc[movies_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies_df.iloc[i[0]].movie_id
            recommended_movies.append(movies_df.iloc[i[0]]['title'])  # Append movie title
            recommended_movies_posters.append(fetch_poster(movie_id))  # Fetch movie poster

        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the dataset. Please try another movie.")
        return [], []


# Load movie titles for selection
movies_list = pickle.load(open('movies.pkl', 'rb'))['title'].values

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title
st.title('🎬 Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox('🔍 Select a Movie to Get Recommendations', movies_list)

# Recommend movies when button is clicked
if st.button('🎥 Recommend Movies'):
    names, posters = recommend(selected_movie_name)

    if names:
        st.subheader("You may also like:")
        cols = st.columns(5)  # Create 5 columns for displaying movies

        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])  # Display movie title
                st.image(posters[idx])  # Display poster

#streamlit run app.py