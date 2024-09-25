import pandas as pd
import joblib

# Load the dataset (replace with your test data)
file_path = 'input_data.xlsx'  # Replace with the generic input file name
data = pd.read_excel(file_path)

# Ensure Business Name (or Premise Name) is a string and handle missing values
data['Business Name'] = data['Business Name'].astype(str).fillna('')

# Load the trained model, vectorizer, and label encoder
model = joblib.load('model.pkl')  # Generic model name
tfidf_vectorizer = joblib.load('vectorizer.pkl')  # Generic vectorizer name
label_encoder = joblib.load('label_encoder.pkl')  # Generic label encoder name

# Preprocess the Business Name column
X_data = tfidf_vectorizer.transform(data['Business Name'])

# Define keyword-based rules
keyword_rules = {
    'apartment': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'building': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'assisted living': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year', 'Commercial Hood Cleaning', 'Commercial Hood Suppression'],
    'auto': ['Fire Sprinkler System', 'Fire Alarm System'],
    'bank': ['Fire Alarm System'],
    'food': ['Commercial Hood Cleaning', 'Commercial Hood Suppression'],
    'church': ['Fire Alarm System', 'Fire Sprinkler System', 'Commercial Hood Cleaning', 'Commercial Hood Suppression'],
    'care': ['Fire Alarm System', 'Fire Sprinkler System', 'Commercial Hood Cleaning', 'Commercial Hood Suppression'],
    'shop': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'store': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'market': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'school': ['Fire Alarm System', 'Fire Sprinkler System', 'Commercial Hood Cleaning', 'Commercial Hood Suppression'],
    'hotel': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year'],
    'group home': ['Fire Alarm System', 'Fire Sprinkler System', 'Sprinkler 5 Year']
}

# Keyword variations to account for different spellings/phrases
keyword_variations = {
    'apartment': ['apartments', 'apartment', 'apts'],
    'building': ['building', 'bldg'],
    'assisted living': ['assisted', 'assisted living'],
    'auto': ['auto service', 'collision', 'auto center', 'collision center', 'auto body', 'automotive', 'auto repair'],
    'bank': ['bank', 'credit union', 'financial', 'atm'],
    'food': ['burger', 'taco', 'mexican', 'bar', 'grill', 'grille', 'pizza', 'pizzeria', 'food', 'cafe', 'café', 'restaurant', 'panera bread', 'smokehouse'],
    'church': ['church', 'faith', 'chapel', 'worship'],
    'care': ['care', 'assisted living', 'nursing home', 'senior center'],
    'shop': ['shop', 'store', 'market'],
    'store': ['shop', 'store', 'market', 'outlet', 'complex', 'plaza', 'staples', 'gamestop', 'cvs pharmacy', 'gas'],
    'market': ['shop', 'store', 'market', 'mart'],
    'school': ['school', 'high school', 'middle school', 'elementary', 'academy'],
    'hotel': ['hotel', 'motel', 'inn', 'stay'],
    'walmart': ['walmart', 'wal-mart'],
    'hospital': ['hospital', 'clinic', 'medical center', 'healthcare', 'surgery', 'surgical'],
    'group home': ['senior center', 'group home'],
    'chains': ['staples', 'gamestop', 'cvs', 'jc penney', 'planet fitness', 'post office', 'library', 'town hall', 'panera bread']
}

# Predict system types for the dataset
y_pred_probs = model.predict_proba(X_data)

# Initialize lists to hold the predictions and confidence scores
predicted_system_types = []
confidence_scores = []

# Set prediction thresholds
general_threshold = 0.28
fire_sprinkler_threshold = 0.48

for i, probs in enumerate(y_pred_probs):
    predicted_types = set()
    confidence = []

    # Extract the business name for keyword matching
    business_name = data['Business Name'].iloc[i].lower()

    # Stage 1: Apply keyword rules
    for category, systems in keyword_rules.items():
        variations = keyword_variations.get(category, [])
        if any(keyword in business_name for keyword in variations):
            for system_type in systems:
                if system_type not in predicted_types:
                    predicted_types.add(system_type)
                    confidence.append(f"{system_type}: Rule-based")

    # Ensure Commercial Hood Suppression is added if Commercial Hood Cleaning is present
    if 'Commercial Hood Cleaning' in predicted_types:
        predicted_types.add('Commercial Hood Suppression')
        confidence.append("Commercial Hood Suppression: Added due to presence of Commercial Hood Cleaning")

    # Stage 2: Apply model predictions, but only add new types
    for idx, prob in enumerate(probs):
        system_type = label_encoder.inverse_transform([idx])[0]
        threshold = fire_sprinkler_threshold if system_type == 'Fire Sprinkler' else general_threshold

        if prob >= threshold:
            predicted_types.add(system_type)
            confidence.append(f"{system_type}: {prob:.2f}")

    # Convert the set back to a list to preserve order
    unique_predicted_types = list(predicted_types)

    # Join the system types with commas
    refined_prediction_str = ','.join(unique_predicted_types)

    if refined_prediction_str:
        predicted_system_types.append(refined_prediction_str)
        confidence_scores.append(', '.join(confidence))
    else:
        predicted_system_types.append('None')  # No prediction if no system type passes the threshold
        confidence_scores.append('Low confidence - No system type added')

# Add the predictions and confidence scores to the dataset
data['Predicted System Type'] = predicted_system_types
data['Confidence Score'] = confidence_scores

# Save the predictions to a new Excel file
output_file_path = 'output_predictions.xlsx'  # Replace with the generic output file name
data.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"Predicted system types saved to '{output_file_path}'")
