'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { useAppStore } from '@/store/appStore';
import SceneDesigner from '@/components/SceneDesigner';
import AgentStudio from '@/components/AgentStudio';
import EpisodeViewer from '@/components/EpisodeViewer';
import SimulationController from '@/components/SimulationController';

// Dynamic import for Scene3D to avoid SSR issues with Three.js
const Scene3D = dynamic(() => import('@/components/Scene3D'), {
  ssr: false,
  loading: () => <div style={{ width: '100%', height: '100%', background: '#1a1a2e', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>Loading 3D Scene...</div>
});

export default function Home() {
  const [activeTab, setActiveTab] = useState<'scene' | 'agent' | 'episode'>('scene');
  const { currentScene, agents } = useAppStore();

  return (
    <div className="app-container">
      <header className="header">
        <h1>🎭 AI Drama World Lab</h1>
        <p>Create interactive 3D worlds with intelligent AI agents</p>
      </header>

      <div className="main-content">
        <div className="viewport">
          <Scene3D 
            objects={currentScene?.objects || []} 
            agents={agents}
          />
        </div>

        <div className="sidebar">
          <div className="tabs">
            <button 
              className={activeTab === 'scene' ? 'active' : ''}
              onClick={() => setActiveTab('scene')}
            >
              Scene Designer
            </button>
            <button 
              className={activeTab === 'agent' ? 'active' : ''}
              onClick={() => setActiveTab('agent')}
            >
              Agent Studio
            </button>
            <button 
              className={activeTab === 'episode' ? 'active' : ''}
              onClick={() => setActiveTab('episode')}
            >
              Episode Viewer
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'scene' && <SceneDesigner />}
            {activeTab === 'agent' && <AgentStudio />}
            {activeTab === 'episode' && <EpisodeViewer />}
          </div>

          <SimulationController />
        </div>
      </div>

      <style jsx>{`
        .app-container {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: #0f0f1e;
        }

        .header {
          padding: 20px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .header h1 {
          margin: 0;
          font-size: 28px;
          color: white;
        }

        .header p {
          margin: 5px 0 0 0;
          font-size: 14px;
          color: rgba(255, 255, 255, 0.9);
        }

        .main-content {
          display: flex;
          flex: 1;
          overflow: hidden;
        }

        .viewport {
          flex: 1;
          position: relative;
          background: #1a1a2e;
        }

        .sidebar {
          width: 400px;
          display: flex;
          flex-direction: column;
          background: #16162a;
          border-left: 1px solid #2a2a3e;
          overflow-y: auto;
        }

        .tabs {
          display: flex;
          background: #1a1a2e;
          border-bottom: 2px solid #2a2a3e;
        }

        .tabs button {
          flex: 1;
          padding: 15px;
          background: transparent;
          color: #888;
          border: none;
          cursor: pointer;
          font-size: 13px;
          font-weight: 600;
          transition: all 0.2s;
          border-bottom: 3px solid transparent;
        }

        .tabs button:hover {
          background: #2a2a3e;
          color: #b4b4b4;
        }

        .tabs button.active {
          color: #4ecdc4;
          border-bottom-color: #4ecdc4;
          background: #2a2a3e;
        }

        .tab-content {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
        }

        @media (max-width: 1024px) {
          .main-content {
            flex-direction: column;
          }

          .sidebar {
            width: 100%;
            max-height: 50vh;
          }
        }
      `}</style>
    </div>
  );
}
