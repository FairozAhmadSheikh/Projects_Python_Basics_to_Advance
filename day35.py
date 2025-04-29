import PyPDF2
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    max_chunk = 500  # tokenizer limit
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    
    summary = ''
    for chunk in chunks:
        res = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summary += res[0]['summary_text'] + ' '
    return summary.strip()
def main():
    pdf_path = input("📄 Enter path to your PDF file: ").strip()
    print("⏳ Extracting text...")
    text = extract_text_from_pdf(pdf_path)

    print("🧠 Summarizing content... This may take a moment.")
    summary = summarize_text(text)

    print("\n📝 Summary:")
    print("-" * 40)
    print(summary)
    print("-" * 40)

if __name__ == "__main__":
    main()