import React, { useState } from 'react';
import Header from './components/Header';

const dummyMovies = [
  {
    title: 'Iron Man',
    genre: 'Action / Adventure / Sci-Fi',
    cover:
      'https://img.yts.mx/assets/images/movies/Iron_Man_2008/medium-cover.jpg',
  },
  {
    title: 'Iron Man 2',
    genre: 'Action / Adventure / Sci-Fi',
    cover:
      'https://img.yts.mx/assets/images/movies/Iron_Man_2_2010/medium-cover.jpg',
  },
  {
    title: 'Iron Man 3',
    genre: 'Action / Adventure / Sci-Fi',
    cover:
      'https://img.yts.mx/assets/images/movies/Iron_Man_3_2013/medium-cover.jpg',
  },
  {
    title: 'The Avengers',
    genre: 'Action / Adventure / Sci-Fi / Thriller',
    cover:
      'https://img.yts.mx/assets/images/movies/The_Avengers_2012/medium-cover.jpg',
  },
  {
    title: 'Captain America: The First Avenger',
    genre: 'Action / Adventure / Sci-Fi',
    cover:
      'https://img.yts.mx/assets/images/movies/Captain_America_The_First_Avenger_2011/medium-cover.jpg',
  },
];

const MovieRecommendations = () => {
  const [query, setQuery] = useState('');

  return (
    <div>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        <div className="items-center justify-between w-full mx-auto">
          <div className="space-y-1">
            <h2 className="text-2xl font-semibold tracking-tight">Trending</h2>
            <p className="text-sm text-muted-foreground">
              Top trends for you. Updated daily.
            </p>
          </div>
          <div
            data-orientation="horizontal"
            role="none"
            className="shrink-0 bg-border h-[1px] w-full my-4"
          ></div>
        </div>
      </div>

      <div className="overflow-x-scroll w-3/4 flex mx-auto">
        {dummyMovies.map((movie) => (
          <div className="h-full w-full rounded-[inherit]">
            <div className="flex space-x-4 pb-4">
              <div className="space-y-3 w-[250px]">
                <span data-state="closed">
                  <div className="overflow-hidden rounded-md">
                    <img
                      alt="React Rendezvous"
                      loading="lazy"
                      width="250"
                      height="330"
                      decoding="async"
                      data-nimg="1"
                      className="h-auto w-auto object-cover transition-all hover:scale-105 aspect-[3/4]"
                      srcset={movie.cover}
                      src={movie.cover}
                      // style="color: transparent;"
                    />
                  </div>
                </span>
                <div className="space-y-1 text-sm">
                  <h3 className="font-medium leading-none">{movie.title}</h3>
                  <p className="text-xs text-muted-foreground">{movie.genre}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MovieRecommendations;
