import { Link } from 'react-router-dom';
import { Search } from './Search';

const Header = () => {
  return (
    <div>
      <header class="bg-white">
        <nav
          class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8"
          aria-label="Global"
        >
          <div class="flex lg:flex-1">
            <Link to="/" class="-m-1.5 p-1.5">
              <span class="sr-only">Movie Match</span>
              <h2 class="h-8 w-auto text-3xl font-bold">
                Moive<span className="text-red-600">Match</span>
              </h2>
            </Link>
          </div>
          <div class="hidden lg:flex lg:gap-x-12">
            <Link
              to="/new"
              class="text-sm font-semibold leading-6 text-gray-900"
            >
              New
            </Link>
            <Link
              to="/trending"
              class="text-sm font-semibold leading-6 text-gray-900"
            >
              Trending
            </Link>
            <Link
              to="/popular"
              class="text-sm font-semibold leading-6 text-gray-900"
            >
              Popular
            </Link>
            <Link
              to="/top-rated"
              class="text-sm font-semibold leading-6 text-gray-900"
            >
              Top Rated
            </Link>
            <Link
              to="/browse"
              class="text-sm font-semibold leading-6 text-gray-900"
            >
              Browse
            </Link>
          </div>
          <div class="hidden lg:flex lg:flex-1 lg:justify-end">
            <Search />
          </div>
        </nav>
      </header>
    </div>
  );
};

export default Header;
