from flask import Flask, jsonify, request
from pymongo import MongoClient
# from flask_cors import CORS
import datetime

app = Flask(__name__)
# CORS(app)

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['pracs']
notes_collection = db['pracs_collection'] 

@app.route('/getNotes', methods=['GET'])
def getNotes():
    notes = list(notes_collection.find())
    for note in notes:
        note['_id'] = str(note['_id'])
    return jsonify(notes)

@app.route('/postNotes', methods=['POST'])
def postNotes():
    note = request.get_json()
    if not note or 'title' not in note or 'content' not in note:
        return jsonify({'error': 'Both title and content are required'}), 400
    
    note['created_date'] = datetime.datetime.now()
    result = notes_collection.insert_one(note)
    
    return jsonify({
        'acknowledged': result.acknowledged,
        'inserted_id': str(result.inserted_id)
    }), 201

@app.route('/deleteNote', methods=['DELETE'])
def deleteNote():
    body = request.get_json()
    if not body or 'title' not in body:
        return jsonify({'error': 'Title is required to delete note'}), 400
    
    result = notes_collection.delete_one({"title": body['title']})
    
    if result.deleted_count == 1:
        return jsonify({'message': f"Note with title '{body['title']}' deleted successfully"}), 200
    else:
        return jsonify({'error': f"No note found with title '{body['title']}'"}), 404

@app.route('/updateNote', methods=['PUT'])
def updateNote():
    body = request.get_json()
    if not body or 'title' not in body or 'content' not in body:
        return jsonify({'error': 'Both title and new content are required for updating'}), 400
    
    filter_query = {"title": body['title']}
    new_values = {"$set": {"content": body['content'], "updated_date": datetime.datetime.now()}}
    
    result = notes_collection.update_one(filter_query, new_values)
    
    if result.matched_count == 0:
        return jsonify({'error': f"No note found with title '{body['title']}'"}), 404
    
    return jsonify({'message': f"Note with title '{body['title']}' updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
