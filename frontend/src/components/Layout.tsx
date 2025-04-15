import React from 'react';
import { Link } from 'react-router-dom';
import { useExpert } from '../contexts/ExpertContext';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { expertVerification, logout } = useExpert();

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 p-6 border-r border-primary/20">
        <div className="flex items-center space-x-3 mb-8">
          <h1 className="text-2xl font-bold text-black">Forecaster X</h1>
        </div>
        
        <nav className="space-y-2">
          <Link to="/" className="block text-black hover:text-black transition-colors">
            Dashboard
          </Link>
          <Link to="/events" className="block text-black hover:text-black transition-colors">
            Active Events
          </Link>
          <Link to="/history" className="block text-black hover:text-black transition-colors">
            History
          </Link>
        </nav>

        <div className="mt-8 pt-8 border-t border-white/10">
          {expertVerification.isExpert ? (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-primary"></div>
                <span className="text-primary">Verified Expert</span>
              </div>
              <button
                onClick={logout}
                className="w-full px-4 py-2 text-white/70 hover:text-white transition-colors text-left"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link
              to="/become-expert"
              className="block px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors text-center"
            >
              Become an Expert
            </Link>
          )}
        </div>
      </aside>
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  );
}; 