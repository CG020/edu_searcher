import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar/Navbar';
import axios from 'axios';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [activeFilters, setActiveFilters] = useState([]);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);

    const searchResources = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/search', { 
                params: { query, page } 
            });
            if (page === 1) {
                setResults(response.data.results || []);
            } else {
                setResults(prevResults => [...prevResults, ...(response.data.results || [])]);
            }
            setHasMore(response.data.has_more);
            setHasSearched(true);
        } catch (error) {
            console.error('Error fetching resources:', error);
            setResults([]);
            setHasMore(false);
        }
    };

    useEffect(() => {
        if (query && hasSearched) {
            searchResources();
        }
    }, [query, page, hasSearched]);

    const handleSearch = () => {
        setPage(1);
        setHasSearched(true);
        searchResources();
    };

    const handleSeeMore = () => {
        setPage(prevPage => prevPage + 1);
    };

    const handleClear = () => {
        setQuery('');
        setResults([]);
        setActiveFilters([]);
        setPage(1);
        setHasMore(false);
        setHasSearched(false);
    };

    const toggleFilter = (source) => {
        setActiveFilters(prevFilters =>
            prevFilters.includes(source)
                ? prevFilters.filter(f => f !== source)
                : [...prevFilters, source]
        );
        setPage(1);
    };

    const filteredResults = activeFilters.length > 0
        ? results.filter(result => activeFilters.includes(result.source))
        : results;

    const getSourceIcon = (source) => {
        switch(source) {
            case 'YouTube':
                return '▶️';
            case 'Khan Academy':
                return '🎓';
            default:
                return '📚';
        }
    };

    const sources = [...new Set(results.map(result => result.source))];

    return (
      <div>
          <div className='header-section'>
              <Navbar message='edu space' tabs={['search','library','history','options']}/>
          </div>

          <div className="container">
              <p className='section-label'>search</p>
              
              <div className="search-container">
                  <input
                      type="text"
                      placeholder="Search for tutorials..."
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                  />
                  <button className="search-button" onClick={handleSearch}>Search</button>
                  <button className="clear-button" onClick={handleClear}>Clear</button>
              </div>

              {hasSearched && (
                  <div className="filter-buttons">
                      {sources.map(source => (
                          <button
                              key={source}
                              onClick={() => toggleFilter(source)}
                              className={`filter-button ${activeFilters.includes(source) ? 'active' : ''}`}
                          >
                              {getSourceIcon(source)} {source}
                          </button>
                      ))}
                  </div>
              )}

              <div className="results-container">
                  <div className="results-column">
                      {filteredResults.filter((_, index) => index % 2 === 0).map((result, index) => (
                          <div key={index * 2} className="result-item">
                              <div className="source-label">
                                  <span>{getSourceIcon(result.source)}</span>
                                  <span>{result.source}</span>
                              </div>
                              <h3>{result.title}</h3>
                              <a href={result.link}>Learn more</a>
                          </div>
                      ))}
                  </div>
                  <div className="results-column">
                      {filteredResults.filter((_, index) => index % 2 !== 0).map((result, index) => (
                          <div key={index * 2 + 1} className="result-item">
                              <div className="source-label">
                                  <span>{getSourceIcon(result.source)}</span>
                                  <span>{result.source}</span>
                              </div>
                              <h3>{result.title}</h3>
                              <a href={result.link}>Learn more</a>
                          </div>
                      ))}
                  </div>
              </div>

              {hasSearched && hasMore && (
                  <button className="see-more-button" onClick={handleSeeMore}>See More</button>
              )}
              
              <br></br><br></br><br></br>
              <p className='section-label'>library</p>
          </div>
      </div>
  );
}

export default App;