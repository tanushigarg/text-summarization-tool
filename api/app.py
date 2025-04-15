from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import configure_retriever, configure_llm, configure_qa_chain

app = Flask(__name__)
CORS(app)

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        input_text = request.json.get("text", "")

        retriever = configure_retriever(input_text)
        llm = configure_llm()
        qa_chain = configure_qa_chain(retriever, llm)
        response = qa_chain.run(input_text)

        return jsonify({"summary": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)