bl_info = {
    "name": "Simulador de lluvia",
    "author": "Octavio Gregorio Guerrero",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools",
    "description": "Simulador de lluvia",
    "category": "Object"
}

import bpy

class SimuladorDeLluvia(bpy.types.Panel):
    bl_label = "Simulador de lluvia"
    bl_idname = "Simulador_de_lluvia"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Configuración de la lluvia:")
        layout.prop(scene, "intensidad")
        layout.operator("object.crea_lluvia", text="Iniciar lluvia")
        layout.operator("object.inicia_deten_lluvia", text="Iniciar/Detener lluvia")
        layout.operator("object.crea_escena", text="Crear Escenario")

class IniciaLluvia(bpy.types.Operator):
    bl_idname = "object.crea_lluvia"
    bl_label = "Inicia Lluvia"

    def execute(self, context):
        scene = context.scene
        scene["inicia_lluvia"] = True        
        
        
        #Creamos partículas para la lluvia
        
        
        bpy.ops.object.particle_system_add()

        
        # Creaamos el splash
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1, location=(100, 0, 0))
        bpy.ops.object.shade_smooth()
        splash = bpy.context.object
    

        # Creaamos la gota
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(100, 0, 0))
        gota = bpy.context.object
        gota.scale = (0.5, 0.5, 1.3)
    


       # bpy.context.object.modifiers["Dynamic"].ui_type = 'BRUSH'
       # bpy.ops.dpaint.type_toggle(type='BRUSH')
       # bpy.context.object.modifiers["Dynamic Paint"].brush_settings.paint_source = 'PARTICLE_SYSTEM'
       # bpy.context.object.modifiers["Dynamic Paint"].brush_settings.particle_system = bpy.data.objects["Plane.001"].particle_systems["ParticleSystem"]

        # Obtener el objeto con partículas existente
        plano = bpy.data.objects['Plane.001']

        # Acceder a la configuración de partículas del objeto
        particle_settings = plano.particle_systems[0].settings  # Ajusta el índice adecuado si hay múltiples sistemas de partículas
        
        
        particle_settings.count = int(scene.intensidad * 2000)
        particle_settings.frame_start = -100
        particle_settings.frame_end = 200
        particle_settings.size_random = 0.5

       
        particle_settings.render_type = 'OBJECT'

        
        gota = bpy.data.objects['Sphere']

        # Establecer la gota como objeto de renderizado
        particle_settings.instance_object = gota
        
    
       ############################# 

        plano2 = bpy.data.objects['Plane']
        modificador_colision = plano2.modifiers.new(name="Colisión", type='COLLISION')
        
        
        modificador_part = plano2.modifiers.new(name="Particulas", type='PARTICLE_SYSTEM')
        bpy.data.particles["ParticleSettings"].count = 2000
        bpy.data.particles["ParticleSettings"].frame_start = 0
        bpy.data.particles["ParticleSettings"].lifetime = 10

        bpy.context.scene.frame_end = 200
        
        particle_settings = plano2.particle_systems[0].settings

        
        particle_settings.count = int(scene.intensidad * 1000)
        particle_settings.frame_start = 0
        particle_settings.lifetime = 10
        particle_settings.lifetime = 10
        particle_settings.particle_size = 0.025
        particle_settings.size_random = 0.5


        particle_settings.render_type = 'OBJECT'

        splash = bpy.data.objects['Icosphere']

        particle_settings.instance_object = splash
        

        
        #hacemos que el suelo responda a las gotas
        modificador_subdivision = plano2.modifiers.new(name="Subdi", type='SUBSURF')
        modificador_subdivision.subdivision_type = 'SIMPLE'
        modificador_subdivision.levels = 7
        bpy.ops.object.shade_smooth()
        
        modificador_dynamic = plano2.modifiers.new(name="Dynamic", type='DYNAMIC_PAINT')
        bpy.ops.dpaint.type_toggle(type='CANVAS')
            
        #bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"].surface_type = 'WAVE'
        #bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"].brush_influence_scale = 0.5
        #bpy.context.object.modifiers["Dynamic"].ui_type = 'BRUSH'
        #bpy.context.object.modifiers["Dynamic"].brush_settings.paint_source = 'PARTICLE_SYSTEM'
        #bpy.context.object.modifiers["Dynamic"].brush_settings.particle_system = bpy.data.objects["Plane.001"].particle_systems["ParticleSystem"]
        
        
        # creamos los keyframes para el movimiento de la nube
        
        bpy.ops.object.select_all(action='DESELECT')

        obj1 = bpy.data.objects["Plane.001"]
        obj2 = bpy.data.objects["Area"]


        obj1.select_set(True)
        obj2.select_set(True)


        
        obj1.location.x = +15
        obj2.location.x = +15
        
        obj1.keyframe_insert(data_path="location", frame=500)
        obj2.keyframe_insert(data_path="location", frame=500)

        obj1.location.x = -5
        obj2.location.x = -5
        
        obj1.keyframe_insert(data_path="location", frame=1)
        obj2.keyframe_insert(data_path="location", frame=1)
        
        return {'FINISHED'}


