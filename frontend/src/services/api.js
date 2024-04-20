import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getRecommendations = async ({ query }) => {
  try {
    const response = await API.post(`/recommendations/`, {
      query: query,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

export const getTrending = async () => {
  try {
    const response = await API.get(`/trending_movies/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

export const getPopularMovies = async () => {
  try {
    const response = await API.get(`/popular_movies/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

export const getLatestMovies = async () => {
  try {
    const response = await API.get(`/latest_movies/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

export const getTopRatedMovies = async () => {
  try {
    const response = await API.get(`/top_rated_movies/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

export const browseMovies = async () => {
  try {
    const response = await API.get(`/browse/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};
