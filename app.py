from flask import Flask, render_template, request, jsonify
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)

# Load a pre-trained model and tokenizer locally
generator = pipeline('text-generation', model='gpt2')

# Function to generate story using the local model
def generate_story_locally(prompt):
    try:
        generated_text = generator(f"Write a detailed story based on: {prompt}", max_length=500, num_return_sequences=1, temperature=0.8)[0]['generated_text']
        # Remove the prompt from the generated text
        return generated_text.replace(f"Write a detailed story based on: {prompt}", "", 1).strip()
    except Exception as e:
        print(f"Error during local story generation: {e}")
        return "Story generation failed locally."

# Route for the main page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the story generation request
@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()
    prompt = data['prompt']

    try:
        # Generate story with the local model
        story = generate_story_locally(prompt)
        return jsonify({"story": story})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)