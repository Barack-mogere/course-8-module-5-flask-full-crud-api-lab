from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get the JSON data sent by the client
    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    # Make sure the event has a title
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create a new ID
    new_id = max(event.id for event in events) + 1

    # Create the new event
    new_event = Event(new_id, data["title"])

    # Add the event to our in-memory list
    events.append(new_event)

    # Return the new event
    return jsonify(new_event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get the JSON data from the request
    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    # Find the event with the requested ID
    for event in events:
        if event.id == event_id:

            # Make sure a title was provided
            if "title" not in data:
                return jsonify({"error": "Title is required"}), 400

            # Update the event title
            event.title = data["title"]

            # Return the updated event
            return jsonify(event.to_dict()), 200

    # If the event wasn't found
    return jsonify({"error": "Event not found"}), 404

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event with the requested ID
    for event in events:
        if event.id == event_id:

            # Remove the event from the list
            events.remove(event)

            # Return a successful 204 response
            return "", 204

    # If the event wasn't found
    return jsonify({"error": "Event not found"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)
