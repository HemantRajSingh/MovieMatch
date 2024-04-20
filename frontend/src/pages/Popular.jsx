import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';
import { useQuery } from 'react-query';
import { getPopularMovies } from '../services/api';

const Popular = () => {
  const { data } = useQuery('latest', getPopularMovies);
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        <MovieList
          title="Popular"
          subtitle="Popular Movies"
          movieList={data ? data : []}
        />
      </div>
    </>
  );
};

export default Popular;
