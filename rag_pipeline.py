"""RAG Pipeline Stub for VANE-SPACE-SLA v2.0

This module provides a deterministic, testable RAG orchestration stub that:
- retrieves documents from a simulated vector store (using provided contexts)
- builds a grounded prompt using StrictPromptBuilder
- performs a deterministic LLM inference stub (no external API calls)
- computes a simple grounding score based on lexical overlap

All configuration is read from env vars (see .env.example)."""

import logging
import random
import time
from typing import List, Dict, Any, Optional

from strict_prompt_builder import StrictPromptBuilder
from config import Config

logger = logging.getLogger("rag_pipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")


class RAGPipeline:
    def __init__(self, embedding_model: Optional[str] = None, llm_model: Optional[str] = None):
        self.embedding_model = embedding_model or Config.EMBEDDING_MODEL
        self.llm_model = llm_model or Config.LLM_MODEL

    def _retrieve_documents(self, contexts: List[str], top_k: int = 3) -> List[Dict[str, Any]]:
        """Simulated retrieval: returns the first top_k context blocks as "documents".
        Each doc is a dict with id and content and a mock score.
        """
        docs = []
        for i, c in enumerate(contexts[:top_k]):
            docs.append({"id": f"doc_{i}", "content": c, "score": round(1.0 - (i * 0.05), 2)})
        logger.info(f"Retrieved {len(docs)} documents (simulated)")
        return docs

    def _llm_infer(self, prompt: str, seed: Optional[int] = None) -> str:
        """A deterministic stub for LLM inference. If the prompt contains the strict halt token,
        return the HALT token. Otherwise return a synthetic answer that echoes the user query
        and mentions how many context blocks were seen.
        """
        if seed is not None:
            random.seed(seed)

        if "[HALT_HALLUCINATION_DETECTED" in prompt:
            return "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]"

        # Try to extract USER QUERY line
        user_line = "USER QUERY:"
        user_query = None
        for line in prompt.splitlines():
            if line.strip().startswith(user_line):
                user_query = line.split(user_line, 1)[1].strip()
                break

        if not user_query:
            user_query = "(no user query provided)"

        # Create a short deterministic response using seed
        tokens = [w for w in user_query.split() if len(w) > 3]
        sample_token = tokens[0] if tokens else "result"
        rnd = random.Random(seed)
        qualifier = rnd.choice(["According to the verified context", "Based on the provided baseline", "From the audited documents"]) if seed is not None else "According to the verified context"

        response = f"{qualifier}, the answer to '{user_query}' is: {sample_token} (simulated)."
        return response

    def _compute_grounding_score(self, model_response: str, contexts: List[str]) -> float:
        """Compute a simple lexical overlap score between response and contexts."
        if not contexts:
            return 0.0

        resp_tokens = set([t.lower() for t in model_response.split() if len(t) > 3])
        total_overlap = 0
        for c in contexts:
            ctx_tokens = set([t.lower() for t in c.split() if len(t) > 3])
            total_overlap += len(resp_tokens.intersection(ctx_tokens))

        # Normalize by number of contexts and a small constant to keep in [0,1]
        score = min(1.0, total_overlap / (len(contexts) * 10 + 1e-6))
        return round(score, 3)

    def run_rag_cycle(self, user_query: str, contexts: Optional[List[str]] = None,
                      grounding_strength: str = "strict", top_k: int = 3, seed: Optional[int] = None) -> Dict[str, Any]:
        """Run one RAG cycle and return structured outputs suitable for tests and demo.

        Returns keys: retrieved_docs, prompt, model_response, grounding_score, metadata
        """
        if contexts is None:
            contexts = []

        if seed is not None:
            random.seed(seed)

        retrieved = self._retrieve_documents(contexts, top_k=top_k)

        builder = StrictPromptBuilder(model_id=self.llm_model, grounding_strength=grounding_strength)
        prompt_obj = builder.build_grounded_prompt(user_query, [d["content"] for d in retrieved])
        prompt_text = prompt_obj["prompt"]

        # If strict and no contexts, enforce HALT
        if grounding_strength == "strict" and len(retrieved) == 0:
            model_response = "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]"
        else:
            model_response = self._llm_infer(prompt_text, seed=seed)

        grounding_score = self._compute_grounding_score(model_response, [d["content"] for d in retrieved])

        # Determine grounding label
        if grounding_score >= Config.CONFIDENCE_HIGH_THRESHOLD:
            grounding_label = "HIGH_CONFIDENCE_GROUNDED"
        elif grounding_score >= Config.CONFIDENCE_MEDIUM_THRESHOLD:
            grounding_label = "MEDIUM_CONFIDENCE_GROUNDED"
        else:
            grounding_label = "LOW_CONFIDENCE_OR_HALLUCINATORY"

        metadata = {
            "model": self.llm_model,
            "embedding_model": self.embedding_model,
            "grounding_strength": grounding_strength,
            "retrieved_count": len(retrieved),
            "timestamp": time.time(),
            "grounding_label": grounding_label
        }

        logger.info(f"RAG cycle completed — grounding_label={grounding_label} score={grounding_score}")

        return {
            "retrieved_docs": retrieved,
            "prompt": prompt_text,
            "model_response": model_response,
            "grounding_score": grounding_score,
            "metadata": metadata
        }


# Simple module-level function for convenience
_default_pipeline = RAGPipeline()

def run_rag_cycle(user_query: str, contexts: Optional[List[str]] = None, grounding_strength: str = "strict",
                  top_k: int = 3, seed: Optional[int] = None) -> Dict[str, Any]:
    return _default_pipeline.run_rag_cycle(user_query, contexts, grounding_strength, top_k, seed)
