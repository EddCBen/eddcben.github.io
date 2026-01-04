import math

def generate_home_architecture():
    # --- Configuration ---
    filename = "assets/images/architecture.svg"
    width, height = 900, 500
    bg_color = "transparent" # Integrate with page bg
    
    # Scientific Color Palette (Slate/Teal/Indigo)
    colors = {
        "text": "#f8fafc",      # Slate 50
        "sub_text": "#94a3b8",  # Slate 400
        "border": "#334155",    # Slate 700
        
        "input_bg": "#312e81",  # Indigo 900
        "input_stroke": "#6366f1", # Indigo 500
        
        "kernel_bg": "#0f172a", # Slate 900
        "kernel_stroke": "#38bdf8", # Sky 400 (The "Core")
        
        "proto_bg": "#134e4a",  # Teal 900
        "proto_stroke": "#2dd4bf", # Teal 400
        
        "graph_bg": "#3f3f46",  # Zinc 700
        "graph_stroke": "#a1a1aa", # Zinc 400
        
        "line": "#64748b"       # Slate 500
    }
    
    # Node Data
    nodes = [
        # Inputs
        {"id": "in1", "label": "Multi-Modal", "sub": "Input Stream", "type": "input", "x": 50, "y": 200, "w": 140, "h": 100},
        
        # The Protocol Shell
        {"id": "proto", "label": "Deterministic Protocol", "sub": "Verifiable Logic Layer", "type": "proto", "x": 250, "y": 100, "w": 400, "h": 300},
        
        # The Kernel (Inside Protocol)
        {"id": "cru", "label": "CRU", "sub": "Probabilistic Kernel\n(SLM)", "type": "kernel", "x": 350, "y": 200, "w": 200, "h": 100},
        
        # The Graph (Output)
        {"id": "graph", "label": "Execution Graph", "sub": "Structured Memory", "type": "graph", "x": 700, "y": 150, "w": 160, "h": 200}
    ]
    
    # Helper to clean up graph lines
    edges = [
        ("in1", "cru"), # Input penetrates protocol to Kernel
        ("cru", "graph"), # Kernel updates Graph
        ("proto", "graph") # Protocol constraints enforce Graph structure
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="background-color:{bg_color}; font-family: 'Inter', 'Segoe UI', sans-serif;">
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="{colors['line']}" />
        </marker>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <linearGradient id="protoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{colors['proto_bg']};stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:{colors['proto_bg']};stop-opacity:0.4" />
        </linearGradient>
    </defs>
    '''
    
    # Draw logic is specific here to show encapsulation
    
    # 1. Inputs
    n = nodes[0]
    svg += f'''
    <g transform="translate({n['x']}, {n['y']})">
        <rect width="{n['w']}" height="{n['h']}" rx="12" fill="{colors['input_bg']}" stroke="{colors['input_stroke']}" stroke-width="2" />
        <text x="{n['w']/2}" y="45" text-anchor="middle" fill="{colors['text']}" font-weight="bold" font-size="16">{n['label']}</text>
        <text x="{n['w']/2}" y="70" text-anchor="middle" fill="{colors['sub_text']}" font-size="12">{n['sub']}</text>
    </g>
    '''
    
    # 2. Protocol Shell (Behind Kernel)
    p = nodes[1]
    svg += f'''
    <g transform="translate({p['x']}, {p['y']})">
        <rect width="{p['w']}" height="{p['h']}" rx="20" fill="url(#protoGradient)" stroke="{colors['proto_stroke']}" stroke-width="2" stroke-dasharray="5,5" />
        <text x="{p['w']/2}" y="40" text-anchor="middle" fill="{colors['proto_stroke']}" font-weight="bold" font-size="14" letter-spacing="1">{p['label'].upper()}</text>
        <text x="{p['w']/2}" y="280" text-anchor="middle" fill="{colors['sub_text']}" font-size="12">{p['sub']}</text>
    </g>
    '''
    
    # 3. Connections (Before Kernel to be underneath?) No, on top typically.
    # Let's draw Kernel first then lines? No lines should connect centers.
    
    # Draw Edges
    # Input -> Kernel
    svg += f'<path d="M{nodes[0]["x"]+nodes[0]["w"]},{nodes[0]["y"]+nodes[0]["h"]/2} L{nodes[2]["x"]},{nodes[2]["y"]+nodes[2]["h"]/2}" stroke="{colors["line"]}" stroke-width="2" marker-end="url(#arrow)" />'
    
    # Kernel -> Graph
    svg += f'<path d="M{nodes[2]["x"]+nodes[2]["w"]},{nodes[2]["y"]+nodes[2]["h"]/2} L{nodes[3]["x"]},{nodes[3]["y"]+nodes[3]["h"]/2}" stroke="{colors["line"]}" stroke-width="2" marker-end="url(#arrow)" />'
    
    # Protocol top -> Graph top (Enforcement line)
    svg += f'<path d="M{nodes[1]["x"]+nodes[1]["w"]},{nodes[1]["y"]+60} C{nodes[1]["x"]+nodes[1]["w"]+50},{nodes[1]["y"]+60} {nodes[3]["x"]-50},{nodes[3]["y"]+40} {nodes[3]["x"]},{nodes[3]["y"]+40}" stroke="{colors["proto_stroke"]}" stroke-width="1" stroke-dasharray="2,2" marker-end="url(#arrow)" opacity="0.6"/>'

    # 4. Kernel (CRU)
    k = nodes[2]
    svg += f'''
    <g transform="translate({k['x']}, {k['y']})">
        <rect width="{k['w']}" height="{k['h']}" rx="12" fill="{colors['kernel_bg']}" stroke="{colors['kernel_stroke']}" stroke-width="3" filter="url(#glow)" />
        <text x="{k['w']/2}" y="45" text-anchor="middle" fill="{colors['text']}" font-weight="bold" font-size="20">{k['label']}</text>
        <text x="{k['w']/2}" y="75" text-anchor="middle" fill="{colors['sub_text']}" font-size="12">{k['sub'].split()[0]} {k['sub'].split()[1]}</text>
    </g>
    '''
    
    # 5. Graph
    g = nodes[3]
    # Draw some internal nodes like a mini graph
    svg += f'''
    <g transform="translate({g['x']}, {g['y']})">
        <rect width="{g['w']}" height="{g['h']}" rx="8" fill="{colors['graph_bg']}" stroke="{colors['graph_stroke']}" stroke-width="2" />
        <text x="{g['w']/2}" y="25" text-anchor="middle" fill="{colors['text']}" font-weight="bold" font-size="14">{g['label']}</text>
        <text x="{g['w']/2}" y="180" text-anchor="middle" fill="{colors['sub_text']}" font-size="11">{g['sub']}</text>
        
        <!-- Internal DAG mini-viz -->
        <circle cx="80" cy="50" r="10" fill="#fca5a5" opacity="0.8"/>
        <circle cx="50" cy="100" r="10" fill="#fcd34d" opacity="0.8"/>
        <circle cx="110" cy="100" r="10" fill="#fcd34d" opacity="0.8"/>
        <circle cx="80" cy="150" r="10" fill="#86efac" opacity="0.8"/>
        
        <path d="M80,60 L50,90" stroke="white" stroke-width="1" opacity="0.5"/>
        <path d="M80,60 L110,90" stroke="white" stroke-width="1" opacity="0.5"/>
        <path d="M50,110 L80,140" stroke="white" stroke-width="1" opacity="0.5"/>
        <path d="M110,110 L80,140" stroke="white" stroke-width="1" opacity="0.5"/>
    </g>
    '''
            
    svg += "</svg>"
    
    with open(filename, "w") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_home_architecture()
