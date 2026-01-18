export type TokenFeatures = {
    is_locked: boolean;
    has_mint_function: boolean;
    creator_funded_by_tornado: boolean;
};

export type PredictionResult = {
    score: number; // 0 to 1 (Rug Probability)
    riskLevel: "SAFE" | "RISKY" | "DANGEROUS";
    factors: string[];
};

// Trained Weights from rug_model.json
const MODEL = {
    priors: { SAFE: 0.22, RUG: 0.78 },
    classes: ["SAFE", "RUG"],
    likelihoods: {
        SAFE: {
            is_locked: 0.9910714285714286,
            has_mint_function: 0.14285714285714285,
            creator_funded_by_tornado: 0.14285714285714285,
        },
        RUG: {
            is_locked: 0.28316326530612246,
            has_mint_function: 0.6275510204081632,
            creator_funded_by_tornado: 0.6862244897959183,
        },
    },
};

export class RugClassifier {
    static predict(features: TokenFeatures): PredictionResult {
        const scores: Record<string, number> = {};

        // Calculate Log Posterior
        for (const c of MODEL.classes) {
            // @ts-ignore
            scores[c] = Math.log(MODEL.priors[c]);

            for (const [key, val] of Object.entries(features)) {
                // @ts-ignore
                const probTrue = MODEL.likelihoods[c][key];
                if (val) {
                    scores[c] += Math.log(probTrue);
                } else {
                    scores[c] += Math.log(1 - probTrue);
                }
            }
        }

        // Softmax
        const maxScore = Math.max(...Object.values(scores));
        const expScores = {
            SAFE: Math.exp(scores["SAFE"] - maxScore),
            RUG: Math.exp(scores["RUG"] - maxScore),
        };
        const total = expScores.SAFE + expScores.RUG;

        // Probability of RUG
        const rugProb = expScores.RUG / total;

        // Determine Risk Factors
        const factors = [];
        if (!features.is_locked) factors.push("Liquidity Not Locked");
        if (features.has_mint_function) factors.push("Hidden Mint Function");
        if (features.creator_funded_by_tornado) factors.push("Dev Funded by Tornado Cash");
        if (factors.length === 0 && rugProb > 0.5) factors.push("Suspicious Trading Pattern");

        let riskLevel: "SAFE" | "RISKY" | "DANGEROUS" = "SAFE";
        if (rugProb > 0.8) riskLevel = "DANGEROUS";
        else if (rugProb > 0.5) riskLevel = "RISKY";

        return {
            score: rugProb,
            riskLevel,
            factors,
        };
    }
}
