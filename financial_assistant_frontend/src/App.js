import {
  BrowserRouter as Router,  
  Routes,
  Route
} from 'react-router-dom'

import './App.css';
import Header from './components/Header'
import NewsListPage from './pages/NewsListPage'
import NewsPage from './pages/NewsPage'

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path='/' element={<NewsListPage />} />
          <Route path='/news/:id' element={<NewsPage />} />
        </Routes>
        
      </div>
    </Router>
  );
}

export default App;
