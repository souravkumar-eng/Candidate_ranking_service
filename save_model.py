
"""
Save the recommender model to a .pkl file.
"""

import pickle
from recommender_model import RecommenderModel

# Create model instance
model = RecommenderModel()

# Save to disk
with open("model/recommender.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved to model/recommender.pkl")
