from app.pipeline.rag_pipeline import RAGPipeline
from app.evaluation.benchmark import Benchmark


pipeline = RAGPipeline()

benchmark = Benchmark(
    pipeline,
)

results = benchmark.run()

summary = benchmark.summary(
    results,
)

print()

print("Benchmark Results")

print("-" * 60)

for result in results:

    print(result)

print()

print("Summary")

print("-" * 60)

for key, value in summary.items():

    print(f"{key}: {value:.4f}")


benchmark.save(

    results,

    summary,

    "benchmark_results.json",
)