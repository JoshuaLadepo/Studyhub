from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Atomic Habits",
        "available": True
    },
    {
        "id": 2,
        "title": "The Psychology of Money",
        "available": False
    },
    {
        "id": 3,
        "title": "Deep Work",
        "available": True
    }
]

for book in books:
    if book["id"]==2 :
        print(book["title"])

data = {
    "available": False
}
if data is None or "available" not in data or not isinstance(data["available"], bool):
    print("Invalid data: 'available' field is required and must be a boolean.")

@app.route("/api/books/<int:book_id>",methods=["GET"])
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify(error= "Book not found"), 404

@app.route("/api/books", methods = ["POST"])
def post_book():
    new_book = request.get_json()
    if new_book is None:
        return jsonify(error = "cannot enter an empty book Title") , 400
    title = new_book.get("title")
    if  not isinstance(title,str) or not title.strip()  :
        return jsonify(error = "Incorrect format"), 400
    
    new_book["id"]= len(books)+1 
    new_book["available"]= True 
    books.append(new_book)
    return jsonify(new_book), 201
    
    
        








if __name__ == "__main__":
    app.run(debug=True)
