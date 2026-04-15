import spacy.cli
try:
    spacy.cli.download("en_core_web_sm")
    print("Model downloaded successfully")
except Exception as e:
    print(f"Error: {e}")
