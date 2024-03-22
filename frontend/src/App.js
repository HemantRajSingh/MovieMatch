import React, { useState } from 'react';
import axios from 'axios';

const MovieRecommendations = () => {
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get(`http://127.0.0.1:5000//recommendations/${query}`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <div>
      <h2>Get Movie Recommendations</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" value={query} onChange={handleChange} />
        <button type="submit">Get Recommendations</button>
      </form>
      <ul>
      {Array.isArray(recommendations) && recommendations.length > 0 ? (
    recommendations.map((movie) => (
        <li key={movie.id}>
            <h3>{movie['Movie Title']}</h3>
            <img src={movie['Cover Image']} alt={movie['Movie Title']} />
            <p>Genre: {movie.Genre}</p>
            <p>Year: {movie.Year}</p>
        </li>
    ))
) : (
    <li>No recommendations found</li>
)}
      </ul>
    </div>
  );
};

export default MovieRecommendations;
