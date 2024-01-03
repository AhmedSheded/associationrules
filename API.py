from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load pre-trained association rules from the JSON file
with open('pretrained_rules_user_based.json', 'r') as file:
    pretrained_rules = json.load(file)


# Example function to generate user-based recommendations with chosen items
def generate_user_and_chosen_recommendations(user_id, chosen_items):
    recommendations = []

    # Filter rules based on user ID
    user_rules = [rule for rule in pretrained_rules if user_id in rule['antecedents']]

    # Combine user rules with chosen items
    combined_items = chosen_items + list(set([item for rule in user_rules for item in rule['consequents']]))

    # Generate recommendations based on combined items
    for rule in pretrained_rules:
        if any(item in rule['antecedents'] for item in combined_items):
            recommendations.extend(rule['consequents'])

    # Remove duplicates, chosen items, and items the user has already interacted with
    recommendations = list(set(recommendations))
    recommendations = [item for item in recommendations if item not in combined_items]

    return recommendations


# API endpoint for user-based recommendations with chosen items
@app.route('/get_user_and_chosen_recommendations', methods=['POST'])
def get_user_and_chosen_recommendations():
    # Get user ID and chosen items from the request
    data = request.get_json()
    user_id = data.get('user_id', None)
    chosen_items = data.get('chosen_items', [])

    if user_id is None:
        return jsonify({'error': 'User ID not specified in the request'}), 400

    # Generate user-based recommendations with chosen items for the specified user
    recommendations = generate_user_and_chosen_recommendations(user_id, chosen_items)

    # Return the recommendations as JSON
    response = {
        'user_id': user_id,
        'chosen_items': chosen_items,
        'user_and_chosen_recommendations': recommendations
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
