import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Rectangle
import numpy as np

# Create figure with white background
fig = plt.figure(figsize=(12, 16), facecolor='white')
ax = fig.add_subplot(111)
ax.set_xlim(0, 12)
ax.set_ylim(0, 16)
ax.axis('off')

# Modern color scheme - soft gradients
colors = {
    'primary': '#667EEA',      # Soft purple-blue
    'secondary': '#764BA2',    # Deep purple
    'light1': '#F7FAFC',       # Very light gray
    'light2': '#EDF2F7',       # Light gray
    'accent1': '#4299E1',      # Sky blue
    'accent2': '#9F7AEA',      # Light purple
    'text': '#2D3748',         # Dark gray
    'shadow': '#E2E8F0'        # Shadow gray
}

def create_gradient_box(x, y, w, h, color1, color2, label, label_size=14, border_width=2):
    """Create a box with gradient effect and shadow"""
    # Shadow layer
    shadow = FancyBboxPatch(
        (x + 0.1, y - 0.1), w, h,
        boxstyle="round,pad=0.12",
        facecolor=colors['shadow'],
        edgecolor='none',
        alpha=0.3,
        zorder=1
    )
    ax.add_patch(shadow)
    
    # Main box with gradient simulation
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.12",
        facecolor=color1,
        edgecolor=color2,
        linewidth=border_width,
        zorder=2
    )
    ax.add_patch(box)
    
    # Label
    ax.text(
        x + w/2, y + h/2, label,
        fontsize=label_size,
        fontweight='600',
        ha='center',
        va='center',
        color=colors['text'],
        zorder=3
    )

def create_arrow(x1, y1, x2, y2, color=colors['primary']):
    """Create smooth arrow"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='->,head_width=0.4,head_length=0.5',
        color=color,
        linewidth=3,
        alpha=0.7,
        zorder=1
    )
    ax.add_patch(arrow)

def create_icon_user(x, y, size=0.4):
    """Create user icon"""
    head = Circle((x, y + size*0.3), size*0.25, facecolor=colors['accent1'], 
                  edgecolor='white', linewidth=2, zorder=3)
    ax.add_patch(head)
    body = Wedge((x, y - size*0.1), size*0.5, 0, 180, 
                 facecolor=colors['accent1'], edgecolor='white', linewidth=2, zorder=3)
    ax.add_patch(body)

def create_icon_grid(x, y, size=0.5):
    """Create grid icon for game board"""
    for i in range(4):
        for j in range(3):
            rect = Rectangle(
                (x - size/2 + i*size/3.5, y - size/3 + j*size/3),
                size/4, size/4,
                facecolor='white',
                edgecolor=colors['accent1'],
                linewidth=2,
                zorder=3
            )
            ax.add_patch(rect)

def create_icon_brain(x, y, size=0.5):
    """Create brain/AI icon"""
    # Outer circle
    outer = Circle((x, y), size*0.6, facecolor=colors['secondary'], 
                   alpha=0.2, edgecolor=colors['secondary'], linewidth=2, zorder=3)
    ax.add_patch(outer)
    
    # Neural network nodes
    positions = [(-0.3, 0), (0, 0.3), (0.3, 0), (0, -0.3)]
    for px, py in positions:
        node = Circle((x + px*size, y + py*size), size*0.15, 
                     facecolor=colors['secondary'], edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(node)

# Layout configuration
center = 6
box_w = 4.5
box_h = 1.1
gap = 1.5

# Title
ax.text(center, 15.2, 'Connect 4 AI Architecture', 
        fontsize=20, fontweight='bold', ha='center', color=colors['text'])

# Component 1: User Input
y = 13.5
create_icon_user(center, y + 1.3, 0.5)
create_gradient_box(center - box_w/2, y, box_w, box_h, 
                   colors['light1'], colors['accent1'], 'User Input', 13)
create_arrow(center, y, center, y - gap + box_h)

# Component 2: Game Board State
y -= gap
create_icon_grid(center, y + 1.3, 0.6)
create_gradient_box(center - box_w/2, y, box_w, box_h,
                   colors['light1'], colors['accent1'], 'Game Board State', 13)
create_arrow(center, y, center, y - gap + box_h)

# Component 3: AI Processing (highlighted section)
y -= gap
ai_h = 4.2
ai_w = 6

# AI container with gradient
ai_container = FancyBboxPatch(
    (center - ai_w/2, y - ai_h + box_h), ai_w, ai_h,
    boxstyle="round,pad=0.2",
    facecolor='#F7F5FB',
    edgecolor=colors['secondary'],
    linewidth=3,
    zorder=0
)
ax.add_patch(ai_container)

# AI icon
create_icon_brain(center, y + 0.5, 0.6)

# AI sub-components
ai_box_w = 4.8
ai_box_h = 0.85
ai_gap = 0.95

y_ai = y - 0.6
create_gradient_box(center - ai_box_w/2, y_ai, ai_box_w, ai_box_h,
                   colors['light2'], colors['secondary'], 'Minimax Algorithm', 12, 1.5)

y_ai -= ai_gap
create_gradient_box(center - ai_box_w/2, y_ai, ai_box_w, ai_box_h,
                   colors['light2'], colors['secondary'], 'Heuristic Evaluation', 12, 1.5)

y_ai -= ai_gap
create_gradient_box(center - ai_box_w/2, y_ai, ai_box_w, ai_box_h,
                   colors['light2'], colors['secondary'], 'Alpha-Beta Pruning', 12, 1.5)

# Arrow from AI section
y = y - ai_h + box_h
create_arrow(center, y, center, y - gap + box_h)

# Component 4: Best Move Selection
y -= gap
create_gradient_box(center - box_w/2, y, box_w, box_h,
                   colors['light1'], colors['primary'], 'Best Move Selection', 13)
create_arrow(center, y, center, y - gap + box_h)

# Component 5: Board Update
y -= gap
create_gradient_box(center - box_w/2, y, box_w, box_h,
                   colors['light1'], colors['primary'], 'Board Update', 13)

# Save with high quality
plt.tight_layout()
plt.savefig('connect4_premium_architecture.png', 
            dpi=350, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none',
            pad_inches=0.4)
print("✓ Premium architecture diagram created successfully!")
print("  File: connect4_premium_architecture.png")
