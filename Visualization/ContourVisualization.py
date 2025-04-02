from Visualization.VisualizationStrategy import VisualizationStrategy


class ContourVisualization(VisualizationStrategy):
    def plot(self, ax, x, y, z):
        ax.contour(x, y, z, levels=20, cmap='plasma')
        ax.set_xlabel('Ось X')
        ax.set_ylabel('Ось Y')