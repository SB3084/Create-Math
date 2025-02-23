import React, { useState } from 'react';
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

    const checkRenderStatus = async (renderId) => {
        try {
            const response = await axios.get(`/api/status/${renderId}`);
            if (response.data.status === 'complete') {
                setVideoUrl(response.data.url);
                setLoading(false);
            } else {
                setTimeout(() => checkRenderStatus(renderId), 2000);
            }
        } catch (err) {
            setError('Error checking render status');
            setLoading(false);
        }
    };

    const handleRender = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post('/api/render', {
                script: code
            });
            checkRenderStatus(response.data.render_id);
        } catch (err) {
            setError(err.response?.data?.detail || 'Render failed');
            setLoading(false);
        }
    };

    return (
        <div className="editor-container">
            <div className="editor-header">
                <h2>Manim Editor</h2>
                <button 
                    onClick={handleRender}
                    disabled={loading}
                >
                    {loading ? 'Rendering...' : 'Render Animation'}
                </button>
            </div>
            
            <Editor
                height="60vh"
                defaultLanguage="python"
                defaultValue={code}
                onChange={(value) => setCode(value)}
                options={{
                    minimap: { enabled: false },
                    fontSize: 14
                }}
            />
            
            {error && <div className="error-message">{error}</div>}
            
            {videoUrl && (
                <div className="video-preview">
                    <video controls autoPlay>
                        <source src={videoUrl} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            )}
        </div>
    );
};

export default ManimEditor;
