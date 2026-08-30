from strict_prompt_builder import StrictPromptBuilder

def test_strict_grounded_prompt_modes():
    builder = StrictPromptBuilder(model_id='demo-model', grounding_strength='strict')
    res = builder.build_grounded_prompt('What is the status?', ['ctx one'])
    assert 'prompt' in res
    assert 'metadata' in res
    assert res['metadata']['grounding_strength'] == 'strict'
    assert res['metadata']['context_block_count'] == 1

    builder.set_grounding_strength('moderate')
    res2 = builder.build_grounded_prompt('Test', ['a','b'])
    assert res2['metadata']['grounding_strength'] == 'moderate'
    assert res2['metadata']['context_block_count'] == 2

    builder.set_grounding_strength('soft')
    res3 = builder.build_grounded_prompt('Test', [])
    assert res3['metadata']['grounding_strength'] == 'soft'
    assert res3['metadata']['context_block_count'] == 0

    # invalid
    try:
        builder.set_grounding_strength('invalid')
        assert False
    except ValueError:
        assert True
