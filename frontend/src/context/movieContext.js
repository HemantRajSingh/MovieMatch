import { getRecommendations } from '../services/api';
import { useQuery, useMutation } from 'react-query';
const { createContext, useState, useContext } = require('react');

const MovieContext = createContext();

export const MovieProvider = ({ children }) => {
  const [recommendations, setRecommendations] = useState([]);

  const { mutate: fetchRecommendations } = useMutation(getRecommendations, {
    onSuccess: (res) => console.log('context', res),
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
