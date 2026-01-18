# Rug Predictor Dashboard

This is a Next.js application that visualizes Rug Pull probabilities using a client-side Naive Bayes model.

## Setup

1.  Run `npm install` to install dependencies.
2.  Run `npm run dev` to obtain a local preview.

## Deployment (Vercel)

This project is optimized for [Vercel](https://vercel.com/new).

1.  Push this folder (`web/`) to a GitHub repository.
2.  Import the repository in Vercel.
3.  Vercel will detect Next.js and deploy automatically.

## How it Works

-   **Model:** `lib/rugModel.ts` contains the pre-trained weights from our Python training phase.
-   **Simulation:** `app/page.tsx` generates synthetic token data and runs it through the model in real-time.
