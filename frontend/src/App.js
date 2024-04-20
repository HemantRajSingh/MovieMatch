import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Trending from './pages/Trending';
import Browse from './pages/Browse';

const App = () => {
  return (
    <Routes>
      <Route path="/" exact element={<Home />} />
      <Route path="/trending" exact element={<Trending />} />
      <Route path="/browse" exact element={<Browse />} />
    </Routes>
  );
};

export default App;
