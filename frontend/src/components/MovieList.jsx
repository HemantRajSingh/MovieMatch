import React from 'react';

const MovieList = ({ title, subtitle, movieList }) => {
  const generateGenre = (genre) => {
    const validGenre = genre.replace(/'/g, '"');
    return JSON.parse(validGenre);
  };

  return (
    <div className="flex max-w-7xl p-6 mx-auto mt-3">
      <div className="flex w-full mx-auto mt-3">
        <div className="items-center justify-between w-full mx-auto">
          <div className="space-y-1">
            <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
            <p className="text-sm text-muted-foreground">{subtitle}</p>
          </div>
          <div
            data-orientation="horizontal"
            role="none"
            className="shrink-0 w-full my-4"
          >
            <div className="overflow-x-scroll w-full flex mx-auto gap-8">
              {movieList?.map((movie) => (
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
                            srcset={movie.image_link}
                            src={movie.image_link}
                          />
                        </div>
                      </span>
                      <div className="space-y-1 text-sm">
                        <h3 className="font-medium leading-none">
                          {movie.title}
                        </h3>
                        <p className="text-xs text-muted-foreground">
                          {movie?.genre
                            ? generateGenre(movie.genre)?.join(', ')
                            : ''}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieList;
