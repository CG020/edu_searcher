import './App.css';
import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar';


function App() {
    const [query, setQuery] = useState('');
    const [sourceType, setSourceType] = useState('');
    const [level, setLevel] = useState('');
    const [results, setResults] = useState([]);

    const fetchResources = async () => {
        const response = await fetch(`/api/fetch_resources?query=${query}&sourceType=${sourceType}&level=${level}`);
        const data = await response.json();
        setResults(data);
    };

    return (
        <div>
          <div className='header-section'>
            <Navbar message='learn space' tabs={['profile','bio','projects','gallery']}/>
            </div>
            
            <input type="text" placeholder="I want to learn about..." value={query} onChange={e => setQuery(e.target.value)} />
            <input type="text" placeholder="Source Type" value={sourceType} onChange={e => setSourceType(e.target.value)} />
            <input type="text" placeholder="Level" value={level} onChange={e => setLevel(e.target.value)} />
            <button onClick={fetchResources}>Search</button>
            <ul>
                {results.map((result, index) => (
                    <li key={index}>
                        <h3>{result.title}</h3>
                        <a href={result.link}>Learn more</a>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
