bl_info = {
    "name": "Smart STL Exporter (Live Preview)",
    "author": "Andreas Papesch & Copilot",
    "version": (2, 4),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > Smart STL",
    "description": "Export STL with unit detection, custom scale, live mm preview, total bbox, and logging",
    "category": "Import-Export",
}

import bpy
import os
import datetime
import mathutils
from bpy.props import BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy_extras.io_utils import ExportHelper

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def stl_operator_available():
    return hasattr(bpy.ops.export_mesh, "stl")

def get_unit_and_scale(context, use_custom, custom_scale):
    unit_name = context.scene.unit_settings.length_unit
    scale_map = {
        'METERS': 1000.0,
        'CENTIMETERS': 10.0,
        'MILLIMETERS': 1.0,
        'NONE': 1000.0,
    }
    if use_custom:
        return f"Custom ({custom_scale:.3f})", float(custom_scale)
    return unit_name, scale_map.get(unit_name, 1000.0)

def compute_selection_preview(context, scale_factor):
    sel = [o for o in context.selected_objects if o.type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}]
    lines = []
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    for obj in sel:
        dx = obj.dimensions.x * scale_factor
        dy = obj.dimensions.y * scale_factor
        dz = obj.dimensions.z * scale_factor
        lines.append(f"{obj.name}: X={dx:.2f} mm, Y={dy:.2f} mm, Z={dz:.2f} mm")

        bbox_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        for v in bbox_world:
            min_x = min(min_x, v.x)
            min_y = min(min_y, v.y)
            min_z = min(min_z, v.z)
            max_x = max(max_x, v.x)
            max_y = max(max_y, v.y)
            max_z = max(max_z, v.z)

    if not sel:
        total_str = "Keine Auswahl"
    else:
        total_dims = ((max_x - min_x) * scale_factor,
                      (max_y - min_y) * scale_factor,
                      (max_z - min_z) * scale_factor)
        total_str = f"Gesamt-BBox: X={total_dims[0]:.2f} mm, Y={total_dims[1]:.2f} mm, Z={total_dims[2]:.2f} mm"

    return "\n".join(lines), total_str

def write_log(file_path, scale_factor, unit_display, selected_names, total_bbox_str):
    log_dir = bpy.utils.user_resource('SCRIPTS', "stl_export_logs", create=True)
    log_file = os.path.join(log_dir, "stl_export_log.txt")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] Exported: {file_path}, Scale: {scale_factor:.6f}, Unit: {unit_display}, Objects: {', '.join(selected_names)}, {total_bbox_str}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    return log_file, entry

def update_preview_live(context):
    props = context.scene.smart_stl_props
    unit_display, scale_factor = get_unit_and_scale(context, props.use_custom, props.custom_scale)
    preview, total = compute_selection_preview(context, scale_factor)
    props.preview_sizes = preview
    props.total_bbox = total
    props.unit_display = unit_display

# -------------------------------------------------------------------
# Properties
# -------------------------------------------------------------------

class SmartSTLProperties(bpy.types.PropertyGroup):
    use_custom: BoolProperty(name="Custom Scale verwenden", default=False)
    custom_scale: FloatProperty(name="Custom Scale Faktor", default=1.0, min=0.0001, max=100000.0)
    preview_sizes: StringProperty(name="Vorschau (mm)", default="")
    total_bbox: StringProperty(name="Gesamt-BBox (mm)", default="")
    unit_display: StringProperty(name="Einheit", default="")
    last_log: StringProperty(name="Letzter Log-Eintrag", default="")

# -------------------------------------------------------------------
# Export Operator
# -------------------------------------------------------------------

