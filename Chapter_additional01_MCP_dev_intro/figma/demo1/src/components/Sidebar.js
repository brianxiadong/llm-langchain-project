import React from 'react';
import './Sidebar.css';

const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2 className="app-title">Music app</h2>
            </div>

            <div className="menu-section">
                <div className="menu-item discover">
                    <span>Discover</span>
                </div>
                <div className="menu-item active">
                    <div className="menu-icon home-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M9 22V12H15V22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                    <span>Home</span>
                </div>
                <div className="menu-item">
                    <div className="menu-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2" />
                            <path d="M21 21L16.65 16.65" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                    <span>Browse</span>
                </div>
                <div className="menu-item">
                    <div className="menu-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="2" stroke="currentColor" strokeWidth="2" />
                            <path d="M16.24 7.76A6 6 0 0 1 19.07 19.07A6 6 0 0 1 7.76 16.24M16.24 7.76A6 6 0 0 0 7.76 16.24M16.24 7.76L7.76 16.24" stroke="currentColor" strokeWidth="2" />
                        </svg>
                    </div>
                    <span>Radio</span>
                </div>
            </div>

            <div className="library-section">
                <div className="library-header">
                    <span>Library</span>
                </div>
                <div className="menu-item">
                    <div className="menu-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <line x1="8" y1="6" x2="21" y2="6" stroke="currentColor" strokeWidth="2" />
                            <line x1="8" y1="12" x2="21" y2="12" stroke="currentColor" strokeWidth="2" />
                            <line x1="8" y1="18" x2="21" y2="18" stroke="currentColor" strokeWidth="2" />
                            <line x1="3" y1="6" x2="3.01" y2="6" stroke="currentColor" strokeWidth="2" />
                            <line x1="3" y1="12" x2="3.01" y2="12" stroke="currentColor" strokeWidth="2" />
                            <line x1="3" y1="18" x2="3.01" y2="18" stroke="currentColor" strokeWidth="2" />
                        </svg>
                    </div>
                    <span>Playlists</span>
                </div>
                <div className="menu-item">
                    <div className="menu-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M9 18V5L21 3V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <circle cx="6" cy="18" r="3" stroke="currentColor" strokeWidth="2" />
                            <circle cx="18" cy="16" r="3" stroke="currentColor" strokeWidth="2" />
                        </svg>
                    </div>
                    <span>Songs</span>
                </div>
                <div className="menu-item">
                    <div className="menu-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
                            <path d="M8 14S9.5 16 12 16S16 14 16 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <line x1="9" y1="9" x2="9.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <line x1="15" y1="9" x2="15.01" y2="9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                    <span>Personalized picks</span>
                </div>
            </div>
        </div>
    );
};

export default Sidebar; 