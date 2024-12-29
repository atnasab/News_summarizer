from transformers import pipeline

# Initialize Hugging Face summarizer
summarizer = pipeline("summarization")

def summarize_text(text):
    if not text:
        return "No content available."
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
