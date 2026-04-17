import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Define colors
box_color = '#E3F2FD'
border_color = '#1976D2'
arrow_color = '#424242'

# Component positions (x, y, width, height)
components = [
    (3, 14, 4, 1, "User Input"),
    (3, 12, 4, 1, "Game Board\n(Current State)"),
    (3, 10, 4, 1, "Minimax Algorithm"),
    (3, 8, 4, 1, "Heuristic Evaluation\nFunction"),
    (3, 6, 4, 1, "Alpha-Beta Pruning"),
    (3, 4, 4, 1, "Best Move Selection"),
    (3, 2, 4, 1, "Update Game Board")
]

# Draw title
ax.text(5, 15.5, "Architecture of Connect 4 AI System", 
        fontsize=18, fontweight='bold', ha='center', va='center')

# Draw boxes and arrows
for i, (x, y, w, h, label) in enumerate(components):
    # Draw rectangle
    rect = patches.FancyBboxPatch((x, y), w, h, 
                                   boxstyle="round,pad=0.05",
                                   edgecolor=border_color, 
                                   facecolor=box_color,
                                   linewidth=2)
    ax.add_patch(rect)
    
    # Add text
    ax.text(x + w/2, y + h/2, label, 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Draw arrow to next component (except for last one)
    if i < len(components) - 1:
        arrow_start_y = y
        arrow_end_y = components[i+1][1] + components[i+1][3]
        ax.annotate('', xy=(5, arrow_end_y), xytext=(5, arrow_start_y),
                    arrowprops=dict(arrowstyle='->', lw=2.5, color=arrow_color))

plt.tight_layout()
plt.savefig('connect4_architecture.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Diagram saved as 'connect4_architecture.png'")
