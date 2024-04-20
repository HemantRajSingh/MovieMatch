import React, { useState } from 'react';
import { Search } from './Search';

const Header = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  
  return (
    <div>
      <header class="bg-white">
        <nav
          class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8"
          aria-label="Global"
        >
          <div class="flex lg:flex-1">
            <a href="#" class="-m-1.5 p-1.5">
              <span class="sr-only">Movie Match</span>
              <h2 class="h-8 w-auto text-3xl font-bold">
                Moive<span className="text-red-600">Match</span>
              </h2>
            </a>
          </div>
          <div class="hidden lg:flex lg:gap-x-12">
            <a href="#" class="text-sm font-semibold leading-6 text-gray-900">
              Browse
            </a>
            <a href="#" class="text-sm font-semibold leading-6 text-gray-900">
              New
            </a>
            <a href="#" class="text-sm font-semibold leading-6 text-gray-900">
              Popular
            </a>
          </div>
          <div
            class="hidden lg:flex lg:flex-1 lg:justify-end"
            onClick={() => setIsDialogOpen(true)}
          >
            <Search dialogState={isDialogOpen} />
          </div>
        </nav>
      </header>
    </div>
  );
};

export default Header;
