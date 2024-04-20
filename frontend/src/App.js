import Header from './components/Header';
import { useMovieContext } from './context/movieContext';

const MovieRecommendations = () => {
  const { recommendations } = useMovieContext();

  const generateGenre = (genre) => {
    const validGenre = genre.replace(/'/g, '"');
    return JSON.parse(validGenre);
  };

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

      <div className="overflow-x-scroll w-3/4 flex mx-auto gap-8">
        {recommendations?.map((movie) => (
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
                  <h3 className="font-medium leading-none">{movie.title}</h3>
                  <p className="text-xs text-muted-foreground">
                    {movie?.genre ? generateGenre(movie.genre)?.join(', ') : ''}
                  </p>
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
