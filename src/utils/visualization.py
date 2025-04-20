import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np

def create_timeline_visualization(
    events: List[Dict],
    sentiment_data: pd.DataFrame,
    title: str = "Event-Sentiment Timeline"
) -> go.Figure:
    """Create an interactive timeline visualization showing events and sentiment."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add sentiment line
    fig.add_trace(
        go.Scatter(
            x=sentiment_data["timestamp"],
            y=sentiment_data["sentiment_score"],
            name="Sentiment Score",
            line=dict(color="blue")
        ),
        secondary_y=False
    )
    
    # Add event markers
    for event in events:
        fig.add_trace(
            go.Scatter(
                x=[event["timestamp"]],
                y=[event.get("sentiment_impact", 0)],
                mode="markers+text",
                name=event["type"],
                text=[event["text"]],
                textposition="top center",
                marker=dict(
                    size=10,
                    symbol="diamond",
                    color="red" if event.get("sentiment_impact", 0) < 0 else "green"
                )
            ),
            secondary_y=True
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Sentiment Score",
        yaxis2_title="Event Impact",
        showlegend=True,
        hovermode="x unified"
    )
    
    return fig

def create_rumor_analysis_visualization(
    rumors: List[Dict],
    title: str = "Rumor Analysis Dashboard"
) -> go.Figure:
    """Create an interactive dashboard showing rumor analysis results."""
    # Prepare data
    cluster_sizes = [len(r["messages"]) for r in rumors]
    confidence_scores = [r["confidence"] for r in rumors]
    spread_scores = [r["spread_score"] for r in rumors]
    verdicts = [r["verdict"] for r in rumors]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Rumor Clusters by Size",
            "Confidence Distribution",
            "Spread vs Confidence",
            "Verdict Distribution"
        )
    )
    
    # Cluster size distribution
    fig.add_trace(
        go.Histogram(
            x=cluster_sizes,
            name="Cluster Size",
            nbinsx=20
        ),
        row=1, col=1
    )
    
    # Confidence distribution
    fig.add_trace(
        go.Histogram(
            x=confidence_scores,
            name="Confidence",
            nbinsx=20
        ),
        row=1, col=2
    )
    
    # Spread vs Confidence scatter
    fig.add_trace(
        go.Scatter(
            x=spread_scores,
            y=confidence_scores,
            mode="markers",
            text=verdicts,
            marker=dict(
                size=cluster_sizes,
                color=confidence_scores,
                colorscale="Viridis",
                showscale=True
            ),
            name="Rumor Clusters"
        ),
        row=2, col=1
    )
    
    # Verdict distribution
    verdict_counts = pd.Series(verdicts).value_counts()
    fig.add_trace(
        go.Pie(
            labels=verdict_counts.index,
            values=verdict_counts.values,
            name="Verdicts"
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        showlegend=True,
        height=800
    )
    
    return fig

def create_rumor_alert(
    rumor: Dict,
    threshold: float = 0.7
) -> Dict:
    """Create a formatted alert for high-confidence rumors."""
    if rumor["confidence"] < threshold:
        return None
    
    return {
        "title": "⚠️ High-Confidence Rumor Detected",
        "content": {
            "message": f"This phrase has appeared in {len(rumor['messages'])} messages",
            "time_span": f"over the last {rumor['time_span'].total_seconds()/3600:.1f} hours",
            "confidence": f"Confidence: {rumor['confidence']:.2%}",
            "verdict": f"Verdict: {rumor['verdict']}",
            "pattern_matches": f"Pattern matches: {rumor['pattern_matches']}",
            "sample_messages": [
                msg["text"] for msg in rumor["messages"][:3]  # Show first 3 messages
            ]
        }
    } 