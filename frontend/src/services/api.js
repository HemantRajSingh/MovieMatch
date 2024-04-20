import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/',
});

export const recommendtaions = async ({ request }) => {
  try {
    const response = await API.post(`/recommendations`, {
      query: request,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};
