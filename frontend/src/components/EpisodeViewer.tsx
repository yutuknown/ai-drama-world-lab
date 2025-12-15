'use client';

import { useState, useEffect } from 'react';
import { episodeAPI } from '@/lib/api';
import { Episode } from '@/types';

export default function EpisodeViewer() {
  const [episodes, setEpisodes] = useState<Episode[]>([]);
  const [selectedEpisode, setSelectedEpisode] = useState<any>(null);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    loadEpisodes();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (playing && selectedEpisode) {
      interval = setInterval(() => {
        setCurrentFrame((prev) => {
          const next = prev + 1;
          if (next >= selectedEpisode.num_frames) {
            setPlaying(false);
            return 0;
          }
          return next;
        });
      }, 100); // 10 FPS playback
    }
    return () => clearInterval(interval);
  }, [playing, selectedEpisode]);

  const loadEpisodes = async () => {
    setLoading(true);
    try {
      const response = await episodeAPI.list();
      setEpisodes(response.episodes);
    } catch (error) {
      console.error('Error loading episodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadEpisode = async (episodeId: string) => {
    setLoading(true);
    try {
      const episode = await episodeAPI.get(episodeId);
      setSelectedEpisode(episode);
      setCurrentFrame(0);
      setPlaying(false);
    } catch (error) {
      console.error('Error loading episode:', error);
      alert('Failed to load episode');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (episodeId: string) => {
    if (!confirm('Are you sure you want to delete this episode?')) return;
    
    try {
      await episodeAPI.delete(episodeId);
      setEpisodes(episodes.filter(ep => ep.episode_id !== episodeId));
      if (selectedEpisode?.episode_id === episodeId) {
        setSelectedEpisode(null);
      }
    } catch (error) {
      console.error('Error deleting episode:', error);
      alert('Failed to delete episode');
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  return (
    <div className="episode-viewer">
      <h2>Episode Viewer</h2>
      <p>View and replay recorded episodes</p>
      
      {!selectedEpisode ? (
        <div className="episodes-list">
          <div className="header">
            <h3>Recorded Episodes ({episodes.length})</h3>
            <button onClick={loadEpisodes} disabled={loading}>
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
          
          {episodes.length === 0 ? (
            <p className="empty">No episodes recorded yet</p>
          ) : (
            episodes.map((episode) => (
              <div key={episode.episode_id} className="episode-card">
                <div className="episode-info">
                  <strong>{episode.metadata?.name || 'Unnamed Episode'}</strong>
                  <span className="meta">
                    {formatDate(episode.start_time)} • {episode.num_frames} frames
                  </span>
                  {episode.metadata?.description && (
                    <span className="description">{episode.metadata.description}</span>
                  )}
                </div>
                <div className="actions">
                  <button onClick={() => loadEpisode(episode.episode_id)}>
                    View
                  </button>
                  <button
                    className="delete"
                    onClick={() => handleDelete(episode.episode_id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="episode-player">
          <div className="player-header">
            <h3>{selectedEpisode.metadata?.name || 'Unnamed Episode'}</h3>
            <button onClick={() => setSelectedEpisode(null)}>
              Back to List
            </button>
          </div>
          
          <div className="player-info">
            <p>Frames: {selectedEpisode.num_frames}</p>
            <p>Current Frame: {currentFrame + 1} / {selectedEpisode.num_frames}</p>
          </div>
          
          <div className="player-controls">
            <button onClick={() => setPlaying(!playing)}>
              {playing ? 'Pause' : 'Play'}
            </button>
            <button onClick={() => setCurrentFrame(0)} disabled={playing}>
              Reset
            </button>
            <input
              type="range"
              min="0"
              max={Math.max(0, selectedEpisode.num_frames - 1)}
              value={currentFrame}
              onChange={(e) => setCurrentFrame(parseInt(e.target.value))}
              disabled={playing}
            />
          </div>
          
          {selectedEpisode.frames && selectedEpisode.frames[currentFrame] && (
            <div className="frame-info">
              <h4>Frame Data</h4>
              <pre>{JSON.stringify(selectedEpisode.frames[currentFrame], null, 2)}</pre>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .episode-viewer {
          padding: 20px;
          background: #2a2a3e;
          border-radius: 8px;
          color: white;
          max-height: 600px;
          overflow-y: auto;
        }
        
        h2 {
          margin: 0 0 10px 0;
          color: #4ecdc4;
        }
        
        p {
          margin: 0 0 20px 0;
          color: #b4b4b4;
        }
        
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
        }
        
        h3 {
          margin: 0;
          font-size: 16px;
          color: #4ecdc4;
        }
        
        button {
          padding: 8px 16px;
          background: #4ecdc4;
          color: #1a1a2e;
          border: none;
          border-radius: 4px;
          font-size: 14px;
          font-weight: bold;
          cursor: pointer;
          transition: background 0.2s;
        }
        
        button:hover:not(:disabled) {
          background: #45b7d1;
        }
        
        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        .empty {
          color: #6f6f6f;
          text-align: center;
          padding: 20px;
        }
        
        .episode-card {
          background: #1a1a2e;
          padding: 15px;
          border-radius: 4px;
          margin-bottom: 10px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .episode-info {
          flex: 1;
        }
        
        .episode-info strong {
          display: block;
          font-size: 15px;
          margin-bottom: 5px;
          color: #4ecdc4;
        }
        
        .meta {
          display: block;
          font-size: 12px;
          color: #888;
          margin-bottom: 5px;
        }
        
        .description {
          display: block;
          font-size: 13px;
          color: #b4b4b4;
        }
        
        .actions {
          display: flex;
          gap: 8px;
        }
        
        .delete {
          background: #ff6b6b;
        }
        
        .delete:hover {
          background: #ff5252;
        }
        
        .player-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }
        
        .player-info {
          background: #1a1a2e;
          padding: 10px;
          border-radius: 4px;
          margin-bottom: 15px;
        }
        
        .player-info p {
          margin: 5px 0;
          font-size: 13px;
        }
        
        .player-controls {
          display: flex;
          gap: 10px;
          align-items: center;
          margin-bottom: 20px;
        }
        
        .player-controls input[type="range"] {
          flex: 1;
        }
        
        .frame-info {
          background: #1a1a2e;
          padding: 15px;
          border-radius: 4px;
          max-height: 300px;
          overflow-y: auto;
        }
        
        .frame-info h4 {
          margin: 0 0 10px 0;
          color: #4ecdc4;
        }
        
        pre {
          margin: 0;
          font-size: 11px;
          color: #b4b4b4;
          white-space: pre-wrap;
        }
      `}</style>
    </div>
  );
}