class EXPORT_OT_smart_stl(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.smart_stl_live"
    bl_label = "Export Smart STL"
    bl_options = {'PRESET'}
    filename_ext = ".stl"

    def invoke(self, context, event):
        update_preview_live(context)
        return super().invoke(context, event)

    def execute(self, context):
        props = context.scene.smart_stl_props
        if not stl_operator_available():
            self.report({'ERROR'}, "STL-Export-Modul nicht aktiviert.")
            return {'CANCELLED'}

        unit_display, scale_factor = get_unit_and_scale(context, props.use_custom, props.custom_scale)

        try:
            bpy.ops.export_mesh.stl(
                filepath=self.filepath,
                use_selection=True,
                global_scale=scale_factor,
                ascii=False
            )
        except Exception as e:
            self.report({'ERROR'}, f"Export fehlgeschlagen: {e}")
            return {'CANCELLED'}

        selected_names = [o.name for o in context.selected_objects]
        log_path, entry = write_log(self.filepath, scale_factor, unit_display, selected_names, props.total_bbox)
        props.last_log = entry
        self.report({'INFO'}, f"Export abgeschlossen. Log gespeichert.")
        return {'FINISHED'}
# -------------------------------------------------------------------
# Log öffnen Operator
# -------------------------------------------------------------------

class TEXT_OT_open_stl_log(bpy.types.Operator):
    bl_idname = "text.open_smart_stl_log"
    bl_label = "Logfile öffnen"

    def execute(self, context):
        log_dir = bpy.utils.user_resource('SCRIPTS', "stl_export_logs", create=True)
        log_file = os.path.join(log_dir, "stl_export_log.txt")

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                text_data = f.read()
            text_block = bpy.data.texts.get("STL_Export_Log")
            if not text_block:
                text_block = bpy.data.texts.new("STL_Export_Log")
            text_block.clear()
            text_block.write(text_data)
            for area in context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    area.spaces.active.text = text_block
                    break
            self.report({'INFO'}, "STL Export Log im Texteditor geöffnet.")
        else:
            self.report({'WARNING'}, "Kein Logfile gefunden.")
        return {'FINISHED'}

# -------------------------------------------------------------------
# N-Panel
# -------------------------------------------------------------------

class VIEW3D_PT_smart_stl(bpy.types.Panel):
    bl_label = "Smart STL"
    bl_idname = "VIEW3D_PT_smart_stl_live"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Smart STL'

    def draw(self, context):
        layout = self.layout
        props = context.scene.smart_stl_props

        if not stl_operator_available():
            layout.label(text="STL-Export-Modul nicht aktiviert!", icon='ERROR')
            layout.label(text="Preferences > Add-ons > 'Import-Export: STL format'")
            return

        box = layout.box()
        box.label(text="Einheiten & Skalierung")
        row = box.row()
        row.prop(props, "use_custom", text="Custom Scale verwenden")
        box.prop(props, "custom_scale")

        box2 = layout.box()
        box2.label(text=f"Erkannte Einheit: {props.unit_display}")
        box2.label(text="Vorschau (mm):")
        box2.prop(props, "preview_sizes", text="")
        box2.label(text="Gesamt-Bounding-Box (mm):")
        box2.prop(props, "total_bbox", text="")

        layout.separator()
        layout.operator(EXPORT_OT_smart_stl.bl_idname, text="Export STL")
        layout.operator(TEXT_OT_open_stl_log.bl_idname, text="Logfile öffnen")

        layout.separator()
        layout.label(text="Letzter Log-Eintrag:")
        layout.prop(props, "last_log", text="")

# -------------------------------------------------------------------
# Scene Handler für Live-Update
# -------------------------------------------------------------------

def smart_stl_scene_update(scene):
    try:
        update_preview_live(bpy.context)
    except Exception:
        pass

# -------------------------------------------------------------------
# Register / Unregister
# -------------------------------------------------------------------

classes = (
    SmartSTLProperties,
    EXPORT_OT_smart_stl,
    TEXT_OT_open_stl_log,
    VIEW3D_PT_smart_stl,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.smart_stl_props = PointerProperty(type=SmartSTLProperties)
    bpy.app.handlers.depsgraph_update_post.append(smart_stl_scene_update)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.smart_stl_props
    if smart_stl_scene_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(smart_stl_scene_update)

if __name__ == "__main__":
    register()
