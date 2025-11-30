from flask import Blueprint, request, jsonify
import json
import os

api_bp = Blueprint('api', __name__)

# Ruta al archivo JSON de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, '..', 'app', 'data', 'base_del_proto.json')

def load_json_data():
    """Carga el JSON y devuelve (candidatos, es_objeto)"""
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and "candidatos" in data:
            return data["candidatos"], True
        else:
            return data, False
    except FileNotFoundError:
        # Crear archivo vacío si no existe
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return [], False
    except Exception as e:
        print(f"❌ Error cargando JSON: {e}")
        return [], False

def save_json_data(candidatos, es_objeto):
    """Guarda los datos en el formato correcto"""
    try:
        if es_objeto:
            data = {"candidatos": candidatos}
        else:
            data = candidatos
            
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Error guardando JSON: {e}")

@api_bp.route('/api/records', methods=['GET'])
def get_records():
    """Obtiene todos los registros"""
    try:
        candidatos, _ = load_json_data()
        print(f"📊 Enviando {len(candidatos)} registros al frontend")
        return jsonify(candidatos)
    except Exception as e:
        print(f"❌ Error en /api/records: {e}")
        return jsonify({"error": "Error cargando registros"}), 500

@api_bp.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Elimina un registro"""
    try:
        candidatos, es_objeto = load_json_data()
        
        # Filtrar el registro a eliminar
        nuevos_candidatos = [c for c in candidatos if c.get("ID") != record_id]
        
        if len(nuevos_candidatos) == len(candidatos):
            return jsonify({"error": "Registro no encontrado"}), 404
        
        save_json_data(nuevos_candidatos, es_objeto)
        return jsonify({"message": "Registro eliminado"})
    except Exception as e:
        print(f"Error deleting record: {e}")
        return jsonify({"error": "Error eliminando registro"}), 500

@api_bp.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """Actualiza un registro"""
    try:
        candidatos, es_objeto = load_json_data()
        
        # Buscar y actualizar el registro
        for candidato in candidatos:
            if candidato.get("ID") == record_id:
                candidato.update(request.json)
                save_json_data(candidatos, es_objeto)
                return jsonify({"message": "Registro actualizado"})
        
        return jsonify({"error": "Registro no encontrado"}), 404
    except Exception as e:
        print(f"Error updating record: {e}")
        return jsonify({"error": "Error actualizando registro"}), 500

@api_bp.route('/api/predict_all', methods=['POST'])
def predict_all():
    """Genera predicciones IA para todos los registros (placeholder)"""
    try:
        candidatos, es_objeto = load_json_data()
        
        # Placeholder simple basado en experiencia
        for candidato in candidatos:
            experiencia = candidato.get("Experiencia (años)", 0)
            
            if experiencia > 10:
                candidato["Prediccion_IA"] = "Senior"
            elif experiencia > 5:
                candidato["Prediccion_IA"] = "Mid-Level" 
            elif experiencia > 2:
                candidato["Prediccion_IA"] = "Junior"
            else:
                candidato["Prediccion_IA"] = "Trainee"
        
        save_json_data(candidatos, es_objeto)
        return jsonify({
            "msg": f"✅ Predicciones IA generadas para {len(candidatos)} registros",
            "records": candidatos
        })
    except Exception as e:
        print(f"Error generating predictions: {e}")
        return jsonify({"error": "Error generando predicciones"}), 500