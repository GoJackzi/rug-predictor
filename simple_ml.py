import csv
import json
import math

class NaiveBayesClassifier:
    def __init__(self):
        self.priors = {}
        self.likelihoods = {}
        self.classes = []

    def train(self, features, labels):
        self.classes = list(set(labels))
        total_samples = len(labels)
        
        # Calculate Priors: P(Class)
        for c in self.classes:
            self.priors[c] = labels.count(c) / total_samples
            self.likelihoods[c] = {}

        # Calculate Likelihoods: P(Feature | Class)
        # We assume binary/categorical features for simplicity (Bernoulli Naive Bayes) or discretize continuous ones
        # For this prototype, we'll focus on the boolean/categorical columns
        
        feature_names = list(features[0].keys())
        
        for c in self.classes:
            # Filter samples for this class
            class_samples = [features[i] for i, label in enumerate(labels) if label == c]
            class_count = len(class_samples)
            
            for fname in feature_names:
                # Calculate probability of feature=True/Value given Class
                # For simplicity, let's process 'is_locked', 'has_mint_function', 'creator_funded_by_tornado'
                # And assume they are 'True'/'False' strings or booleans
                
                # Laplace Smoothing (+1)
                count_true = sum(1 for s in class_samples if str(s[fname]).lower() == 'true')
                self.likelihoods[c][fname] = (count_true + 1) / (class_count + 2)

    def predict_proba(self, sample):
        """Returns dict of {class: probability}"""
        scores = {}
        for c in self.classes:
            # log(P(Class))
            scores[c] = math.log(self.priors[c])
            
            for fname, val in sample.items():
                if fname in self.likelihoods[c]:
                    prob_true = self.likelihoods[c][fname]
                    if str(val).lower() == 'true':
                        scores[c] += math.log(prob_true)
                    else:
                        scores[c] += math.log(1 - prob_true)
        
        # Convert log scores back to probabilities (Softmaxish)
        # 1. Shift to avoid overflow
        max_score = max(scores.values())
        scores_exp = {c: math.exp(s - max_score) for c, s in scores.items()}
        total = sum(scores_exp.values())
        
        return {c: s / total for c, s in scores_exp.items()}
    
    def save(self, filename="model_weights.json"):
        data = {
            "priors": self.priors,
            "likelihoods": self.likelihoods,
            "classes": self.classes
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load(self, filename="model_weights.json"):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.priors = data["priors"]
            self.likelihoods = data["likelihoods"]
            self.classes = data["classes"]

def train_rug_model():
    print("Training Custom Naive Bayes Model...")
    
    features = []
    labels = []
    
    # Load Data
    try:
        with open('labeled_pairs.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Extract Features
                feat = {
                    'is_locked': row['is_locked'],
                    'has_mint_function': row['has_mint_function'],
                    'creator_funded_by_tornado': row['creator_funded_by_tornado']
                }
                features.append(feat)
                labels.append(row['status'])
    except FileNotFoundError:
        print("Error: labeled_pairs.csv not found!")
        return

    # Train
    clf = NaiveBayesClassifier()
    clf.train(features, labels)
    
    # Save
    clf.save("rug_model.json")
    print("Model trained and saved to rug_model.json")
    
    # Test on a Fake Case
    test_case = {
        'is_locked': False,
        'has_mint_function': True,
        'creator_funded_by_tornado': True
    }
    probs = clf.predict_proba(test_case)
    print("\nTest Prediction for Dangerous Token:")
    print(f"Features: {test_case}")
    print(f"Probabilities: {probs}")
    
    return clf

if __name__ == "__main__":
    train_rug_model()
