import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar/Navbar';
import axios from 'axios';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [visibleResults, setVisibleResults] = useState([]);
    const [activeFilters, setActiveFilters] = useState([]);
    const [page, setPage] = useState(1);
    const resultsPerPage = 5;

    const searchResources = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/search', { params: { query } });
            setResults(response.data);
            setPage(1);
            setActiveFilters([]);
        } catch (error) {
            console.error('Error fetching resources:', error);
        }
    };

    useEffect(() => {
        const filteredResults = activeFilters.length > 0
            ? results.filter(result => activeFilters.includes(result.source))
            : results;
        setVisibleResults(filteredResults.slice(0, page * resultsPerPage));
    }, [results, page, activeFilters]);

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

    const handleSeeMore = () => {
        setPage(prevPage => prevPage + 1);
    };

    const toggleFilter = (source) => {
        setActiveFilters(prevFilters =>
            prevFilters.includes(source)
                ? prevFilters.filter(f => f !== source)
                : [...prevFilters, source]
        );
        setPage(1);
    };

    const sources = [...new Set(results.map(result => result.source))];

    return (
        <div>
            <div className='header-section'>
                <Navbar message='edu space' tabs={['search','library','history','options']}/>
            </div>

            <p className='section-label'>search</p>
            
            <input
                type="text"
                placeholder="Search for tutorials..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button className="search-button" onClick={searchResources}>Search</button>

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

            <ul className="results-list">
                {visibleResults.map((result, index) => (
                    <li key={index} className="result-item">
                        <div className="source-label">
                            <span>{getSourceIcon(result.source)}</span>
                            <span>{result.source}</span>
                        </div>
                        <h3>{result.title}</h3>
                        <a href={result.link}>Learn more</a>
                    </li>
                ))}
            </ul>

            {visibleResults.length < (activeFilters.length > 0 ? results.filter(result => activeFilters.includes(result.source)).length : results.length) && (
                <button className="see-more-button" onClick={handleSeeMore}>See More</button>
            )}
            
            <br></br><br></br><br></br>
            <p className='section-label'>library</p>
        </div>
    );
}

export default App;