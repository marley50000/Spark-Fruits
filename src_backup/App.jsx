import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Admin from './pages/Admin';
import Track from './pages/Track';
import Menu from './pages/Menu';
import Subscribe from './pages/Subscribe';
import './index.css';

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/menu" element={<Menu />} />
                <Route path="/subscribe" element={<Subscribe />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/track" element={<Track />} />
            </Routes>
        </Router>
    );
}

export default App;
