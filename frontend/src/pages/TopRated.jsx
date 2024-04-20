import MovieList from '../components/MovieList';
import Header from '../components/Header';
import React from 'react';

const TopRated = () => {
  return (
    <>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        (
        <MovieList
          title="Top Rated"
          subtitle="Top Rated Movies"
          movieList={[]}
        />
        )
      </div>
    </>
  );
};

export default TopRated;
