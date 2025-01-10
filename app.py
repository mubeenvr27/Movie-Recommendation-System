import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7bc3406242999e0983d713728735cafd& language=en-US'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']


def recomend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    # Get the similarity distances for the movie
    distances = similarity[movie_index]

    # Pair each movie index with its similarity score and sort them
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    # Print the titles of the recommended movies
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommendation System')
select_movie_name = st.selectbox(
    "Hey there! You want to watch a movie like this?",
    movies['title'].values
)


if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recomend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])