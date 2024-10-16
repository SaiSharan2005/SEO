// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import KeywordGeneration from './components/KeywordGeneration';
import KeywordStrategyBuilder from './components/KeywordStrategyBuilder';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/keyword-generation" element={<KeywordGeneration />} />
        <Route path="/keyword-strategy-builder" element={<KeywordStrategyBuilder />} />
      </Routes>
    </Router>
  );
}

export default App;
