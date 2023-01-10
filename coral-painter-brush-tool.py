import dearpygui.dearpygui as dpg
import os
import shutil

brush_dir_path = ""
painter_dir_path = ""
brush_library_name = ""
brush_pack_name = ""
brush_pack_icon = "assets/default-icon.png"

def save_callback():
    print("Save Clicked")

def file_picker_callback(sender, picker_data):

    global brush_dir_path
    global painter_dir_path
    global brush_pack_icon

    print("dir {0} opened".format(picker_data["file_path_name"]))

    if sender == "brush_location_file_picker":
        brush_dir_path = picker_data["file_path_name"]
        dpg.set_value("brush_path_label", brush_dir_path)
    if sender == "painter_location_file_picker":
        painter_dir_path = picker_data["file_path_name"]
        dpg.set_value("brush_folder_path_label", painter_dir_path)
    if sender == "brush_icon_file_picker":
        brush_pack_icon = picker_data["file_path_name"]
        dpg.set_value("brush_icon_path_label", brush_pack_icon)

def open_brush_file_picker(sender):
    dpg.show_item("brush_location_file_picker")

def open_painter_file_picker(sender):
    dpg.show_item("painter_location_file_picker")

def open_icon_file_picker(sender):
    dpg.show_item("brush_icon_file_picker")

def create_brush_pack():
    brush_library_name = dpg.get_value("brush_lib_name_field")
    brush_pack_name = dpg.get_value("brush_pack_name_field")


    # Make string consisting of path where brush lib needs to go (or is) (painter_dir_path + brush_library_name)
    brush_lib_path = "{0}/{1}".format(painter_dir_path, brush_library_name)
    brush_pack_path = "{0}/{1}".format(brush_lib_path,brush_pack_name)
    # Move brush pack (brush_dir_path) into folder with name of brush_pack_name inside brush library
    shutil.move(brush_dir_path, brush_pack_path)
    shutil.copy2(brush_pack_icon, brush_lib_path+"/{0}.png".format(brush_pack_name))
    # Create (or edit) Ordering.dat file and append the needed formatted line to it
    with open(brush_lib_path+"/Ordering.dat","a") as order_file:
        order_file.write("brush-categories|{0}|{1}|-1 \n".format(brush_library_name,brush_pack_name))

dpg.create_context()
dpg.create_viewport(title="Coral Painter Brush Tool by Deurman", min_width=600,width=600, height=400, min_height=400)
dpg.setup_dearpygui()

with dpg.window(tag="main_window", menubar=False):
    dpg.add_text("Brush location:")
    with dpg.group(horizontal=True):
        dpg.add_text("No path selected",tag="brush_path_label")
        dpg.add_button(label="Browse", callback=open_brush_file_picker)
    dpg.add_file_dialog(directory_selector=True, show=False, callback=file_picker_callback, tag="brush_location_file_picker", height=300, width=500)

    dpg.add_spacer(height=10)

    dpg.add_text("Painter Brush folder:")
    with dpg.group(horizontal=True):
        dpg.add_text("No path selected",tag="brush_folder_path_label")
        dpg.add_button(label="Browse", callback=open_painter_file_picker)
    dpg.add_file_dialog(directory_selector=True, show=False, callback=file_picker_callback, tag="painter_location_file_picker", height=300, width=500)

    dpg.add_text("Brush pack icon:")
    with dpg.group(horizontal=True):
        dpg.add_text(brush_pack_icon,tag="brush_icon_path_label")
        dpg.add_button(label="Browse", callback=open_icon_file_picker)
    with dpg.file_dialog(directory_selector=False, show=False, callback=file_picker_callback, tag="brush_icon_file_picker", height=300, width=500):
        dpg.add_file_extension(".png")

    dpg.add_spacer(height=10)

    dpg.add_text("Brush library name:")
    dpg.add_input_text(tag="brush_lib_name_field")

    dpg.add_text("Brush pack name:")
    dpg.add_input_text(tag="brush_pack_name_field")

    dpg.add_spacer(height=10)

    dpg.add_button(label="Create/Update brush pack", callback=create_brush_pack)

dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()