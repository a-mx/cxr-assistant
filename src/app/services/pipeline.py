from pathlib import Path
import time
from dataclasses import dataclass, field
from flask import current_app
from src.app.models.analysis import Analysis


@dataclass
class PipelineResult:
    report: str
    retrieved_cases: list[dict] = field(default_factory=list)
    bounding_boxes: list[dict] = field(default_factory=list)
    inference_time_ms: int = 0

def analyze(
    image_path: Path,
    lateral_image_path: Path | None,
    question: str,
    top_k: int,
    patient_id: int,
    strategy: str = "image_only",
) -> PipelineResult:
    if strategy == "image_only":
        return image_only(
            image_path,
            lateral_image_path,
            question,
            top_k,
            patient_id,
        )

    if strategy == "retrieval":
        return retrieval(
            image_path,
            lateral_image_path,
            question,
            top_k,
            patient_id,
        )

    raise ValueError(f"Unknown strategy: {strategy}")

def image_only(
        image_path: Path,
        lateral_image_path: Path | None,
        question: str,
        top_k: int,
        patient_id: int,
    )-> PipelineResult: 
    start = time.perf_counter()
    
    registry = current_app.extensions["model_registry"]
    results = []

    context = "None" 

    generated = registry.generator.generate(
        image_path,
        lateral_image=lateral_image_path,
        retrieved_context=context,
    )

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return PipelineResult(
        report=generated.report,
        bounding_boxes=generated.bounding_boxes,
        retrieved_cases=results,
        inference_time_ms=elapsed_ms,
    )


def retrieval(
    image_path: Path,
    lateral_image_path: Path | None,
    question: str,
    top_k: int,
    patient_id: int,
) -> PipelineResult:
    start = time.perf_counter()

    registry = current_app.extensions["model_registry"]

    histories = (
        Analysis.query
        .filter_by(patient_id=patient_id)
        .order_by(Analysis.created_at.desc())
        .limit(top_k)
        .all()
    )

    results = [
        {
            "analysis_id": analysis.id,
            "created_at": analysis.created_at.isoformat(),
            "report": analysis.current_report,
        }
        for analysis in histories
    ]

    if results:
        context = "\n\n".join(
            (
                f"Analysis date: {item['created_at']}\n"
                f"Report:\n{item['report']}"
            )
            for item in results
        )
    else:
        context = "No previous analyses for this patient."

    generated = registry.generator.generate(
        image_path,
        lateral_image=lateral_image_path,
        retrieved_context=context,
    )

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return PipelineResult(
        report=generated.report,
        bounding_boxes=generated.bounding_boxes,
        retrieved_cases=results,
        inference_time_ms=elapsed_ms,
    )