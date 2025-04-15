import React from 'react';
import { useExpert } from '../contexts/ExpertContext';

interface PastPrediction {
  id: string;
  question: string;
  predictedProbability: number;
  actualOutcome: boolean;
  validationCount: number;
  expertReward?: {
    validated: boolean;
    accurate: boolean;
    rewardAmount: number;
  };
}

const History: React.FC = () => {
  const { expertVerification } = useExpert();
  const [pastPredictions] = React.useState<PastPrediction[]>([
    {
      id: '1',
      question: 'Will the new AI model pass the Turing test by 2025?',
      predictedProbability: 0.75,
      actualOutcome: true,
      validationCount: 12,
      expertReward: {
        validated: true,
        accurate: true,
        rewardAmount: 100
      }
    },
    {
      id: '2',
      question: 'Will renewable energy surpass fossil fuels by 2030?',
      predictedProbability: 0.65,
      actualOutcome: false,
      validationCount: 8,
      expertReward: {
        validated: true,
        accurate: false,
        rewardAmount: 50
      }
    },
    {
      id: '3',
      question: 'Will quantum computing achieve commercial viability by 2026?',
      predictedProbability: 0.45,
      actualOutcome: true,
      validationCount: 15
    }
  ]);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-white mb-8">Prediction History</h1>
      
      <div className="space-y-6">
        {pastPredictions.map((prediction) => (
          <div key={prediction.id} className="bg-white rounded-sm p-6 shadow-lg">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  {prediction.question}
                </h2>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span>
                    Predicted: {(prediction.predictedProbability * 100).toFixed(1)}%
                  </span>
                  <span>
                    Actual: {prediction.actualOutcome ? 'Yes' : 'No'}
                  </span>
                  <span>
                    Validations: {prediction.validationCount}
                  </span>
                </div>
              </div>
            </div>

            {expertVerification.isExpert && prediction.expertReward && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Your Contribution</h3>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${
                      prediction.expertReward.validated ? 'bg-green-500' : 'bg-gray-300'
                    }`} />
                    <span className="text-sm text-gray-600">
                      {prediction.expertReward.validated ? 'Validated' : 'Not Validated'}
                    </span>
                  </div>
                  {prediction.expertReward.validated && (
                    <>
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${
                          prediction.expertReward.accurate ? 'bg-green-500' : 'bg-red-500'
                        }`} />
                        <span className="text-sm text-gray-600">
                          {prediction.expertReward.accurate ? 'Accurate' : 'Inaccurate'}
                        </span>
                      </div>
                      {prediction.expertReward.accurate && (
                        <div className="ml-auto">
                          <span className="text-sm font-medium text-primary">
                            +{prediction.expertReward.rewardAmount} points
                          </span>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default History; 