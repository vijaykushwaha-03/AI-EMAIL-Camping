import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { Sidebar } from './components/layout/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Campaigns } from './pages/Campaigns';
import { CampaignNew } from './pages/CampaignNew';
import { Contacts } from './pages/Contacts';
import './index.css';

// Placeholder pages
const Templates = () => (
  <div className="page">
    <h1>Templates</h1>
    <p style={{ color: 'var(--text-secondary)' }}>Email template gallery coming soon...</p>
  </div>
);

const Analytics = () => (
  <div className="page">
    <h1>Analytics</h1>
    <p style={{ color: 'var(--text-secondary)' }}>Detailed analytics coming soon...</p>
  </div>
);

const Settings = () => (
  <div className="page">
    <h1>Settings</h1>
    <p style={{ color: 'var(--text-secondary)' }}>Configuration settings coming soon...</p>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/campaigns" element={<Campaigns />} />
              <Route path="/campaigns/new" element={<CampaignNew />} />
              <Route path="/contacts" element={<Contacts />} />
              <Route path="/templates" element={<Templates />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </AnimatePresence>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
