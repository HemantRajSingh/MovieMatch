import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';
import { useQuery } from 'react-query';
import { getLatestMovies } from '../services/api';

const New = () => {
  const { data } = useQuery('latest', getLatestMovies);
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        <MovieList
          title="New"
          subtitle="New Movies"
          movieList={data ? data : []}
        />
      </div>
    </>
  );
};

export default New;
