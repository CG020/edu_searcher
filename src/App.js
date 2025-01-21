import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Account from './components/Account/Account';
import Home from './components/Home/Home';

function App() {
    const [activeTab, setActiveTab] = useState('home');

    return (
        <Router>
            <div className="navigation">
                <NavLink
                    to="/"
                    className={activeTab === 'home' ? 'active' : ''}
                    onClick={() => setActiveTab('home')}>
                    Guest
                </NavLink>
                <NavLink
                    to="/account"
                    className={activeTab === 'account' ? 'active' : ''}
                    onClick={() => setActiveTab('account')}>
                    Account
                </NavLink>
                <div className={`underline ${activeTab}`}></div>
            </div>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/account" element={<Account />} />
            </Routes>
        </Router>
    );
}

export default App;