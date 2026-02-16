import pandas as pd
import os
from fastmcp import FastMCP

# Initialize with dependencies so Horizon installs them automatically
mcp = FastMCP("Psychology-Assistant", dependencies=["pandas"])

# --- Existing Psychology Tools ---

DISTORTIONS = {
    "catastrophizing": "Believing that what has happened or will happen will be so awful and unbearable that you won't be able to stand it.",
    "all_or_nothing": "Viewing a situation in only two categories instead of on a continuum (e.g., 'If I'm not perfect, I'm a failure').",
    "emotional_reasoning": "Reasoning from how you feel ('I feel like an idiot, so I must be one')."
}

@mcp.tool()
def analyze_thought_pattern(thought_text: str) -> str:
    """Analyzes a user's thought for common cognitive distortions."""
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
    """Provides a CBT-based coping strategy for a specific distortion type."""
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
    """Provides a mandatory medical and psychological disclaimer."""
    return (
        "IMPORTANT: This Psychology Assistant is an AI tool designed for educational "
        "and self-reflection purposes only. It is NOT a substitute for professional "
        "medical advice, diagnosis, or treatment."
    )

# --- New Financial Analysis Tool ---

@mcp.tool()
def analyze_transactions(query_type: str = "summary", user_id: str | None = None) -> str:
    """
    Reads the 'transactions.csv' file to provide financial insights.
    
    Args:
        query_type: 'summary' (stats by category) or 'raw' (returns last 10 rows).
        user_id: Optional. If provided, filters data for this specific User ID.
    """
    file_path = r"C:\Users\chris\OneDrive\Desktop\mcp-server\aug_personal_transactions_with_UserId.csv"
    
    if not os.path.exists(file_path):
        return "Error: 'transactions.csv' not found. Please upload the file."

    try:
        df = pd.read_csv(file_path)
        
        # Filter by User ID if provided
        if user_id:
            df = df[df['User ID'].astype(str) == str(user_id)]
            if df.empty:
                return f"No transactions found for User ID: {user_id}"

        # 1. Provide a quick Summary (Spending by Category)
        if query_type == "summary":
            # Convert Amount to numeric, forcing errors to NaN
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
            
            total_spent = df[df['Transaction Type'] == 'debit']['Amount'].sum()
            category_breakdown = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).to_markdown()
            
            return (
                f"### Financial Summary\n"
                f"**Total Debits:** ${total_spent:,.2f}\n\n"
                f"**Spending by Category:**\n{category_breakdown}"
            )

        # 2. Provide Raw Data (for the AI to analyze specific questions)
        else:
            # Return the most recent 10 transactions (assuming sorted by date, or just tail)
            return f"### Recent Transactions\n{df.tail(10).to_markdown(index=False)}"

    except Exception as e:
        return f"Error processing CSV: {str(e)}"

if __name__ == "__main__":
    mcp.run()