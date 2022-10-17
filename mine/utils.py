import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import random


def get_graph():
    buffer =BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def vhcle_tripcount_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 5))
    plt.title('Trip Count')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Vehicles')
    plt.ylabel('Number of Trips')
    plt.tight_layout()
    graph = get_graph()
    return graph


def vhcle_tripcount_bar_plot(x, y):
    plt.switch_backend('AGG')
    plt.bar(range(len(x)), y, align='center')
    plt.title('Trip-Count Chart')
    plt.xticks(range(len(x)), x)
    plt.xlabel('Vehicles')
    plt.ylabel('Number of Trips')
    graph = get_graph()
    return graph