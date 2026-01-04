import math

def generate_ccp_architecture():
    # --- Configuration ---
    filename = "assets/clog/ccp_architecture.svg"
    width, height = 900, 600
    bg_color = "#0f172a"  # Slate 900
    
    # Style Tokens
    colors = {
        "text": "#f1f5f9",      # Slate 100
        "border": "#334155",    # Slate 700
        "node_bg": "#1e293b",   # Slate 800
        "input_bg": "#4c1d95",  # Violet 900
        "logic_bg": "#0f766e",  # Teal 700
        "loop_bg": "#b45309",   # Amber 700
        "out_bg": "#14532d",    # Green 900
        
        "input_border": "#a78bfa",
        "logic_border": "#2dd4bf",
        "loop_border": "#fbbf24",
        "out_border": "#4ade80",
        
        "line": "#64748b"       # Slate 500
    }
    
    # Node Data (id, label, sub, type, x, y, w, h)
    nodes = [
        {"id": "user", "label": "User Request", "sub": "Raw Input", "type": "input", "x": 50, "y": 275, "w": 140, "h": 70},
        {"id": "chunk", "label": "Semantic Segmenter", "sub": "Intent Analysis", "type": "input", "x": 230, "y": 275, "w": 180, "h": 70},
        
        # Cognitive Core (Middle)
        {"id": "orch", "label": "Orchestrator", "sub": "State Manager", "type": "logic", "x": 480, "y": 150, "w": 160, "h": 70},
        {"id": "graph", "label": "Execution Graph", "sub": "Dynamic DAG", "type": "logic", "x": 480, "y": 400, "w": 160, "h": 70},
        
        # Neural-Symbolic Loop (Right)
        {"id": "retr", "label": "Hybrid Retrieval", "sub": "Vector + Regex", "type": "loop", "x": 700, "y": 100, "w": 160, "h": 70},
        {"id": "arg", "label": "Argument Gen", "sub": "LLM Decoding", "type": "loop", "x": 700, "y": 275, "w": 160, "h": 70},
        {"id": "tool", "label": "Tool Execution", "sub": "Sandbox", "type": "loop", "x": 700, "y": 450, "w": 160, "h": 70},
        
        # Output
        {"id": "out", "label": "Response Stream", "sub": "Context Block", "type": "out", "x": 480, "y": 550, "w": 160, "h": 60}
    ]
    
    edges = [
        ("user", "chunk"),
        ("chunk", "orch"),
        ("orch", "graph"), # Spawn
        ("graph", "retr"), # Query
        ("retr", "arg"),
        ("arg", "tool"),
        ("tool", "graph"), # Result Edge
        ("graph", "out")
    ]
    
    # Helper to get node by id
    def get_node(nid):
        return next(n for n in nodes if n["id"] == nid)

    # SVG Construction
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="background-color:{bg_color}; font-family: 'Courier New', monospace;">
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="{colors['line']}" />
        </marker>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>
    '''
    
    # Draw Connections
    for src_id, tgt_id in edges:
        s = get_node(src_id)
        t = get_node(tgt_id)
        
        # Calculate centers
        sx, sy = s["x"] + s["w"]/2, s["y"] + s["h"]/2
        tx, ty = t["x"] + t["w"]/2, t["y"] + t["h"]/2
        
        # Bezier Curve Logic
        path_d = ""
        # Custom routing for cleaner look
        if src_id == "chunk" and tgt_id == "orch":
            path_d = f"M{sx},{sy} C{sx+50},{sy} {tx-50},{ty} {tx},{ty}"
        elif src_id == "tool" and tgt_id == "graph":
            path_d = f"M{s['x']},{sy} C{s['x']-50},{sy} {t['x']+t['w']+50},{ty} {t['x']+t['w']},{ty}"
        elif src_id == "graph" and tgt_id == "retr":
             path_d = f"M{s['x']+s['w']},{sy} C{s['x']+s['w']+50},{sy} {t['x']-50},{ty} {t['x']},{ty}"
        else:
             # Default vertical/horizontal logic
             mid_y = (sy + ty) / 2
             path_d = f"M{sx},{sy} L{tx},{ty}"

        svg += f'<path d="{path_d}" stroke="{colors["line"]}" stroke-width="2" fill="none" marker-end="url(#arrow)" opacity="0.8" />'

    # Draw Nodes
    for n in nodes:
        # Determine colors based on type
        fill = colors["node_bg"]
        stroke = colors["border"]
        if n["type"] == "input":
            fill = colors["input_bg"]
            stroke = colors["input_border"]
        elif n["type"] == "logic":
            fill = colors["logic_bg"]
            stroke = colors["logic_border"]
        elif n["type"] == "loop":
            fill = colors["loop_bg"]
            stroke = colors["loop_border"]
        elif n["type"] == "out":
            fill = colors["out_bg"]
            stroke = colors["out_border"]
            
        svg += f'''
        <g transform="translate({n['x']}, {n['y']})">
            <rect width="{n['w']}" height="{n['h']}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#glow)" />
            <text x="{n['w']/2}" y="25" text-anchor="middle" fill="{colors['text']}" font-weight="bold" font-size="14">{n['label']}</text>
            <text x="{n['w']/2}" y="50" text-anchor="middle" fill="{colors['text']}" font-size="11" opacity="0.8">{n['sub']}</text>
        </g>
        '''
        
    svg += "</svg>"
    
    with open(filename, "w") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_ccp_architecture()
