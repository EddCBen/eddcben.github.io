import math

def generate_csd_architecture():
    # --- Configuration ---
    filename = "assets/clog/csd_architecture.svg"
    width, height = 900, 500  # Wider for side-by-side
    bg_color = "#0a0a1a"
    
    # Style Tokens (Scientific Blue Theme)
    colors = {
        "text": "#e0e6ed",
        "border": "#1e3a8a",  # Deep Blue
        "node_bg": "#111827", # Dark gray/blue
        "node_header": "#1e293b",
        "accent_std": "#64748b", # Slate (Standard)
        "accent_root": "#3b82f6", # Blue
        "accent_db": "#f472b6",   # Pink (Vector DAG)
        "accent_slm": "#a78bfa",  # Purple (SLM)
        "line": "#94a3b8"
    }
    
    # Node Data
    nodes = [
        # Standard LLM (Left)
        {"id": "std_tok", "label": "Tokens", "sub": "0...N", "type": "std", "x": 50, "y": 150, "w": 120, "h": 60},
        {"id": "std_ctx", "label": "Context", "sub": "Window", "type": "std", "x": 50, "y": 250, "w": 120, "h": 60},
        {"id": "std_inf", "label": "Inference", "sub": "Compute", "type": "std", "x": 50, "y": 350, "w": 120, "h": 60},

        # CSD Architecture (Right)
        {"id": "csd_in", "label": "Input", "sub": "Intent", "type": "root", "x": 350, "y": 100, "w": 120, "h": 60},
        {"id": "csd_retr", "label": "Retriever", "sub": "Search", "type": "root", "x": 550, "y": 100, "w": 120, "h": 60},
        {"id": "csd_dag", "label": "Vector DAG", "sub": "Logical State", "type": "db", "x": 550, "y": 20, "w": 120, "h": 60}, # Above retriever
        {"id": "csd_local", "label": "Local Cay", "sub": "Context", "type": "root", "x": 750, "y": 100, "w": 120, "h": 60},
        
        {"id": "csd_slm", "label": "SLM Kernel", "sub": "Synthesis", "type": "slm", "x": 750, "y": 250, "w": 120, "h": 60},
        
        {"id": "csd_new", "label": "New Node", "sub": "Update", "type": "root", "x": 550, "y": 250, "w": 120, "h": 60},
    ]
    
    # Edges
    edges = [
        # Standard
        ("std_tok", "std_ctx"),
        ("std_ctx", "std_inf"),
        
        # CSD
        ("csd_in", "csd_retr"),
        ("csd_dag", "csd_retr"), # DB to Retriever
        ("csd_retr", "csd_local"),
        ("csd_local", "csd_slm"),
        ("csd_slm", "csd_new"),
        ("csd_new", "csd_dag")   # New Node back to DAG (Cycle)
    ]
    
    # Groups (Standard vs CSD) labels
    # We will just draw them as text
    
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
        <linearGradient id="db_grad" x1="0%" y1="0%" x2="100%" y2="0%">
             <stop offset="0%" stop-color="{colors['accent_db']}" stop-opacity="0.2"/>
             <stop offset="100%" stop-color="{colors['accent_db']}" stop-opacity="0.1"/>
        </linearGradient>
    </defs>
    
    <!-- Separator -->
    <line x1="250" y1="50" x2="250" y2="450" stroke="{colors['border']}" stroke-dasharray="4 4" opacity="0.5" />
    
    <text x="110" y="40" fill="{colors['text']}" text-anchor="middle" font-weight="bold" font-family="monospace">Standard LLM</text>
    <text x="600" y="40" fill="{colors['text']}" text-anchor="middle" font-weight="bold" font-family="monospace">CSD Architecture</text>

    '''
    
    node_map = {n["id"]: n for n in nodes}
    
    # Draw Edges
    for src_id, tgt_id in edges:
        src = node_map[src_id]
        tgt = node_map[tgt_id]
        
        # Logic for connecting nodes. 
        # Standard: vertically down
        # CSD: mixed.
        
        # Simple center-to-center logic with specific anchor points would be better, but lets estimate
        # Default: Source Center -> Target Center (clipped by rect)? 
        # Better: Explicit anchors.
        
        # Simple approximation: Center to Center
        sx = src["x"] + src["w"]/2
        sy = src["y"] + src["h"]/2
        tx = tgt["x"] + tgt["w"]/2
        ty = tgt["y"] + tgt["h"]/2
        
        # Adjust start/end to be on the border
        # This is strictly manual for this script for simplicity or we calculate intersections.
        # Manual overrides for cleaner graph:
        
        if src["type"] == "std":
             sx, sy = src["x"] + src["w"]/2, src["y"] + src["h"]
             tx, ty = tgt["x"] + tgt["w"]/2, tgt["y"]
             
        elif src_id == "csd_in":
             sx, sy = src["x"] + src["w"], src["y"] + src["h"]/2
             tx, ty = tgt["x"], tgt["y"] + tgt["h"]/2
        elif src_id == "csd_dag":
             sx, sy = src["x"] + src["w"]/2, src["y"] + src["h"]
             tx, ty = tgt["x"] + tgt["w"]/2, tgt["y"]
        elif src_id == "csd_retr":
             sx, sy = src["x"] + src["w"], src["y"] + src["h"]/2
             tx, ty = tgt["x"], tgt["y"] + tgt["h"]/2
        elif src_id == "csd_local":
            # Bend down to SLM
             sx, sy = src["x"] + src["w"]/2, src["y"] + src["h"]
             tx, ty = tgt["x"] + tgt["w"]/2, tgt["y"]
        elif src_id == "csd_slm":
            # Left to New
             sx, sy = src["x"], src["y"] + src["h"]/2
             tx, ty = tgt["x"] + tgt["w"], tgt["y"] + tgt["h"]/2
        elif src_id == "csd_new":
            # Up to DAG
             sx, sy = src["x"] + src["w"]/2, src["y"]
             tx, ty = tgt["x"] + tgt["w"]/2, tgt["y"] + tgt["h"]
            
        
        # Draw Curve
        # Midpoints
        midx = (sx + tx) / 2
        midy = (sy + ty) / 2
        
        path = ""
        # Straight lines for standard
        if src["type"] == "std":
             path = f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{colors["line"]}" stroke-width="2" marker-end="url(#arrowhead)" opacity="0.8" />'
        
        # Curved for CSD
        else:
            # Bezier
            c1x, c1y, c2x, c2y = sx, sy, tx, ty # Default straight
            
            # Custom curves
            if src_id == "csd_new" and tgt_id == "csd_dag":
                 # Large curve back up
                 path = f'<path d="M {sx} {sy} C {sx} {midy}, {tx} {midy}, {tx} {ty}" stroke="{colors["line"]}" stroke-width="2" fill="none" marker-end="url(#arrowhead)" opacity="0.8" stroke-dasharray="5 5" />' 
                 # Dashed for cycle/update
            else:
                 path = f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="{colors["line"]}" stroke-width="2" marker-end="url(#arrowhead)" opacity="0.8" />'
        
        svg += path + "\n"

    # Draw Nodes
    for n in nodes:
        accent = colors[f"accent_{n['type']}"] if n['type'] in ['root', 'std', 'db', 'slm'] else colors['accent_root']
        
        shape = "rect" # Default
        if n['type'] == 'db':
            # Cylinder-ish (just rect for now with different fill)
             pass
        
        svg += f'<g transform="translate({n["x"]}, {n["y"]})">'
        
        # Glow
        svg += f'<rect x="0" y="0" width="{n["w"]}" height="{n["h"]}" rx="6" fill="{colors["node_bg"]}" stroke="{accent}" stroke-width="1" filter="url(#glow)" opacity="0.3" />'
        
        if n['type'] == 'db':
            # Database shape hint
            svg += f'<rect x="0" y="0" width="{n["w"]}" height="{n["h"]}" rx="6" fill="url(#db_grad)" stroke="{accent}" stroke-width="1" />'
            svg += f'<rect x="0" y="0" width="{n["w"]}" height="10" rx="2" fill="{accent}" opacity="0.5" />' # Top lid
        else:
            # Main Body
            svg += f'<rect x="0" y="0" width="{n["w"]}" height="{n["h"]}" rx="6" fill="{colors["node_bg"]}" stroke="{colors["border"]}" stroke-width="1" />'
            # Header
            svg += f'<path d="M 0 6 Q 0 0 6 0 L {n["w"]-6} 0 Q {n["w"]} 0 {n["w"]} 6 L {n["w"]} 20 L 0 20 Z" fill="{colors["node_header"]}" />'
            # Dot
            svg += f'<circle cx="15" cy="10" r="3" fill="{accent}" />'
        
        # Text
        svg += f'<text x="28" y="14" fill="{colors["text"]}" font-size="11" font-weight="bold" font-family="monospace">{n["label"]}</text>'
        svg += f'<text x="{n["w"]/2}" y="45" fill="{colors["text"]}" font-size="11" text-anchor="middle" font-style="italic" opacity="0.8">{n["sub"]}</text>'
        
        svg += '</g>\n'

    svg += '</svg>'
    
    with open(filename, "w") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_csd_architecture()
