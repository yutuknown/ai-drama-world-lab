'use client';

import { useState } from 'react';
import { worldAPI } from '@/lib/api';
import { useAppStore } from '@/store/appStore';

export default function SceneDesigner() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const { setScene } = useAppStore();

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    try {
      const scene = await worldAPI.generate(prompt);
      setScene(scene);
      alert(`Scene "${scene.name}" generated successfully!`);
    } catch (error) {
      console.error('Error generating scene:', error);
      alert('Failed to generate scene. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const examplePrompts = [
    'A cozy indoor room with furniture',
    'An outdoor park with trees and rocks',
    'A theater stage with backdrop',
    'A simple scene with colorful objects',
  ];

  return (
    <div className="scene-designer">
      <h2>Scene Designer</h2>
      <p>Generate 3D worlds from text descriptions</p>
      
      <div className="prompt-input">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the scene you want to create..."
          rows={4}
          disabled={loading}
        />
        <button onClick={handleGenerate} disabled={loading || !prompt.trim()}>
          {loading ? 'Generating...' : 'Generate Scene'}
        </button>
      </div>
      
      <div className="examples">
        <h3>Example Prompts:</h3>
        {examplePrompts.map((example, index) => (
          <button
            key={index}
            className="example-button"
            onClick={() => setPrompt(example)}
            disabled={loading}
          >
            {example}
          </button>
        ))}
      </div>

      <style jsx>{`
        .scene-designer {
          padding: 20px;
          background: #2a2a3e;
          border-radius: 8px;
          color: white;
        }
        
        h2 {
          margin: 0 0 10px 0;
          color: #4ecdc4;
        }
        
        p {
          margin: 0 0 20px 0;
          color: #b4b4b4;
        }
        
        .prompt-input {
          margin-bottom: 20px;
        }
        
        textarea {
          width: 100%;
          padding: 12px;
          border: 2px solid #3a3a4e;
          border-radius: 4px;
          background: #1a1a2e;
          color: white;
          font-family: inherit;
          font-size: 14px;
          resize: vertical;
          margin-bottom: 10px;
        }
        
        textarea:focus {
          outline: none;
          border-color: #4ecdc4;
        }
        
        button {
          width: 100%;
          padding: 12px 24px;
          background: #4ecdc4;
          color: #1a1a2e;
          border: none;
          border-radius: 4px;
          font-size: 16px;
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
        
        .examples h3 {
          font-size: 14px;
          color: #b4b4b4;
          margin-bottom: 10px;
        }
        
        .example-button {
          width: 100%;
          margin-bottom: 8px;
          padding: 10px;
          background: #3a3a4e;
          font-size: 14px;
          font-weight: normal;
          text-align: left;
        }
        
        .example-button:hover:not(:disabled) {
          background: #4a4a5e;
        }
      `}</style>
    </div>
  );
}
