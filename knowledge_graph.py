import spacy
import networkx as nx
from pyvis.network import Network
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

class KnowledgeGraph:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.knowledge_graph = nx.Graph()
        self.client = OpenAI(api_key=os.environ.get("API_KEY"))

    def extract_keywords(self, paragraph):
        doc = self.nlp(paragraph.lower())  # Convert paragraph to lowercase
        keywords = [
            token.lemma_ for token in doc
            if not token.is_stop and token.is_alpha and len(token.text) > 1
        ]
        print(keywords)
        return keywords

    def extract_relationships(self, keywords):
        relationships = []
        for i, keyword1 in enumerate(keywords):
            for j, keyword2 in enumerate(keywords):
                if i != j:
                    doc1 = self.nlp(keyword1)
                    doc2 = self.nlp(keyword2)

                    # Check if both docs have vectors and are not empty
                    if doc1.vector_norm and doc2.vector_norm:
                        similarity = doc1.similarity(doc2)
                        if similarity > 0.6:  # Adjust the threshold as needed
                            relationships.append((keyword1, keyword2))
                    else:
                        # Handle words without vectors
                        # For instance, you can skip, set low similarity, or handle differently
                        pass  # Here, we're skipping words without vectors

        return relationships

    def build_knowledge_graph(self, paragraph):
        keywords = self.extract_keywords(paragraph)
        relationships = self.extract_relationships(keywords)

        # Add or update edges with weights, avoiding self-loops
        for source, target in relationships:
            if source != target:
                if self.knowledge_graph.has_edge(source, target):
                    edge_data = self.knowledge_graph[source][target]
                    if 'weight' in edge_data:
                        edge_data['weight'] += 1
                    else:
                        # Assign initial weight if not present
                        edge_data['weight'] = 1
                else:
                    self.knowledge_graph.add_edge(source, target, weight=1)  # Use 1 as initial weight

        # Remove isolated nodes
        isolated_nodes = list(nx.isolates(self.knowledge_graph))
        self.knowledge_graph.remove_nodes_from(isolated_nodes)

    def generate_knowledge_graph_html(self, question):
        # Use OpenAI ChatGPT API to generate a paragraph based on the question
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "Act like a knowledgeable and friendly Bot. Explain key concepts and make sure you have sources but don't cite them. Make sure to cover the main ideas in short sentences. Reply should be straight to the point in less than 50 words."},
                {"role": "user", "content": f"{question}"}
            ]
        )

        paragraph = response.choices[0].message.content.strip()
        print("Generated paragraph:", paragraph)

        # Build the knowledge graph
        self.build_knowledge_graph(paragraph)

        # Create a PyVis Network instance for visualization
        pyvis_graph = Network(notebook=False)
        pyvis_graph.from_nx(self.knowledge_graph)

        # Generate HTML to display the graph
        pyvis_graph.set_edge_smooth('dynamic')

        print("html sent")
        # Return the HTML content of the graph
        return pyvis_graph.generate_html(name='knowledge_graph.html', notebook=False),paragraph
