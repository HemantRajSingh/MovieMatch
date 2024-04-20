import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Trending from './pages/Trending';
import Browse from './pages/Browse';
import New from './pages/New';
import Popular from './pages/Popular';
import TopRated from './pages/TopRated';

const App = () => {
  return (
    <Routes>
      <Route path="/" exact element={<Home />} />
      <Route path="/trending" exact element={<Trending />} />
      <Route path="/browse" exact element={<Browse />} />
      <Route path="/new" exact element={<New />} />
      <Route path="/popular" exact element={<Popular />} />
      <Route path="/top-rated" exact element={<TopRated />} />
    </Routes>
  );
};

export default App;
