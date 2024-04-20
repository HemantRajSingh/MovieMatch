import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';

const Trending = () => {
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        (
        <MovieList title="Trending" subtitle="Trending Movies" movieList={[]} />
        )
      </div>
    </>
  );
};

export default Trending;
