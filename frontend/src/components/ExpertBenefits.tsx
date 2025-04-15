import React from 'react';
import { Link } from 'react-router-dom';

export const ExpertBenefits: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-black">Become a Verified Expert</h1>
        <p className="text-xl text-black/70">
          Join our network of experts and help shape the future of prediction markets
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-black border border-white/10 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-bold text-white">Network Benefits</h2>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Enhanced Reputation:</strong> Build your credibility in the prediction market ecosystem
              </span>
            </li>
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Early Access:</strong> Get priority access to new events and predictions
              </span>
            </li>
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Community Influence:</strong> Your feedback directly impacts the network's predictions
              </span>
            </li>
          </ul>
        </div>

        <div className="bg-black border border-white/10 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-bold text-white">Rewards System</h2>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Accuracy Rewards:</strong> Earn tokens based on your prediction accuracy
              </span>
            </li>
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Staking Benefits:</strong> Higher staking rewards for verified experts
              </span>
            </li>
            <li className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                <span className="text-primary">✓</span>
              </div>
              <span className="text-white/70">
                <strong className="text-white">Governance Rights:</strong> Participate in network decisions and upgrades
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-black border border-white/10 rounded-lg p-6 space-y-4">
        <h2 className="text-2xl font-bold text-white">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">1</div>
            <h3 className="text-lg font-bold text-white">Apply</h3>
            <p className="text-white/70">Submit your expertise and social profiles for verification</p>
          </div>
          <div className="space-y-2">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">2</div>
            <h3 className="text-lg font-bold text-white">Verify</h3>
            <p className="text-white/70">Get verified and start providing feedback on predictions</p>
          </div>
          <div className="space-y-2">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">3</div>
            <h3 className="text-lg font-bold text-white">Earn</h3>
            <p className="text-white/70">Build your reputation and earn rewards for accurate feedback</p>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <Link
          to="/become-expert/apply"
          className="px-8 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors text-lg font-medium"
        >
          Start Your Application
        </Link>
      </div>
    </div>
  );
}; 