"use client";

import { useEffect, useState } from "react";
import { type TokenFeatures, RugClassifier, type PredictionResult } from "@/lib/rugModel";

// Generate Fake Token Data for the simulation
function generateToken() {
  const isRug = Math.random() < 0.6; // Stream has 60% rugs

  const feats: TokenFeatures = {
    is_locked: isRug ? Math.random() < 0.3 : true,
    has_mint_function: isRug ? Math.random() < 0.8 : Math.random() < 0.1,
    creator_funded_by_tornado: isRug ? Math.random() < 0.7 : Math.random() < 0.05,
  };

  return {
    name: `Token ${Math.random().toString(36).substring(7).toUpperCase()}`,
    address: `0x${Math.random().toString(16).substring(2, 42)}`,
    features: feats,
  };
}

export default function Dashboard() {
  const [currentToken, setCurrentToken] = useState<any>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [history, setHistory] = useState<any[]>([]);

  // Simulation Loop
  useEffect(() => {
    const interval = setInterval(() => {
      const token = generateToken();
      const result = RugClassifier.predict(token.features);

      setCurrentToken(token);
      setPrediction(result);

      setHistory(prev => [
        { token, result, time: new Date().toLocaleTimeString() },
        ...prev.slice(0, 9) // Keep last 10
      ]);
    }, 4000); // New token every 4s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono p-4 md:p-8">
      <header className="flex justify-between items-center mb-12 border-b border-green-900 pb-4">
        <h1 className="text-2xl font-bold tracking-widest text-purple-500">
          RUG_PREDICTOR_V1
        </h1>
        <div className="text-xs text-gray-500">Live Mainnet Feed ●</div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* LEFT: Main Gauge */}
        <div className="flex flex-col items-center justify-center border border-gray-900 bg-gray-900/20 p-8 rounded-xl relative overflow-hidden">
          {/* Animated Background Grid */}
          <div className="absolute inset-0 z-0 opacity-10 bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>

          {prediction ? (
            <>
              {/* GAUGE */}
              <div className="relative z-10 w-64 h-64 flex items-center justify-center mb-8">
                <div className={`w-full h-full rounded-full border-8 ${prediction.score > 0.8 ? 'border-red-600 shadow-[0_0_50px_rgba(220,38,38,0.5)]' :
                    prediction.score > 0.5 ? 'border-yellow-500' : 'border-green-500 shadow-[0_0_50px_rgba(34,197,94,0.3)]'
                  } animate-pulse flex items-center justify-center`}>
                  <div className="text-center">
                    <div className="text-5xl font-bold text-white mb-2">
                      {Math.round(prediction.score * 100)}%
                    </div>
                    <div className="text-sm tracking-widest uppercase text-gray-400">Rug Probability</div>
                  </div>
                </div>
              </div>

              {/* DETAILS */}
              <div className="z-10 w-full max-w-md bg-black/50 p-6 rounded border border-gray-800">
                <h2 className="text-xl text-white mb-4">{currentToken.name}</h2>
                <div className="space-y-2 mb-6">
                  {prediction.factors.length > 0 ? (
                    prediction.factors.map((f: string, i: number) => (
                      <div key={i} className="flex items-center text-red-400">
                        <span className="mr-2">⚠️</span> {f}
                      </div>
                    ))
                  ) : (
                    <div className="text-green-400 flex items-center">
                      <span className="mr-2">✅</span> No Obvious Risks Detected
                    </div>
                  )}
                </div>

                <div className="text-xs text-gray-600 break-all font-mono">
                  CA: {currentToken.address}
                </div>
              </div>
            </>
          ) : (
            <div className="text-gray-500 animate-pulse">Initializing Neural Link...</div>
          )}
        </div>

        {/* RIGHT: History Feed */}
        <div className="border-l border-gray-900 pl-0 lg:pl-8">
          <h3 className="text-gray-400 mb-6 flex items-center">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-ping"></span>
            RECENTLY SCANNED PAIRS
          </h3>

          <div className="space-y-4">
            {history.map((item, idx) => (
              <div key={idx} className="flex justify-between items-center p-4 border border-gray-900 hover:bg-gray-900/30 transition-colors rounded">
                <div>
                  <div className="text-white font-bold">{item.token.name}</div>
                  <div className="text-xs text-gray-600">{item.time}</div>
                </div>

                <div className={`text-right ${item.result.score > 0.8 ? 'text-red-500' :
                    item.result.score > 0.5 ? 'text-yellow-500' : 'text-green-500'
                  }`}>
                  <div className="font-bold">{Math.round(item.result.score * 100)}% RISK</div>
                  <div className="text-xs opacity-75">{item.result.riskLevel}</div>
                </div>
              </div>
            ))}

            {history.length === 0 && (
              <div className="text-gray-800 italic">Waiting for new blocks...</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
