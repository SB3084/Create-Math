import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';

const ManimEditor = () => {
    const [code, setCode] = useState(`from manim import *

class MainScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.wait(1)`);
    const [videoUrl, setVideoUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const checkStatus = async (renderId) => {
        try {
            const { data } = await axios.get(`/api/status/${renderId}`);
            if (data.status === 'complete') {
                setVideoUrl(data.url + `?t=${Date.now()}`);
                setLoading(false);
            } else {
                setTimeout(() => checkStatus(renderId), 2000);
            }
        } catch (err) {
            setError('Failed to check render status');
            setLoading(false);
        }
    };

    const handleRender = async () => {
        setLoading(true);
        setError('');
        try {
            const { data } = await axios.post('/api/render', { script: code });
            checkStatus(data.render_id);
        } catch (err) {
            setError(err.response?.data?.detail || 'Render failed');
            setLoading(false);
        }
    };

    return (
        <div className="editor-container">
            <div className="editor-header">
                <h2>Manim Editor</h2>
                <button onClick={handleRender} disabled={loading}>
                    {loading ? 'Rendering...' : 'Render'}
                </button>
            </div>
            
            <Editor
                height="60vh"
                defaultLanguage="python"
                value={code}
                onChange={setCode}
                options={{ 
                    minimap: { enabled: false },
                    fontSize: 14,
                    scrollBeyondLastLine: false
                }}
            />
            
            {error && <div className="error">{error}</div>}
            
            {videoUrl && (
                <div className="video-container">
                    <video key={videoUrl} controls autoPlay>
                        <source src={videoUrl} type="video/mp4" />
                    </video>
                </div>
            )}
        </div>
    );
};

export default ManimEditor;
