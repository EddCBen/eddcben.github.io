import math

def generate_context_dag():
    # --- Configuration ---
    filename = "assets/images/context_dag.svg"
    width, height = 800, 500
    bg_color = "#0a0a1a"  # Dark scientific blue/black
    
    # Style Tokens
    colors = {
        "text": "#e0e6ed",
        "border": "#1e3a8a",  # Deep Blue
        "node_bg": "#111827", # Dark gray/blue
        "node_header": "#1e293b",
        "accent_root": "#3b82f6", # Blue
        "accent_idea": "#8b5cf6", # Purple
        "accent_reason": "#f59e0b", # Amber
        "accent_fact": "#10b981", # Emerald
        "line": "#94a3b8"
    }
    
    # Node Data (ID, Label, SubTitle, Type, x, y, width, height)
    nodes = [
        {"id": "root", "label": "ROOT", "sub": "Genesis", "type": "root", "x": 50, "y": 200, "w": 140, "h": 70},
        {"id": "idea1", "label": "CTXB-01", "sub": "User Segment A", "type": "idea", "x": 300, "y": 100, "w": 160, "h": 70},
        {"id": "idea2", "label": "CTXB-02", "sub": "User Segment B", "type": "idea", "x": 300, "y": 300, "w": 160, "h": 70},
        {"id": "reason", "label": "RSN-01", "sub": "Analysis Node", "type": "reason", "x": 550, "y": 100, "w": 160, "h": 70},
        {"id": "fact", "label": "FACT-01", "sub": "Entity Extraction", "type": "fact", "x": 600, "y": 250, "w": 160, "h": 70}
    ]
    
    # Edges (Source ID, Target ID)
    edges = [
        ("root", "idea1"),
        ("root", "idea2"),
        ("idea1", "reason"),
        ("reason", "fact"),
        ("idea2", "fact")
    ]
    
    # SVG Header
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="font-family: 'Computer Modern', serif;">
    <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="{colors['line']}" />
        </marker>
    </defs>
    
    <!-- Background (Transparent or Styled) -->
    <!-- <rect width="100%" height="100%" fill="{bg_color}" /> -->
    '''
    
    # Draw Edges (Cubic Bezier)
    node_map = {n["id"]: n for n in nodes}
    
    for src_id, tgt_id in edges:
        src = node_map[src_id]
        tgt = node_map[tgt_id]
        
        # Calculate start and end points (Right side of src, Left side of tgt)
        sx = src["x"] + src["w"]
        sy = src["y"] + src["h"] / 2
        tx = tgt["x"]
        ty = tgt["h"] / 2 + tgt["y"]
        
        # Control points for smooth curve
        c1x = sx + (tx - sx) / 2
        c1y = sy
        c2x = tx - (tx - sx) / 2
        c2y = ty
        
        path = f'<path d="M {sx} {sy} C {c1x} {c1y}, {c2x} {c2y}, {tx} {ty}" stroke="{colors["line"]}" stroke-width="2" fill="none" marker-end="url(#arrowhead)" opacity="0.8" />'
        svg += path + "\n"
        
    # Draw Nodes
    for n in nodes:
        # Determine Color based on type
        accent = colors[f"accent_{n['type']}"]
        
        # Node Group
        svg += f'<g transform="translate({n["x"]}, {n["y"]})">'
        
        # Shadow/Glow
        svg += f'<rect x="0" y="0" width="{n["w"]}" height="{n["h"]}" rx="6" fill="{colors["node_bg"]}" stroke="{accent}" stroke-width="1" filter="url(#glow)" opacity="0.3" />'
        
        # Main Body
        svg += f'<rect x="0" y="0" width="{n["w"]}" height="{n["h"]}" rx="6" fill="{colors["node_bg"]}" stroke="{colors["border"]}" stroke-width="1" />'
        
        # Header Bar
        svg += f'<path d="M 0 6 Q 0 0 6 0 L {n["w"]-6} 0 Q {n["w"]} 0 {n["w"]} 6 L {n["w"]} 24 L 0 24 Z" fill="{colors["node_header"]}" />'
        
        # Indicator Dot
        svg += f'<circle cx="15" cy="12" r="4" fill="{accent}" />'
        
        # Header Text (Label)
        svg += f'<text x="28" y="16" fill="{colors["text"]}" font-size="12" font-weight="bold" font-family="monospace">{n["label"]}</text>'
        
        # Body Text (Subtitle)
        svg += f'<text x="{n["w"]/2}" y="48" fill="{colors["text"]}" font-size="12" text-anchor="middle" font-style="italic" opacity="0.8">{n["sub"]}</text>'
        
        svg += '</g>\n'

    # Footer/Title
    svg += f'<text x="{width/2}" y="{height-20}" fill="{colors["line"]}" text-anchor="middle" font-size="14" font-family="monospace" opacity="0.5">FIG 2: CONTEXT STATE DAG TOPOLOGY</text>'

    svg += '</svg>'
    
    with open(filename, "w") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_context_dag()
