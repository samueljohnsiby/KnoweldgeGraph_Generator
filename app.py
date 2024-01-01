from flask import Flask, render_template, request, jsonify
from knowledge_graph import KnowledgeGraph  # Import the KnowledgeGraph class

app = Flask(__name__)

# Initialize a global instance of KnowledgeGraph
knowledge_graph_instance = KnowledgeGraph()

# Serve the HTML file containing the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive user questions and send a response
@app.route('/ask', methods=['POST'])
def handle_question():
    user_question = request.json.get('question')

    # Process the question and generate updated graph HTML using the global knowledge_graph_instance
    graph_html,graph_paragraph = knowledge_graph_instance.generate_knowledge_graph_html(user_question)

    print("reached here")
    # Return the updated graph HTML to the frontend
    return jsonify({'graph_html': graph_html, 'paragraph': graph_paragraph})

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask a
