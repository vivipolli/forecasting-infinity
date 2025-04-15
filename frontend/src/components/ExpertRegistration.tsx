import React, { useState } from 'react';
import { useExpert } from '../contexts/ExpertContext';
import { ExpertProfile } from '../types/expert';
import { Link } from 'react-router-dom';

const EXPERTISE_OPTIONS = [
  'Crypto',
  'Finance',
  'Technology',
  'Politics',
  'Science',
  'Economics',
];

export const ExpertRegistration: React.FC = () => {
  const { setExpertProfile } = useExpert();
  const [formData, setFormData] = useState<ExpertProfile>({
    name: '',
    email: '',
    expertise: [],
    socialProfiles: {},
    isVerified: false,
    experience: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.experience.length < 300) {
      alert('Please provide at least 300 characters about your experience');
      return;
    }

    const socialCount = Object.values(formData.socialProfiles).filter(Boolean).length;
    if (socialCount < 2) {
      alert('Please provide at least 2 social media profiles');
      return;
    }

    setExpertProfile(formData);
  };

  const handleExpertiseChange = (expertise: string) => {
    setFormData(prev => ({
      ...prev,
      expertise: prev.expertise.includes(expertise)
        ? prev.expertise.filter(e => e !== expertise)
        : [...prev.expertise, expertise]
    }));
  };

  const getSocialCount = () => {
    return Object.values(formData.socialProfiles).filter(Boolean).length;
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-2xl w-full p-6 bg-black border border-white/10 rounded-lg">
        <Link 
          to="/become-expert" 
          className="text-primary hover:text-primary/80 mb-4 inline-block"
        >
          ← Back
        </Link>
        <h2 className="text-2xl font-bold text-white mb-6 text-center">Become an Expert</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-white/70 mb-2">Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-white/70 mb-2">Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
              required
            />
          </div>

          <div>
            <label className="block text-white/70 mb-2">Expertise</label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {EXPERTISE_OPTIONS.map(expertise => (
                <button
                  key={expertise}
                  type="button"
                  onClick={() => handleExpertiseChange(expertise)}
                  className={`px-4 py-2 rounded-lg border transition-colors ${
                    formData.expertise.includes(expertise)
                      ? 'bg-primary/20 border-primary text-primary'
                      : 'bg-black border-white/10 text-white/70 hover:border-primary/50'
                  }`}
                >
                  {expertise}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-white/70 mb-2">
              About Me (Minimum 300 characters)
              <span className="text-sm text-white/50 ml-2">
                {formData.experience.length}/300
              </span>
            </label>
            <textarea
              value={formData.experience}
              onChange={(e) => setFormData(prev => ({ ...prev, experience: e.target.value }))}
              className="w-full h-40 px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary resize-none"
              required
              minLength={300}
              placeholder="Describe your experience in detail..."
            />
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="block text-white/70">Social Media Profiles</label>
              <span className="text-sm text-white/50">
                {getSocialCount()}/2 required
              </span>
            </div>
            
            <div>
              <label className="block text-white/70 mb-2">X (Twitter) Profile</label>
              <input
                type="text"
                value={formData.socialProfiles.x || ''}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  socialProfiles: { ...prev.socialProfiles, x: e.target.value }
                }))}
                className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://x.com/username"
              />
            </div>

            <div>
              <label className="block text-white/70 mb-2">GitHub Profile</label>
              <input
                type="text"
                value={formData.socialProfiles.github || ''}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  socialProfiles: { ...prev.socialProfiles, github: e.target.value }
                }))}
                className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://github.com/username"
              />
            </div>

            <div>
              <label className="block text-white/70 mb-2">LinkedIn Profile</label>
              <input
                type="text"
                value={formData.socialProfiles.linkedin || ''}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  socialProfiles: { ...prev.socialProfiles, linkedin: e.target.value }
                }))}
                className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://linkedin.com/in/username"
              />
            </div>

            <div>
              <label className="block text-white/70 mb-2">Instagram Profile</label>
              <input
                type="text"
                value={formData.socialProfiles.instagram || ''}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  socialProfiles: { ...prev.socialProfiles, instagram: e.target.value }
                }))}
                className="w-full px-4 py-2 bg-black border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://instagram.com/username"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            Submit Application
          </button>
        </form>
      </div>
    </div>
  );
}; 