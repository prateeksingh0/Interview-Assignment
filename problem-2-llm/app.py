import os
import tempfile
import streamlit as st

from services.loader import TestSuiteLoader
from services.evaluator import EvaluationPipeline
from services.metrics import MetricsCalculator
from services.bias.manager import BiasManager
from services.validator import JudgeValidator
from services.reporter import ReportGenerator


st.set_page_config(
    page_title="LLM Evaluation Framework",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 LLM Evaluation Framework")

st.caption(
    "Independent LLM Evaluation using Ollama"
)

with st.sidebar:

    st.header("Configuration")

    uploaded_file = st.file_uploader(
        "Upload Test Suite",
        type=["json", "yaml", "yml"],
    )

    generator_model = st.text_input(
        "Generator Model",
        value="llama3.1:8b",
    )

    judge_model = st.text_input(
        "Judge Model",
        value="qwen2.5:7b",
    )

    run_button = st.button(
        "▶ Run Evaluation",
        use_container_width=True,
    )


if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".json",
    ) as tmp:

        tmp.write(uploaded_file.getvalue())

        uploaded_path = tmp.name
else:

    uploaded_path = None

if run_button:

    os.environ["GENERATOR_MODEL"] = generator_model
    os.environ["JUDGE_MODEL"] = judge_model

    if uploaded_path is None:

        st.error("Please upload a test suite.")

        st.stop()

    with st.spinner("Running evaluation..."):

        progress = st.progress(0)

        status = st.empty()

        cases = TestSuiteLoader.load(uploaded_path)

        pipeline = EvaluationPipeline()

        evaluations = []

        total = len(cases)

        for index, case in enumerate(cases):

            status.text(
                f"Evaluating test case {index+1} of {total}"
            )

            evaluation = pipeline.evaluate(
                case,
                system_prompt_a="Answer in one sentence.",
                system_prompt_b="Answer in three sentences.",
            )

            evaluations.append(evaluation)

            progress.progress(
                (index + 1) / total
            )

        progress.empty()
        status.empty()

        metrics = MetricsCalculator.calculate(
            evaluations,
        )

        bias = BiasManager().run(
            evaluations,
        )

        validation = JudgeValidator().validate_suite(
            evaluations,
        )

        reporter = ReportGenerator()

        json_path = reporter.generate_json(
            evaluations,
            metrics,
            bias,
            validation,
        )

        csv_path = reporter.generate_csv(
            evaluations,
        )

        st.session_state["metrics"] = metrics
        st.session_state["bias"] = bias
        st.session_state["validation"] = validation
        st.session_state["evaluations"] = evaluations
        st.session_state["json_path"] = json_path
        st.session_state["csv_path"] = csv_path

    st.success(
            f"""
        ✅ Evaluation completed successfully!

        • Processed {len(evaluations)} test cases

        • Reports generated successfully

        • Dashboard updated
        """
    )

st.divider()

metrics = st.session_state.get("metrics")
validation = st.session_state.get("validation")

col1, col2, col3, col4 = st.columns(4)

if metrics and validation:

    with col1:
        st.metric(
            "Total Cases",
            metrics["summary"]["total_cases"],
        )

    with col2:
        st.metric(
            "Pass Rate",
            f'{metrics["summary"]["pass_rate"]}%',
        )

    with col3:
        st.metric(
            "Average Score",
            metrics["comparison"]["average_score_a"],
        )

    with col4:
        st.metric(
            "Reliability",
            f"{validation.average_consistency}%",
        )

else:

    with col1:
        st.metric("Total Cases", "-")

    with col2:
        st.metric("Pass Rate", "-")

    with col3:
        st.metric("Average Score", "-")

    with col4:
        st.metric("Reliability", "-")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Metrics",
        "🛡 Bias Analysis",
        "✅ Validation",
        "📄 Results",
        "💡 Recommendation",
    ]
)

with tab1:

    if metrics:

        st.subheader("📊 Evaluation Summary")

        summary = metrics["summary"]
        comparison = metrics["comparison"]

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### Summary")

            st.table(
                {
                    "Metric": [
                        "Total Cases",
                        "Pass Rate",
                    ],
                    "Value": [
                        summary["total_cases"],
                        f'{summary["pass_rate"]}%',
                    ],
                }
            )

        with c2:

            st.markdown("### Comparison")

            st.table(
                {
                    "Metric": [
                        "Wins A",
                        "Wins B",
                        "Ties",
                        "Average Score A",
                        "Average Score B",
                    ],
                    "Value": [
                        comparison["wins_a"],
                        comparison["wins_b"],
                        comparison["ties"],
                        comparison["average_score_a"],
                        comparison["average_score_b"],
                    ],
                }
            )

        st.markdown("### Criteria Scores")

        criteria = metrics["criteria"]

        rows = []

        for name, values in criteria.items():

            rows.append(
                {
                    "Criterion": name,
                    "Score A": values["average_score_a"],
                    "Score B": values["average_score_b"],
                }
            )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("Run an evaluation first.")

