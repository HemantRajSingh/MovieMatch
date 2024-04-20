import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';

const New = () => {
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        (
        <MovieList title="New" subtitle="New Movies" movieList={[]} />)
      </div>
    </>
  );
};

export default New;
