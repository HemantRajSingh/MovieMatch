import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';
import { useQuery } from 'react-query';
import { getTrending } from '../services/api';

const Trending = () => {
  const { data } = useQuery('trending', getTrending);
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        <MovieList
          title="Trending"
          subtitle="Trending Movies"
          movieList={data ? data : []}
        />
      </div>
    </>
  );
};

export default Trending;
