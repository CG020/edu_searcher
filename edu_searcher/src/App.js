import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import axios from 'axios';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const searchResources = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/search', { params: { query } });
            setResults(response.data);
        } catch (error) {
            console.error('Error fetching resources:', error);
        }
    };

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
            <ul className="results-list">
                {results.map((result, index) => (
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
            
            <br></br><br></br><br></br>
            <p className='section-label'>library</p>
        </div>
    );
}

export default App;