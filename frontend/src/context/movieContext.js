import { useMutation } from 'react-query';
import { getRecommendations } from '../services/api';
const { createContext, useState, useContext } = require('react');

const MovieContext = createContext();

export const MovieProvider = ({ children }) => {
  const [recommendations, setRecommendations] = useState([]);

  const { mutate: fetchRecommendations } = useMutation(getRecommendations, {
    onSuccess: (res) => {
      setRecommendations(res);
    },
    onError: (error) => {
      console.error('Error fetching recommendations:', error);
    },
  });

  return (
    <MovieContext.Provider
      value={{
        recommendations,
        fetchRecommendations,
      }}
    >
      {children}
    </MovieContext.Provider>
  );
};

export const useMovieContext = () => useContext(MovieContext);
