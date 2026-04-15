"""
ML Model Training Script for Job Role Recommendation
This script trains a RandomForest classifier to recommend job roles based on user skills
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import csv

def load_job_roles_data(csv_path='data/it_jobs_roles.csv'):
    """Load job roles and skills from CSV"""
    roles_data = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSV has 'Job Title' not 'Role'
                role_name = row.get('Job Title', '').strip()
                skills_str = row.get('Skills', '').strip()
                
                if role_name and skills_str:
                    roles_data.append({
                        'role': role_name,
                        'skills': skills_str
                    })
    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_path}")
        print("Please ensure the CSV file exists in the data directory")
        return []
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return []
    
    return roles_data

def train_role_recommender():
    """Train the job role recommendation model"""
    print("Loading job roles data...")
    roles_data = load_job_roles_data()
    
    if not roles_data:
        print("ERROR: No data loaded from CSV!")
        return None
    
    # Prepare data
    skills_list = [item['skills'] for item in roles_data]
    roles_list = [item['role'] for item in roles_data]
    
    print(f"Loaded {len(roles_data)} job roles")
    print(f"Sample roles: {roles_list[:5]}")
    
    # Create TF-IDF vectorizer
    print("\nCreating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1,
        lowercase=True
    )
    
    X = vectorizer.fit_transform(skills_list)
    y = np.array(roles_list)
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Unique roles: {len(set(y))}")
    
    # Split data - don't stratify if we have too few samples
    # Check if we can stratify (need at least 2 samples per class)
    from collections import Counter
    class_counts = Counter(y)
    min_class_count = min(class_counts.values())
    
    if min_class_count >= 2 and len(set(y)) > 1:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    # Train Random Forest
    print("\nTraining RandomForest classifier...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=2,
        random_state=42,
        n_jobs=-1
    )
    
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model and vectorizer
    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    model_path = os.path.join(models_dir, 'role_recommender.pkl')
    vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
    
    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"\n✅ Model saved to: {model_path}")
    print(f"✅ Vectorizer saved to: {vectorizer_path}")
    
    return clf, vectorizer

from sklearn.metrics.pairwise import cosine_similarity

def predict_roles(user_skills, top_n=3):
    """Predict top N job roles for given skills using Cosine Similarity"""
    try:
        # Load vectorizer
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        
        # We need the original vectors to compare against
        roles_data = load_job_roles_data()
        if not roles_data:
            return []
            
        role_names = [item['role'] for item in roles_data]
        role_skills = [item['skills'] for item in roles_data]
        
        # Vectorize all roles
        X_roles = vectorizer.transform(role_skills)
        
        # Convert user skills to string
        if isinstance(user_skills, list):
            skills_str = ', '.join(user_skills)
        else:
            skills_str = str(user_skills)
        
        # Transform user skills
        X_user = vectorizer.transform([skills_str])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(X_user, X_roles)[0]
        
        # Get top N indices
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        recommendations = []
        for idx in top_indices:
            score = similarities[idx]
            # Only include if there's some similarity
            if score > 0:
                recommendations.append({
                    'role': role_names[idx],
                    'confidence': int(score * 100)
                })
        
        # Fallback: if no matches found via TF-IDF, try basic keyword overlap
        if not recommendations:
            user_skills_set = set(s.lower().strip() for s in (user_skills if isinstance(user_skills, list) else user_skills.split(',')))
            
            overlap_scores = []
            for item in roles_data:
                role_skills_set = set(s.lower().strip() for s in item['skills'].split(','))
                intersection = user_skills_set.intersection(role_skills_set)
                if intersection:
                    overlap_scores.append({
                        'role': item['role'],
                        'confidence': int((len(intersection) / len(role_skills_set)) * 100)
                    })
            
            overlap_scores.sort(key=lambda x: x['confidence'], reverse=True)
            recommendations = overlap_scores[:top_n]

        return recommendations
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        return []

if __name__ == '__main__':
    print("=" * 60)
    print("JOB ROLE RECOMMENDATION MODEL TRAINING")
    print("=" * 60)
    
    # Train the model
    result = train_role_recommender()
    
    if result is None:
        print("\n❌ Training failed! Please check the error messages above.")
        exit(1)
    
    clf, vectorizer = result
    
    # Test prediction
    print("\n" + "=" * 60)
    print("TESTING PREDICTIONS")
    print("=" * 60)
    
    test_skills = ["Python, Machine Learning, TensorFlow, Data Analysis, SQL"]
    print(f"\nTest Skills: {test_skills[0]}")
    
    recommendations = predict_roles(test_skills[0], top_n=3)
    print("\nRecommended Roles:")
    for rec in recommendations:
        print(f"  - {rec['role']}: {rec['confidence']}% confidence")
