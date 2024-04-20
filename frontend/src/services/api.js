import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:5000',
});

export const getRecommendations = async ({ request }) => {
  try {
    const response = await API.post(`/recommendations/`, {
      query: request,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};
