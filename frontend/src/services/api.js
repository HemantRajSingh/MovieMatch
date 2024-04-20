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
    console.log(typeof response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};
