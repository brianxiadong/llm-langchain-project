import React from 'react';
import './MainContent.css';

const MainContent = () => {
    const albums = [
        { id: 1, artist: 'Artist Name', genre: 'R&B', color: '#f5f5f5' },
        { id: 2, artist: 'Artist Name', genre: 'Indie pop', color: '#f5f5f5' },
        { id: 3, artist: 'Artist Name', genre: 'Hip hop', color: '#f5f5f5' },
        { id: 4, artist: 'Artist Name', genre: 'Electronic', color: '#f5f5f5' },
        { id: 5, artist: 'Artist Name', genre: 'R&B', color: '#f5f5f5' },
        { id: 6, artist: 'Artist Name', genre: 'Rock', color: '#f5f5f5' }
    ];

    const playlists = [
        { id: 1, title: 'Playlist 1', description: 'Description of playlist', color: '#93c5fd' },
        { id: 2, title: 'Playlist 2', description: 'Description of playlist', color: '#ffee93' },
        { id: 3, title: 'Playlist 3', description: 'Description of playlist', color: '#ffc1c1' },
        { id: 4, title: 'Playlist 4', description: 'Description of playlist', color: '#f5f5f5' }
    ];

    return (
        <div className="main-content">
            <div className="content-section">
                <div className="section-title">
                    <h2>Title</h2>
                    <p>Subheading</p>
                </div>

                <div className="large-grid">
                    {playlists.map(playlist => (
                        <div key={playlist.id} className="playlist-card">
                            <div className="playlist-cover" style={{ backgroundColor: playlist.color }}>
                                <span className="playlist-title-overlay">{playlist.title}</span>
                            </div>
                            <div className="playlist-info">
                                <h3>{playlist.title}</h3>
                                <p>{playlist.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="content-section">
                <div className="section-title">
                    <h2>Title</h2>
                    <p>Subheading</p>
                </div>

                <div className="small-grid">
                    {albums.map(album => (
                        <div key={album.id} className="album-card">
                            <div className="album-cover" style={{ backgroundColor: album.color }}></div>
                            <div className="album-info">
                                <h4>{album.artist}</h4>
                                <p>{album.genre}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MainContent; 