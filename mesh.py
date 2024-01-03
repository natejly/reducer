import pyfqmr
import trimesh as tr
import polyscope as ps
import time
import os
import trimesh
import numpy as np
class Mesh:
    @staticmethod
    def load(dir):
        try:
            print("Directory: " + dir)
            start = time.time()
            mesh = tr.load(dir)
            end = time.time()
            vertices = mesh.vertices
            faces = mesh.faces
            print(f"Loaded mesh in {round(end - start, 3)} seconds")
            return mesh.vertices, mesh.faces
        except Exception as e:
            print("Error loading mesh:", e)
            return None, None

    @staticmethod
    def reduce(vertices, faces, target_count, aggressiveness, preserve_border, verbose, lossless):
        try:
            ms = pyfqmr.Simplify()
            ms.setMesh(vertices, faces)
            ms.simplify_mesh(target_count=target_count, aggressiveness=aggressiveness, preserve_border=preserve_border, verbose=10, lossless=lossless)
            vertices, faces, normals = ms.getMesh()
            return vertices, faces
        except Exception as e:
            print("Error reducing mesh:", e)
            return None, None

    @staticmethod
    def smooth(vertices, faces, iterations, alpha):
        smoothed_vertices = vertices.copy()

        for _ in range(iterations):
            new_vertices = smoothed_vertices.copy()
            for i, vertex in enumerate(smoothed_vertices):
                neighbor_indices = np.where(faces == i)[0]
                neighbors = smoothed_vertices[faces[neighbor_indices, :]]
                average_neighbor_position = np.mean(neighbors, axis=0)    
                if average_neighbor_position.ndim == 2:
                    average_neighbor_position = average_neighbor_position[0]
                new_vertices[i] = vertex + alpha * (average_neighbor_position - vertex)
            
            smoothed_vertices = new_vertices

        return smoothed_vertices
    @staticmethod
    def export(vertices, faces, output_path):
        try:
            mesh = tr.Trimesh(vertices=vertices, faces=faces)
            mesh.export(output_path)
            print("Saved as: " + output_path)
            print("")
        except Exception as e:
            print("Error saving mesh:", e)

def main():
    try:
        ps.init()
        visualize = False
        target_face_count = 500000
        aggressiveness = 10
        preserve_border = True
        lossless = False
        iterations = 5
        alpha = 0.1
        input_file = "CTRL.stl"
        output_file = "Red" + input_file.split('.')[0] + ".stl"

        stock_vertices, stock_faces = Mesh.load(input_file)

        if visualize:
            ps.register_surface_mesh("Original", stock_vertices, stock_faces)

        vertices, faces = Mesh.reduce(stock_vertices, stock_faces, target_face_count, aggressiveness, preserve_border, lossless)

        if visualize:
            ps.register_surface_mesh("Reduced", vertices, faces)

        smoothed_vertices = Mesh.smooth(vertices, faces, iterations, alpha)

        if visualize:
            ps.register_surface_mesh("Smoothed", smoothed_vertices, faces)
            ps.show()
            print("Close polyscope to continue")

        Mesh.export(smoothed_vertices, faces, output_file)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
