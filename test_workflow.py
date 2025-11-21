"""
Test script for The Daily AI workflow.
Run this to test the complete pipeline without the UI.
"""

from src.state import NewsState
from src.graph.workflow import news_workflow


def test_workflow(topic: str = "Latest developments in AI", 
                 format_type: str = "blog"):
    """
    Test the complete workflow with a sample topic.
    
    Args:
        topic: News topic to research
        format_type: Desired output format
    """
    print("=" * 80)
    print("THE DAILY AI - WORKFLOW TEST")
    print("=" * 80)
    print(f"\nTopic: {topic}")
    print(f"Format: {format_type}")
    print("\n" + "=" * 80 + "\n")
    
    # Create initial state
    initial_state = NewsState(
        topic=topic,
        format_type=format_type
    )
    
    # Run workflow
    print("🚀 Starting workflow...\n")
    
    final_state = None
    for state in news_workflow.stream(initial_state):
        # Get the latest state
        final_state = list(state.values())[0]
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80 + "\n")
    
    if final_state and final_state.generated_content:
        content = final_state.generated_content
        
        print(f"Title: {content.title}")
        print(f"Format: {content.format_type}")
        print(f"Word Count: {content.word_count}")
        print(f"\n{'-' * 80}\n")
        print(content.content)
        print(f"\n{'-' * 80}\n")
        
        if final_state.fact_check:
            fc = final_state.fact_check
            print(f"\nFact-Check Results:")
            print(f"  Accurate: {fc.is_accurate}")
            print(f"  Confidence: {fc.confidence_score:.2%}")
            if fc.issues_found:
                print(f"  Issues: {', '.join(fc.issues_found)}")
        
        print(f"\nSources ({len(content.sources_used)}):")
        for idx, url in enumerate(content.sources_used, 1):
            print(f"  {idx}. {url}")
        
        print("\n✅ Test completed successfully!")
    
    elif final_state and final_state.error_message:
        print(f"❌ Error: {final_state.error_message}")
    else:
        print("❌ No content generated")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys
    
    # Allow command-line arguments
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        test_workflow(topic)
    else:
        # Default test
        print("Testing with default topic...")
        print("(You can provide a custom topic as command-line argument)\n")
        test_workflow()
