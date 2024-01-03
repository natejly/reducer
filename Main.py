import app, mesh, tkinter as tk, polyscope as ps, os

def isfile(dir):
    return os.path.isfile(dir)

def binary(var):
    return var == 1

def runtime(gui):
    try:
        target_face_count = int(gui.target_var.get())
        aggressiveness = int(gui.aggressiveness_var.get()) 
        dir = gui.selected_file_folder.get()
        iterations = int(gui.iterations_var.get())
        alpha = float(gui.alpha_var.get())
        preserve_border = binary(gui.preserve_border_var.get())
        lossless = binary(gui.lossless_var.get())
        smoothing = binary(gui.smoothing_var.get())

        if isfile(dir):
            ps.init()
            ps.set_navigation_style("turntable")
            ps.set_up_dir("z_up")
            vertices, faces = mesh.Mesh.load(dir)
            path = os.path.split(dir)[0]
            filename = os.path.split(dir)[1]
            redname = os.path.splitext(filename)[0] + "_reduced" + os.path.splitext(filename)[1]
            output_path = os.path.join(path, redname)
            ps.register_surface_mesh("Original", vertices, faces)
            vertices, faces = mesh.Mesh.reduce(vertices, faces, target_face_count, aggressiveness, preserve_border, True, lossless)
            ps.register_surface_mesh("Reduced", vertices, faces)
            if smoothing:
                vertices = mesh.Mesh.smooth(vertices, faces, iterations, alpha)
                ps.register_surface_mesh("Reduced+Smoothed", vertices, faces)
            
            mesh.Mesh.export(vertices, faces, output_path) 
            ps.show()
        else:
            newfolder = dir+"_reduced"
            os.mkdir(newfolder)
            for filename in os.listdir(dir):
                if os.path.splitext(filename)[1] == ['.stl','.obj']:
                    path = os.path.join(dir, filename)
                    vertices, faces = mesh.Mesh.load(path)
                    filename = os.path.split(path)[1]
                    redname = os.path.splitext(filename)[0] + "_reduced" + os.path.splitext(filename)[1]
                    output_path = os.path.join(newfolder, redname)
                    vertices, faces = mesh.Mesh.reduce(vertices, faces, target_face_count, aggressiveness, preserve_border, True, lossless)
                    if smoothing:
                        vertices = mesh.Mesh.smooth(vertices, faces, iterations, alpha)
                        ps.register_surface_mesh("Reduced+Smoothed", vertices, faces)
                    mesh.Mesh.export(vertices, faces, output_path)
    
    except Exception as e:
        print("An error occurred:", e)

def main():
    try:
        root = tk.Tk()
        gui = app.App(root)
        root.mainloop()
    except Exception as e:
        print("An error occurred:", e)
  
if __name__ == "__main__":
    main()
