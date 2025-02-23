import { useState } from 'react'
import EditorComponent from './components/Editor'
import './App.css'

function App() {
  const [darkMode, setDarkMode] = useState(true)

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'}`}>
      <header className="app-header">
        <h1 className="app-title">✨ Manim Studio Pro</h1>
        <div className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '🌞' : '🌙'}
        </div>
      </header>
      <EditorComponent />
      <footer className="app-footer">
        <p>Powered by Manim CE v0.18 | Render Engine v1.2.3</p>
      </footer>
    </div>
  )
}

export default App
