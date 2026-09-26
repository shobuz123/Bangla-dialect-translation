import sys
sys.stdout.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dialect-translator")
_translator = None

def get_translator():
    global _translator
    if _translator is None:
        import translator
        translator.load_all()
        _translator = translator
    return _translator


@mcp.tool()
def translate_dialect(text: str, direction: str = "dialect", dialect: str = "sylheti") -> dict:
    """বাংলা উপভাষা অনুবাদ করে, RAG দিয়ে ভুল সংশোধন সহ।

    Args:
        text: অনুবাদের জন্য বাংলা বাক্য
        direction: 'dialect' (standard->dialect) বা 'standard' (dialect->standard)
        dialect: sylheti, chittagonian, mymensingh, বা noakhali
    """
    t = get_translator()
    result = t.translate(text, direction=direction, dialect=dialect, model_choice="nllb")
    return {
        "input": text,
        "dialect": dialect,
        "direction": direction,
        "model_output": result["model_output"],
        "final_translation": result["final"],
        "rag_corrected": result["rag_used"],
        "match_score": result["score"],
    }


@mcp.tool()
def list_dialects() -> list:
    """সমর্থিত সব উপভাষার তালিকা দেয়।"""
    return ["sylheti", "chittagonian", "mymensingh", "noakhali"]


if __name__ == "__main__":
    mcp.run()