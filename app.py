import streamlit as st
import requests
import pandas as pd


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Secure AI Privacy Gateway",
    page_icon="🛡",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.title("🛡 Secure AI Privacy Gateway")

st.markdown("""
Privacy-first AI assistant that masks sensitive
information before sending prompts to LLMs.
""")


# =====================================================
# MODE SELECTION
# =====================================================

mode = st.selectbox(
    "Select Service",
    [
        "Data Masking Service",
        "Secure AI Assistant"
    ]
)


# =====================================================
# MODE 1 — DATA MASKING SERVICE
# =====================================================

if mode == "Data Masking Service":

    st.subheader("📁 Sensitive Data Masking")

    col1, col2 = st.columns(2)

    with col1:

        uploaded_file = st.file_uploader(
            "Upload File",
            type=["txt", "csv", "pdf"]
        )

        user_input = ""

        if uploaded_file is not None:

            if uploaded_file.type == "text/plain":

                user_input = str(
                    uploaded_file.read(),
                    "utf-8"
                )

            elif uploaded_file.type == "text/csv":

                df = pd.read_csv(uploaded_file)

                user_input = df.to_string()

            elif uploaded_file.type == "application/pdf":

                user_input = (
                    "PDF uploaded successfully."
                )

        user_input = st.text_area(
            "Enter Sensitive Text",
            value=user_input,
            height=300,
            placeholder="Paste sensitive data here..."
        )

        mask_button = st.button(
            "🔒 Mask Data"
        )

    if mask_button:

        payload = {
            "text": user_input
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/hybrid-mask-and-send",
                json=payload
            )

            data = response.json()

        except Exception as e:

            st.error("Backend Error")

            st.code(str(e))

            st.stop()

        with col2:

            st.success(
                "Masking Completed Successfully"
            )

            st.subheader("🔐 Masked Output")

            st.code(
                data.get("masked_text", ""),
                language="text"
            )

            audit_data = data.get(
                "masked_entities",
                []
            )

            regex_count = len([
                x for x in audit_data
                if x["method"] == "REGEX"
            ])

            ner_count = len([
                x for x in audit_data
                if x["method"] in ["NER", "CUSTOM_REGEX"]
            ])

            total_entities = len(audit_data)

            st.subheader(
                "📊 Privacy Dashboard"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Protected Fields",
                total_entities
            )

            c2.metric(
                "Regex Matches",
                regex_count
            )

            c3.metric(
                "NER Matches",
                ner_count
            )

            st.subheader(
                "📋 Transparency Panel"
            )

            audit_df = pd.DataFrame(
                audit_data
            )

            st.dataframe(
                audit_df,
                use_container_width=True
            )

            st.download_button(
                label="⬇ Download Masked Text",
                data=data.get(
                    "masked_text",
                    ""
                ),
                file_name="masked_output.txt",
                mime="text/plain"
            )


# =====================================================
# MODE 2 — SECURE AI ASSISTANT
# =====================================================

elif mode == "Secure AI Assistant":

    st.subheader(
        "🤖 Privacy-Safe AI Assistant"
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    with st.sidebar:

        st.header("⚙ Assistant Controls")

        uploaded_pdf = st.file_uploader(
            "Upload PDF (Optional)",
            type=["pdf"]
        )

        if uploaded_pdf is not None:

            files = {
                "file": uploaded_pdf
            }

            try:

                upload_response = requests.post(
                    "http://127.0.0.1:8000/upload-document",
                    files=files
                )

                if upload_response.status_code == 200:

                    st.success(
                        "PDF uploaded successfully"
                    )

                else:

                    st.error(
                        "PDF upload failed"
                    )

            except Exception as e:

                st.error(str(e))

        if st.button("🗑 Clear Chat"):

            st.session_state.messages = []

            st.rerun()

    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask anything securely..."
    )

    # =====================================================
    # USER MESSAGE
    # =====================================================

    if prompt:

        st.session_state.messages.append({

            "role": "user",

            "content": prompt
        })

        with st.chat_message("user"):

            st.markdown(prompt)

        payload = {
            "text": prompt
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/secure-ai-chat",
                json=payload
            )

            data = response.json()

        except Exception as e:

            st.error("Cannot connect to backend")

            st.code(str(e))

            st.stop()

        assistant_response = data.get(
            "final_response",
            "No response generated."
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                assistant_response
            )

            with st.expander(
                "🔍 Privacy + Retrieval Details"
            ):

                st.subheader(
                    "Retrieved Context"
                )

                st.code(
                    data.get(
                        "retrieved_context",
                        ""
                    ),
                    language="text"
                )

                st.subheader(
                    "Masked Prompt"
                )

                st.code(
                    data.get(
                        "masked_prompt",
                        ""
                    ),
                    language="text"
                )

                st.subheader(
                    "Transparency Panel"
                )

                audit_df = pd.DataFrame(
                    data.get(
                        "masked_entities",
                        []
                    )
                )

                st.dataframe(
                    audit_df,
                    use_container_width=True
                )

        st.session_state.messages.append({

            "role": "assistant",

            "content": assistant_response
        })