import React, { useState } from 'react';
import { useExpert } from '../contexts/ExpertContext';

interface EventCardProps {
  eventId: string;
  description: string;
  probability: number;
  context?: string;
  category?: string;
  expertValidations: number;
  onFeedback: (eventId: string, agrees: boolean) => void;
}

export const EventCard: React.FC<EventCardProps> = ({
  eventId,
  description,
  probability,
  context,
  category,
  expertValidations,
  onFeedback,
}) => {
  const { expertVerification } = useExpert();
  const [showModal, setShowModal] = useState(false);
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);
  const [selectedFeedback, setSelectedFeedback] = useState<boolean | null>(null);
  const probabilityColor = probability >= 0.5 
    ? 'text-primary' 
    : 'text-secondary';

  const handleFeedbackClick = (agrees: boolean) => {
    setSelectedFeedback(agrees);
    setShowFeedbackModal(true);
  };

  const handleConfirm = () => {
    if (selectedFeedback !== null) {
      onFeedback(eventId, selectedFeedback);
      setShowFeedbackModal(false);
    }
  };

  return (
    <>
      <div className="bg-black rounded-sm p-4 relative hover:translate-x-[-4px] hover:translate-y-[-4px] transition-transform duration-200 shadow-lg">
        <div className="absolute inset-0 bg-white/5 rounded-sm translate-x-1 translate-y-1 -z-10" />
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            {category && (
              <span className="inline-block px-2 py-1 text-xs rounded-full bg-primary/10 text-primary mb-2">
                {category}
              </span>
            )}
            
            <h3 className="text-lg font-bold text-white mb-1">
              {description.split('?')[0] + '?'}
            </h3>
            
            <div className="relative">
              <button
                onClick={() => setShowModal(true)}
                className="text-primary text-sm mt-1 hover:underline"
              >
                See More
              </button>
            </div>

            <div className="mt-3 flex items-center gap-2">
              <span className="text-secondary font-semibold">
                Validated by {expertValidations} experts
              </span>
              <div className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse" />
            </div>
          </div>
          
          <div className="flex flex-col items-end gap-2">
            <div className="text-right">
              <p className="text-xs text-white/50">Prediction</p>
              <p className={`text-xl font-bold ${probabilityColor}`}>
                {(probability * 100).toFixed(1)}%
              </p>
            </div>
            
            {expertVerification.isExpert ? (
              <div className="flex space-x-2">
                <button
                  onClick={() => handleFeedbackClick(true)}
                  className="px-3 py-1.5 text-sm rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
                >
                  Agree
                </button>
                <button
                  onClick={() => handleFeedbackClick(false)}
                  className="px-3 py-1.5 text-sm rounded-lg bg-secondary/10 text-secondary hover:bg-secondary/20 transition-colors"
                >
                  Disagree
                </button>
              </div>
            ) : (
              <div className="group relative">
                <button
                  disabled
                  className="px-3 py-1.5 text-sm rounded-lg bg-white/5 text-white/50 cursor-not-allowed"
                >
                  Provide Feedback
                </button>
                <div className="absolute bottom-full right-0 mb-2 w-64 p-2 bg-black/90 border border-white/10 rounded-lg text-xs text-white/70 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  You need to be a verified expert to provide feedback. Click "Become an Expert" in the sidebar to apply.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-gray-900">
                Event Details
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500">Question</p>
                <p className="text-gray-900 font-medium">{description.split('?')[0] + '?'}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-500">Description</p>
                <p className="text-gray-900 whitespace-pre-wrap">{description.split('?')[1]?.trim()}</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-500">Current Prediction</p>
                <p className={`text-xl font-bold ${probabilityColor}`}>
                  {(probability * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {showFeedbackModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              Confirm Your Feedback
            </h3>
            
            <div className="mb-6">
              <p className="text-gray-600 mb-2">Event Details:</p>
              <p className="text-gray-900 font-medium">{description}</p>
              {context && (
                <p className="text-gray-600 text-sm mt-1">{context}</p>
              )}
              <p className="text-gray-600 text-sm mt-2">
                Current Prediction: {(probability * 100).toFixed(1)}%
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowFeedbackModal(false)}
                className="px-4 py-2 text-sm rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                className={`px-4 py-2 text-sm rounded-lg ${
                  selectedFeedback
                    ? 'bg-primary/10 text-primary hover:bg-primary/20'
                    : 'bg-secondary/10 text-secondary hover:bg-secondary/20'
                } transition-colors`}
              >
                Confirm {selectedFeedback ? 'Agree' : 'Disagree'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}; 