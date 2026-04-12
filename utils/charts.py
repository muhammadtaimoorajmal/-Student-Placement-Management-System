import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_application_status(parent_frame, data):
    """data: dict with status counts"""
    fig, ax = plt.subplots(figsize=(5,4))
    statuses = list(data.keys())
    counts = list(data.values())
    ax.bar(statuses, counts, color=['#4CAF50','#FFC107','#F44336','#2196F3'])
    ax.set_title('Application Status Distribution')
    ax.set_ylabel('Number of Applications')
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()