import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ExpertProvider } from './contexts/ExpertContext';
import { Layout } from './components/Layout';
import { ExpertRegistration } from './components/ExpertRegistration';
import Home from './pages/Home';
import { ExpertBenefits } from './components/ExpertBenefits';
import History from './components/History';

const App: React.FC = () => {
  return (
    <ExpertProvider>
      <Router>
        <div className="min-h-screen bg-white">
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/events" element={<Home />} />
              <Route path="/history" element={<History />} />
              <Route path="/become-expert" element={<ExpertBenefits />} />
              <Route path="/become-expert/apply" element={<ExpertRegistration />} />
            </Routes>
          </Layout>
        </div>
      </Router>
    </ExpertProvider>
  );
};

export default App; 