import React, { createContext, useContext, useState, useEffect } from 'react';
import { ExpertProfile, ExpertVerification } from '../types/expert';

interface ExpertContextType {
  expertVerification: ExpertVerification;
  setExpertProfile: (profile: ExpertProfile) => void;
  logout: () => void;
}

const ExpertContext = createContext<ExpertContextType | undefined>(undefined);

export const ExpertProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [expertVerification, setExpertVerification] = useState<ExpertVerification>(() => {
    const stored = localStorage.getItem('expertVerification');
    return stored ? JSON.parse(stored) : { isExpert: false };
  });

  useEffect(() => {
    localStorage.setItem('expertVerification', JSON.stringify(expertVerification));
  }, [expertVerification]);

  const setExpertProfile = (profile: ExpertProfile) => {
    setExpertVerification({
      isExpert: true,
      profile: { ...profile, isVerified: true }
    });
  };

  const logout = () => {
    setExpertVerification({ isExpert: false });
  };

  return (
    <ExpertContext.Provider value={{ expertVerification, setExpertProfile, logout }}>
      {children}
    </ExpertContext.Provider>
  );
};

export const useExpert = () => {
  const context = useContext(ExpertContext);
  if (!context) {
    throw new Error('useExpert must be used within an ExpertProvider');
  }
  return context;
}; 