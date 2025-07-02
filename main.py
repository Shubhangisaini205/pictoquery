import streamlit as st
import base64
import openai
from PIL import Image

# Set your OpenAI API key
openai.api_key =  st.secrets["OPEN_API_KEY"]  # Replace with a secure way in production

st.title("🧠 Image-Based Q&A with GPT-4")

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Text prompt
user_input = st.text_area("💬 Enter your question for GPT-4", height=100)

# Button to submit
if st.button("🔍 Analyze Image and Answer"):

    if uploaded_file is None or not user_input.strip():
        st.warning("Please upload an image and enter a question.")
    else:
        # Encode image as base64
        base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")

        # Show image preview
        st.image(uploaded_file, caption="Uploaded Image")

        # Create prompt
        image_prompt = f'''
        I have uploaded an image. Based on the image please answer this question:
        {user_input}
        Be detailed and show any calculations or reasoning steps if required.
        '''

        # Send to OpenAI
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": image_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                )

                st.success("✅ Response from GPT-4")
                st.markdown(response.choices[0].message["content"])

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
