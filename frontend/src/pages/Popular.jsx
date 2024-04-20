import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';
const Popular = () => {
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        (
        <MovieList title="Popular" subtitle="Popular Movies" movieList={[]} />)
      </div>
    </>
  );
};

export default Popular;
