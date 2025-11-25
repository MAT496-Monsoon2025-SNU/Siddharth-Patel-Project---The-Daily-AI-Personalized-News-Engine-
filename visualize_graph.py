"""
Visualize the LangGraph workflow and save it as an image.
"""

from src.graph.workflow import news_workflow
from IPython.display import Image, display

# Generate the graph visualization
try:
    # Get the graph as PNG
    graph_image = news_workflow.get_graph().draw_mermaid_png()
    
    # Save to file
    with open("workflow_graph.png", "wb") as f:
        f.write(graph_image)
    
    print("✅ Graph saved as 'workflow_graph.png'")
    print("You can open this file to see the visual representation of your workflow!")
    
except Exception as e:
    print(f"❌ Error generating graph: {e}")
    print("\nTrying alternative method...")
    
    # Alternative: Print Mermaid diagram code
    try:
        mermaid_code = news_workflow.get_graph().draw_mermaid()
        print("\n📊 Mermaid Diagram Code:")
        print("=" * 50)
        print(mermaid_code)
        print("=" * 50)
        print("\nYou can paste this code into https://mermaid.live to visualize the graph!")
    except Exception as e2:
        print(f"❌ Error: {e2}")
