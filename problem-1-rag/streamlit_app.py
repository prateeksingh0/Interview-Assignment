import streamlit as st
from pathlib import Path

from app.ingestion.loader import DocumentLoader
from app.chunking.chunker import TextChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.lancedb_store import LanceDBStore
from app.pipeline.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="Cost-Efficient RAG",
    page_icon="📚",
    layout="wide",
)

if "indexed" not in st.session_state:
    st.session_state["indexed"] = False

if "document_name" not in st.session_state:
    st.session_state["document_name"] = None

if "pipeline" not in st.session_state:
    st.session_state["pipeline"] = None

if "embedder" not in st.session_state:
    st.session_state["embedder"] = None

if "num_chunks" not in st.session_state:
    st.session_state["num_chunks"] = 0

if "ingest_result" not in st.session_state:
    st.session_state["ingest_result"] = None

st.title("📚 Cost-Efficient RAG Application")
st.caption("Applied AI/ML Engineering Assignment — Problem 1")


uploaded_file = st.file_uploader(
    "Upload Document",
    type=[
        "pdf",
        "html",
        "htm",
        "md",
    ],
)


UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

if uploaded_file is not None:

    file_path = (
        UPLOAD_DIR /
        uploaded_file.name
    )

    with open(
        file_path,
        "wb",
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

debug = st.sidebar.checkbox(
    "Debug Mode",
    value=False,
)

# -------------------------------------------------
# Ingestion
# -------------------------------------------------
def initialize_pipeline(file_path: str):

    loader = DocumentLoader()

    document = loader.load(file_path)

    chunker = TextChunker()

    chunks = chunker.chunk(document)

    embedder = Embedder()

    embeddings = embedder.embed_chunks(chunks)

    store = LanceDBStore()

    pipeline = RAGPipeline()

    ingest_result = store.ingest(
        embeddings,
        embedder.model_name,
        embedder.dimension,
    )

    return (
        pipeline,
        embedder,
        len(chunks),
        ingest_result,
    )

if uploaded_file:

    if st.button("Index Document"):

        pipeline, embedder, num_chunks, ingest_result = (
            initialize_pipeline(str(file_path))
        )

        st.session_state["indexed"] = True

        st.session_state["pipeline"] = pipeline

        st.session_state["embedder"] = embedder

        st.session_state["num_chunks"] = num_chunks

        st.session_state["ingest_result"] = ingest_result

        st.session_state["document_name"] = uploaded_file.name


st.sidebar.header("System Information")

if st.session_state["document_name"]:

    st.sidebar.write(
        f"**Document:** {st.session_state['document_name']}"
    )

else:

    st.sidebar.write(
        "**Document:** None"
    )

if st.session_state["embedder"]:

    st.sidebar.write(
        f"**Embedding Model:** {st.session_state['embedder'].model_name}"
    )

    st.sidebar.write(
        f"**Dimension:** {st.session_state['embedder'].dimension}"
    )

else:

    st.sidebar.write(
        "**Embedding Model:** -"
    )

    st.sidebar.write(
        "**Dimension:** -"
    )

st.sidebar.write(
    "**Vector DB:** LanceDB"
)

st.sidebar.divider()

st.sidebar.header("Database")

if st.session_state["ingest_result"]:

    ingest = st.session_state["ingest_result"]

    st.sidebar.metric(
        "Inserted",
        ingest["inserted"],
    )

    st.sidebar.metric(
        "Skipped",
        ingest["skipped"],
    )

    st.sidebar.metric(
        "Total",
        ingest["total"],
    )

if st.session_state.get("indexed", False):
    question = st.text_input(
        "Ask a question",
        placeholder="Ask anything about the uploaded document..."
    )

    if st.button("Ask"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            st.stop()

        with st.spinner(
            "Generating answer..."
        ):

            result = st.session_state["pipeline"].ask(question)

            runtime = result["runtime_metrics"]

            evaluation = result["evaluation_metrics"]

        st.subheader("💬 Answer")

        st.markdown(result["answer"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Latency",
                f"{result['latency']:.2f} s",
            )

        with col2:
            st.metric(
                "Retrieved Chunks",
                len(result["chunks"]),
            )

        with col3:
            st.metric(
                "Embedding Dimension",
                st.session_state["embedder"].dimension,
            )
        
        st.subheader("📊 Runtime Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Avg Similarity",
                f"{runtime['avg_similarity']:.3f}",
            )

            st.metric(
                "Highest",
                f"{runtime['highest_similarity']:.3f}",
            )

        with col2:

            st.metric(
                "Lowest",
                f"{runtime['lowest_similarity']:.3f}",
            )

            st.metric(
                "Context Length",
                f"{runtime['context_length']} chars",
            )

        with col3:

            st.metric(
                "Answer Length",
                f"{runtime['answer_length']} words",
            )

        st.subheader("📈 Evaluation Metrics")

        if evaluation:
            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Recall@k",
                    f"{evaluation['recall']:.2f}",
                )

                st.metric(
                    "Precision@k",
                    f"{evaluation['precision']:.2f}",
                )

            with col2:

                st.metric(
                    "MRR",
                    f"{evaluation['mrr']:.2f}",
                )

                st.metric(
                    "nDCG",
                    f"{evaluation['ndcg']:.2f}",
                )

            with col3:

                st.metric(
                    "Faithfulness",
                    f"{evaluation['faithfulness']:.2f}",
                )

                st.metric(
                    "Answer Relevance",
                    f"{evaluation['answer_relevance']:.2f}",
                )

            st.metric(
                "Context Precision",
                f"{evaluation['context_precision']:.2f}",
            )

            with st.expander(
                "Expected Answer"
            ):

                st.text(
                    evaluation["expected_answer"]
                )

        st.subheader("📚 Supporting Chunks")

        for chunk in result["chunks"]:

            with st.expander(chunk.citation):

                st.caption(
                    f"Source: {chunk.metadata['source']}"
                )

                st.write(chunk.text)

        if debug:

            with st.expander(
                "Generated Context"
            ):

                st.text(
                    result["context"]
                )

            with st.expander(
                "Generated Prompt"
            ):

                st.text(
                    result["prompt"]
                )

    else:
        st.info(
            "Upload a document and click 'Index Document' first."
        )
