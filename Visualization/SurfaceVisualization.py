from Visualization.VisualizationStrategy import VisualizationStrategy


class SurfaceVisualization(VisualizationStrategy):
    def plot(self, ax, x, y, z):
        ax.plot_surface(x, y, z, cmap='plasma', alpha=0.4, rstride=3, cstride=3, antialiased=False)
        ax.set_zlabel('Ось Z')