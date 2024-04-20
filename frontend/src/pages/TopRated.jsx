import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';
import { useQuery } from 'react-query';
import { getTopRatedMovies } from '../services/api';

const TopRated = () => {
  const { data } = useQuery('trending', getTopRatedMovies);
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        <MovieList
          title="Top Rated"
          subtitle="Top Rated Movies"
          movieList={data ? data : []}
        />
      </div>
    </>
  );
};

export default TopRated;
