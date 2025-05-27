import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import Navigation from './components/Navigation';

function App() {
    return (
        <div className="app">
            <Sidebar />
            <div className="main-area">
                <Navigation />
                <MainContent />
            </div>
        </div>
    );
}

export default App; 