class IniDetLluvia(bpy.types.Operator):
    bl_idname = "object.inicia_deten_lluvia"
    bl_label = "Ini Det Lluvia"

    def execute(self, context):
        scene = context.scene
        scene["inicia_lluvia"] = False
        
        bpy.ops.screen.animation_play()

        return {'FINISHED'}

class CreaEscena(bpy.types.Operator):
    bl_idname = "object.crea_escena"
    bl_label = "Crea Escena"

    def execute(self, context):
        # Eliminar objetos existentes en la escena
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        
        for obj in bpy.context.selected_objects:
            # Verificar si el objeto tiene materiales
            if obj.type == 'MESH' and obj.data.materials:
                # Eliminar cada material del objeto
                for material_slot in obj.material_slots:
                    material = material_slot.material
                    if material:
                        bpy.data.materials.remove(material)
                obj.data.materials.clear()
                    
        bpy.ops.object.delete()

    
        bpy.ops.object.select_by_type(type='LIGHT')
        bpy.ops.object.delete()
        
        bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 15), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.046959, -0.998897, 2.04192e-07), (-0.0759307, -0.00356941, 0.997107), (-0.996007, -0.0468232, -0.0760146)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.context.object.data.energy = 4
        bpy.context.object.data.color = (0.358841, 0.0924809, 0.0133396)
        
        
        bpy.ops.object.light_add(type='AREA', radius=48, align='WORLD', location=(0, 0, 16), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

        #bpy.context.object.data.energy = 40000
        bpy.context.object.data.energy = 20000
        bpy.context.object.data.color = (0.241607, 0.356979, 0.367238)


        
        # Crear el primer plano
        bpy.ops.mesh.primitive_plane_add(size=100)
        plane1 = bpy.context.object
        plane1.location.z = 0

        # Crear el segundo plano
        bpy.ops.mesh.primitive_plane_add(size=20)
        plane2 = bpy.context.object
        plane2.location.z = 15
        
        #NUBE
        bpy.ops.object.modifier_add(type='OCEAN')
        bpy.context.object.modifiers["Ocean"].spectrum = 'PIERSON_MOSKOWITZ'
        bpy.context.object.modifiers["Ocean"].viewport_resolution = 10
        bpy.context.object.modifiers["Ocean"].choppiness = 1.15
        bpy.context.object.modifiers["Ocean"].wave_scale = 1.5
        bpy.context.object.modifiers["Ocean"].viewport_resolution = 15
        bpy.ops.object.modifier_apply(modifier="Ocean")
        
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 4), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.mesh.edge_face_add()
        bpy.ops.transform.translate(value=(-0, -0, -1.95055), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        
        
        # Obtén una referencia al objeto al que deseas asignar el material
        nombre_objeto = "Plane.001"
        objeto = bpy.data.objects[nombre_objeto]

        # Crea un nuevo material
        nombre_material = "Prueba"
        material = bpy.data.materials.new(name=nombre_material)
        material.use_nodes = True

        objeto.data.materials.append(material)
        
        objeto.active_material_index = 0
        
        material = bpy.data.materials["Prueba"]


        nodo_materiales = material.node_tree.nodes


        for enlace in material.node_tree.links:

                material.node_tree.links.remove(enlace)


        nodo_principled_volume = nodo_materiales.new(type='ShaderNodeVolumePrincipled')


        nodo_output = nodo_materiales.get('Material Output') 
        enlace_volume = material.node_tree.links.new(nodo_principled_volume.outputs['Volume'], nodo_output.inputs['Volume'])
        
        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].strength = -0.25
    

        plane2
        
        
        


        


        return {'FINISHED'}

def register():
    bpy.types.Scene.intensidad = bpy.props.FloatProperty(
        name="Intensidad",
        description="Intensidad de la lluvia",
        default=0.5,
        min=0.0,
        max=5.0
    )
    bpy.types.Scene.inicia_lluvia = bpy.props.BoolProperty(default=False)

    bpy.utils.register_class(SimuladorDeLluvia)
    bpy.utils.register_class(IniciaLluvia)
    bpy.utils.register_class(IniDetLluvia)
    bpy.utils.register_class(CreaEscena)


def unregister():
    bpy.utils.unregister_class(SimuladorDeLluvia)
    bpy.utils.unregister_class(IniciaLluvia)
    bpy.utils.unregister_class(IniDetLluvia)
    bpy.utils.unregister_class(CreaEscena)
    del bpy.types.Scene.intensidad
    del bpy.types.Scene.inicia_lluvia


if __name__ == "__main__":
    register()
