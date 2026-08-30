from rag_pipeline import run_rag_cycle


def test_rag_cycle_with_contexts():
    query = "Check server 01 status"
    contexts = [
        "Server 01: CPU 42.8% memory 68% status SECURE",
        "Server 02: CPU 12% memory 33% status IDLE"
    ]
    out = run_rag_cycle(query, contexts, grounding_strength='strict', top_k=2, seed=42)
    assert 'retrieved_docs' in out
    assert 'prompt' in out
    assert 'model_response' in out
    assert 'grounding_score' in out
    assert isinstance(out['grounding_score'], float)
    assert out['metadata']['retrieved_count'] == 2


def test_rag_cycle_strict_no_contexts_halts():
    out = run_rag_cycle('Do something', [], grounding_strength='strict', seed=1)
    assert out['model_response'].startswith('[HALT_HALLUCINATION_DETECTED')
    assert out['grounding_score'] == 0.0
