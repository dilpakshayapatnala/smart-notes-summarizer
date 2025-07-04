import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
from openai import OpenAI
import io

# === SET YOUR OPENAI API KEY HERE ===
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Replace with your actual API key

st.set_page_config(page_title="Smart Notes Summarizer", layout="centered")
st.title("📚 Smart Notes to Bullet Points")
st.write("Upload **text**, **PDF**, or **image** files to generate bullet-point summaries using AI.")

uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "png", "jpg", "jpeg"])

text_content = ""

if uploaded_file:
    file_type = uploaded_file.type

    if "text" in file_type:
        text_content = uploaded_file.read().decode("utf-8")

    elif "pdf" in file_type:
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
            text_content = "\n".join(pages)

    elif "image" in file_type:
        image = Image.open(uploaded_file)
        text_content = pytesseract.image_to_string(image)

    st.subheader("📄 Extracted Text:")
    st.text_area("Text", text_content, height=300)

    if text_content and st.button("🔍 Generate Summary"):
        with st.spinner("Summarizing..."):
            prompt = f"Summarize the following content into concise bullet points:\n\n{text_content}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            summary = response.choices[0].message.content

            st.subheader("✅ Bullet Point Summary")
            st.markdown(summary)

