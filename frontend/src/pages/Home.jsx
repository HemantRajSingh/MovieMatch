import Header from '../components/Header';
import MovieList from '../components/MovieList';
import { useMovieContext } from '../context/movieContext';

const Home = () => {
  const { recommendations } = useMovieContext();

  return (
    <div>
      <Header />
      <div className="flex w-3/4 mx-auto mt-3">
        {recommendations?.length ? (
          <MovieList
            title="Search Results"
            subtitle="Movies based on the provided summary"
            movieList={recommendations}
          />
        ) : (
          <MovieList
            title="Trending"
            subtitle=" Top trends for you. Updated daily."
            movieList={[]}
          />
        )}
      </div>
    </div>
  );
};

export default Home;
