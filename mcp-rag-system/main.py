import streamlit as st
import os
import time
import mcp


# --- Page Configuration ---
st.set_page_config(
    page_title="Agentic RAG System",
    page_icon="🤖",
    layout="wide",
)

# --- Styling ---
st.markdown("""
<style>
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .st-emotion-cache-1y4p8pa {
        padding-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Main Application ---
st.title("🤖 MCP-Powered Agentic RAG System")
st.caption("A Streamlit application demonstrating a RAG system using Firecrawl, Agno, and Milvus via MCP.")


# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
if "firecrawl_api_key" not in st.session_state:
    st.session_state.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "")

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.session_state.openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.openai_api_key,
        help="Get your key from https://platform.openai.com/api-keys"
    )
    st.session_state.firecrawl_api_key = st.text_input(
        "Firecrawl API Key",
        type="password",
        value=st.session_state.firecrawl_api_key,
        help="Get your key from https://firecrawl.dev"
    )
    st.divider()
    st.subheader("MCP Server Status")
    # In a real app, you would have logic to check server status
    st.success("Firecrawl MCP: Connected")
    st.success("Milvus RAG MCP: Connected")
    st.divider()
    st.info("This application is a demo. It does not persist data between sessions.")


# --- Main Content Tabs ---
tab1, tab2 = st.tabs(["📄 Documents Management", "💬 Chat with Agent"])

with tab1:
    st.header("Add Documents to the Knowledge Base")
    st.write("You can add documents by scraping a web page or uploading a text file.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌐 Scrape a Web Page")
        url_to_scrape = st.text_input("Enter URL to scrape:", "https://milvus.io/docs")
        if st.button("Scrape and Add"):
            if not st.session_state.firecrawl_api_key:
                st.error("Please enter your Firecrawl API Key in the sidebar.")
            elif not url_to_scrape:
                st.warning("Please enter a URL.")
            else:
                with st.spinner(f"Scraping {url_to_scrape}..."):
                    scraped_content = mcp.firecrawl.scrape(url_to_scrape)
                    time.sleep(2) # Simulate network call
                    scraped_content = f"This is the scraped content from {url_to_scrape}. It would be much longer in reality."
                    
                with st.spinner("Adding document to Milvus..."):
                    mcp.milvus_rag.add_documents(scraped_content)
                    time.sleep(1) # Simulate DB insertion
                    st.success(f"Successfully scraped and added content from URL.")
                    st.text_area("Scraped Content Preview", scraped_content, height=200)


    with col2:
        st.subheader("📤 Upload a File")
        uploaded_file = st.file_uploader("Choose a .txt or .md file", type=["txt", "md"])
        if uploaded_file is not None:
            if st.button("Upload and Add"):
                with st.spinner("Processing and adding file..."):
                    file_content = uploaded_file.getvalue().decode("utf-8")
                    # Placeholder for MCP call to milvus-rag
                    mcp.milvus_rag.add_documents(file_content)
                    time.sleep(1)
                    st.success(f"Successfully added file: {uploaded_file.name}")
                    st.text_area("File Content Preview", file_content, height=200)


with tab2:
    st.header("Chat with your RAG Agent")
    st.write("Ask questions about your documents or request a web search for up-to-date information.")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):
        if not st.session_state.openai_api_key:
            st.error("Please enter your OpenAI API Key in the sidebar to chat.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner("Thinking..."):
                    # Placeholder for Agno Agent logic
                    assistant_response = "I am a helpful assistant. This is a placeholder response."
                    
                    # Simulate streaming response
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if not st.session_state.openai_api_key or not st.session_state.firecrawl_api_key:
    st.warning("Please enter your API keys in the sidebar to use all features.", icon="⚠️")
