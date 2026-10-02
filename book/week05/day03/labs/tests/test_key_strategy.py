from app.cache import build_llm_cache_key


def test_cache_key_is_stable_for_dict_order():
    payload_a = {"text": "Bonjour", "task": "classify"}
    payload_b = {"task": "classify", "text": "Bonjour"}

    key_a = build_llm_cache_key("ai-api", "dev", "demo-llm", "v1", payload_a)
    key_b = build_llm_cache_key("ai-api", "dev", "demo-llm", "v1", payload_b)

    assert key_a == key_b


def test_cache_key_contains_model_and_prompt_version():
    key = build_llm_cache_key(
        "ai-api",
        "dev",
        "demo-llm",
        "v1",
        {"message": "hello"},
    )

    assert "demo-llm" in key
    assert "v1" in key
    assert key.startswith("ai-api:dev:cache:llm:")
