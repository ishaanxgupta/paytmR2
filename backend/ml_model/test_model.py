import os
import sys

# We must define the class in __main__ because Kaggle notebook saved it there.
from sklearn.ensemble import VotingClassifier
class VotingLGBMEnsemble(VotingClassifier):
    @property
    def feature_importances_(self):
        import numpy as np
        return np.mean([est.feature_importances_ for est in self.estimators_], axis=0)

# Patch main module
setattr(sys.modules['__main__'], 'VotingLGBMEnsemble', VotingLGBMEnsemble)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.risk_engine import compute_risk_score

user_features = {
    'transaction_count': 50,
    'avg_transaction_amount': 2500,
    'kyc_tier': 3,
    'device_trust_score': 0.9,
    'days_since_registration': 365,
    'fraud_flags': 0,
    'total_spent': 125000,
}

print("Running test with SAFE features...")
score, factors = compute_risk_score(user_features)
print(f"Risk Score: {score}")
print(f"Factors: {factors}")

risky_user_features = {
    'transaction_count': 3,
    'avg_transaction_amount': 10000,
    'kyc_tier': 0,
    'device_trust_score': 0.1,
    'days_since_registration': 1,
    'fraud_flags': 3,
    'total_spent': 30000,
}

print("\nRunning test with RISKY features...")
score2, factors2 = compute_risk_score(risky_user_features)
print(f"Risk Score: {score2}")
print(f"Factors: {factors2}")