with tab2:

    bias = st.session_state.get("bias")

    if bias:

        st.subheader("🛡 Bias Analysis")

        c1, c2 = st.columns(2)

        with c1:

            st.success(
                f"Position Bias\n\nFlip Rate: {bias['position_bias']['flip_rate']}"
            )

            st.success(
                f"Verbosity Bias\n\nRate: {bias['verbosity_bias']['verbosity_bias_rate']}"
            )

            st.success(
                f"Self Enhancement\n\nRisk: {bias['self_enhancement_bias']['risk']}"
            )

        with c2:

            st.success(
                f"Sycophancy\n\nRate: {bias['sycophancy_bias']['sycophancy_rate']}"
            )

            clustering = bias["score_clustering"]["result"]

            status = (
                "Needs Review"
                if clustering["clustered"]
                else "Acceptable"
            )

            st.success(
                f"Score Clustering\n\n{status}"
            )

    else:

        st.info("Run an evaluation first.")

with tab3:

    if validation:

        st.subheader("✅ Judge Reliability")

        st.progress(
            validation.average_consistency / 100
        )

        st.metric(
            "Average Consistency",
            f"{validation.average_consistency}%",
        )

        st.metric(
            "Stable Cases",
            f"{validation.stable_cases}/{validation.total_cases}",
        )

        st.dataframe(
            [
                {
                    "Runs": result.total_runs,
                    "Consistency": result.consistency_rate,
                    "Stable": result.stable,
                }
                for result in validation.results
            ],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("Run an evaluation first.")

with tab4:

    evaluations = st.session_state.get(
        "evaluations"
    )

    if evaluations:

        for evaluation in evaluations:

            with st.expander(
                f"📄 Test Case {evaluation.test_case.id}",
                expanded=False,
            ):

                st.markdown("### Question")

                st.write(
                    evaluation.test_case.input
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Winner",
                    evaluation.verdict.winner,
                )

                c2.metric(
                    "Score A",
                    evaluation.verdict.overall_score_a,
                )

                c3.metric(
                    "Score B",
                    evaluation.verdict.overall_score_b,
                )

                with st.expander("Answer A"):

                    st.write(
                        evaluation.answer_a
                    )

                with st.expander("Answer B"):

                    st.write(
                        evaluation.answer_b
                    )

    else:

        st.info(
            "Run an evaluation first."
        )

if "json_path" in st.session_state:

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        with open(
            st.session_state["json_path"],
            "rb",
        ) as f:

            st.download_button(
                "📥 Download JSON Report",
                f,
                file_name="evaluation_report.json",
                use_container_width=True,
            )

    with c2:

        with open(
            st.session_state["csv_path"],
            "rb",
        ) as f:

            st.download_button(
                "📥 Download CSV Report",
                f,
                file_name="evaluation_report.csv",
                use_container_width=True,
            )

with tab5:

    bias = st.session_state.get("bias")
    validation = st.session_state.get("validation")

    if bias and validation:

        st.subheader("💡 Evaluation Recommendation")

        if validation.average_consistency >= 95:
            st.success("✅ Judge Reliability: Excellent")
        else:
            st.warning("⚠ Judge Reliability: Needs Review")

        if bias["position_bias"]["flip_rate"] == 0:
            st.success("🟢 Position Bias: Low")
        else:
            st.warning("🟡 Position Bias Detected")

        if bias["verbosity_bias"]["verbosity_bias_rate"] == 0:
            st.success("🟢 Verbosity Bias: Low")
        else:
            st.warning("🟡 Verbosity Bias Detected")

        st.success(
            f"🟢 Self Enhancement Risk: {bias['self_enhancement_bias']['risk']}"
        )

        if bias["sycophancy_bias"]["sycophancy_rate"] == 0:
            st.success("🟢 Sycophancy Bias: Low")
        else:
            st.warning("🟡 Sycophancy Bias Detected")

        clustering = bias["score_clustering"]["result"]

        if clustering["clustered"]:
            st.warning("🟡 Score Clustering Detected")
        else:
            st.success("🟢 Score Distribution is Healthy")

    else:

        st.info("Run an evaluation first.")

st.divider()

st.caption(
    "LLM Evaluation Framework • Built with Streamlit • Ollama • Pydantic"
)