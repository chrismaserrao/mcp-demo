from fastmcp import FastMCP

mcp = FastMCP("Psychology-Assistant")

DISTORTIONS = {
    "catastrophizing": "Believing that what has happened or will happen will be so awful and unbearable that you won't be able to stand it.",
    "all_or_nothing": "Viewing a situation in only two categories instead of on a continuum (e.g., 'If I'm not perfect, I'm a failure').",
    "emotional_reasoning": "Reasoning from how you feel ('I feel like an idiot, so I must be one')."
}

@mcp.tool()
def analyze_thought_pattern(thought_text: str) -> str:
    """
    Analyzes a user's thought for common cognitive distortions.
    Returns the likely distortion type and a confidence score.
    """
    thought_lower = thought_text.lower()
    

    if "always" in thought_lower or "never" in thought_lower:
        return "Detected: All-or-Nothing Thinking. (Confidence: High)"
    elif "disaster" in thought_lower or "awful" in thought_lower or "worst" in thought_lower:
        return "Detected: Catastrophizing. (Confidence: High)"
    elif "feel" in thought_lower and "must" in thought_lower:
        return "Detected: Emotional Reasoning. (Confidence: Medium)"
    else:
        return "No specific cognitive distortion detected with high confidence."

@mcp.tool()
def get_coping_strategy(distortion_type: str) -> str:
    """
    Provides a CBT-based coping strategy for a specific distortion type.
    Input should be one of: 'catastrophizing', 'all_or_nothing', 'emotional_reasoning'.
    """
    key = distortion_type.lower()
    if "catastrophizing" in key:
        return "Strategy: 'Decatastrophizing'. Ask yourself: 'What is the worst that could happen? How likely is it? Can I survive it?'"
    elif "all_or_nothing" in key:
        return "Strategy: 'Shades of Gray'. Try to evaluate things on a scale of 0-100 rather than pass/fail."
    elif "emotional_reasoning" in key:
        return "Strategy: 'Feelings are not Facts'. Treat your emotion as a hypothesis to be tested, not the truth."
    else:
        return "Strategy: Mindfulness. Observe the thought without judgment and let it pass."
    

@mcp.tool()
def get_medical_disclaimer() -> str:
    """
    Provides a mandatory medical and psychological disclaimer.
    This tool should be called at the start of any new session or when 
    providing specific CBT strategies.
    """
    return (
        "IMPORTANT: This Psychology Assistant is an AI tool designed for educational "
        "and self-reflection purposes only. It is NOT a substitute for professional "
        "medical advice, diagnosis, or treatment. If you are in a crisis or "
        "experiencing an emergency, please contact your local emergency services "
        "or a crisis hotline immediately."
    )


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )