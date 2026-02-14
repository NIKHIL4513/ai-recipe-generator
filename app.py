import streamlit as st
from openai import OpenAI
import os
import re

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽️", layout="wide")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("""
<style>
body {
    background-color: #1e1e1e;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
.header {
    text-align:center;
    font-size:36px;
    color:#ffd166;
    margin:0;
}
.subheader {
    text-align:center;
    font-size:16px;
    color:#fff;
    margin:0 0 5px 0;
}
.input-card {
    background-color:#2a2d37;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.4);
    margin-bottom:0;
    width:95%;
    margin-left:auto;
    margin-right:auto;
}
.recipe-card {
    background-color:#2a2d37;
    border-radius:15px;
    padding:15px;
    width:95%;
    margin:auto;
    box-shadow:0px 8px 25px rgba(0,0,0,0.6);
}
.section {
    padding:10px;
    border-radius:10px;
    margin-bottom:5px;
}
.ingredients-section {
    background-color:#3b3f4c;
}
.instructions-section {
    background-color:#3b3f4c;
}
.section-title {
    color:#ffd166;
    text-align:center;
    font-size:18px;
    margin:0 0 5px 0;
}
ul, ol {
    padding-left:20px;
    line-height:1.5;
    margin:0;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<div class='header'>🍳 AI Recipe Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Enter ingredients and select cuisine to get your recipe</div>", unsafe_allow_html=True)


st.markdown("<div class='input-card'>", unsafe_allow_html=True)
ingredients_input = st.text_area("🥕 Enter ingredients (comma-separated):", placeholder="e.g., rice, chicken, onion, egg")
cuisine = st.selectbox("🌍 Select cuisine (optional):", ["Any", "Indian", "Chinese", "Italian", "Mexican", "Continental"])
generate = st.button("✨ Generate Recipe")
st.markdown("</div>", unsafe_allow_html=True)


if generate:
    if ingredients_input.strip() == "":
        st.warning("⚠️ Please enter at least one ingredient.")
    else:
        with st.spinner("👩‍🍳 Generating your recipe..."):
            try:
                prompt = f"""You are a professional chef. Create a recipe using these ingredients:
{ingredients_input}

Cuisine: {cuisine if cuisine != 'Any' else ''}

Return in EXACT format:

TITLE: <recipe name>

INGREDIENTS:
- item

INSTRUCTIONS:
1. step
"""
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional chef."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                recipe_text = response.choices[0].message.content

              
                title = ""
                ingredients = []
                instructions = []
                section = None
                for line in recipe_text.split("\n"):
                    line = line.strip()
                    if line.startswith("TITLE:"):
                        title = line.replace("TITLE:", "").strip()
                    elif line.startswith("INGREDIENTS"):
                        section = "ingredients"
                    elif line.startswith("INSTRUCTIONS"):
                        section = "instructions"
                    elif section == "ingredients" and (line.startswith("-") or line):
                        ingredients.append(line.lstrip("-").strip())
                    elif section == "instructions" and re.match(r'^\d+[\.\)]', line):
                        instructions.append(line)

                st.success("✅ Recipe Generated Successfully!")

                
                st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center; color:#ffd166;'>{title}</h2>", unsafe_allow_html=True)

                col1, col2 = st.columns([1,1])

                with col1:
                    st.markdown("<div class='section ingredients-section'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-title'>🧺 Ingredients</div>", unsafe_allow_html=True)
                    st.markdown("<ul>", unsafe_allow_html=True)
                    for item in ingredients:
                        st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
                    st.markdown("</ul>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='section instructions-section'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-title'>👨‍🍳 Instructions</div>", unsafe_allow_html=True)
                    st.markdown("<ol>", unsafe_allow_html=True)
                    for step in instructions:
                        st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                    st.markdown("</ol>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ Error generating recipe. Please try again.")
                st.code(str(e))
