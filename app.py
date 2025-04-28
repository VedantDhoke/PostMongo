from flask import Flask, jsonify, request
from pymongo import MongoClient
# from flask_cors import CORS
import datetime

app = Flask(__name__)
# CORS(app)

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['pracs']
notes_collection = db['pracs']

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
    
    result  = notes_collection.delete_one({"title": body['title']})
    
    if result.deleted_count == 1:
        return jsonify({'message': f"Note with title '{body['title']}' deleted successfully"}), 200
    else:
        return jsonify({'error': f"No note found with title '{body['title']}'"}), 404



if __name__ == '__main__':
    app.run(debug=True)