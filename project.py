from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable Cross-Origin Resource Sharing

# Mock Database
courses = [
    {
        "id": 1,
        "name": "Web Development",
        "description": "Master front-end and back-end development with hands-on projects.",
        "image": "web.jpg",
    },
    {
        "id": 2,
        "name": "Graphic Design",
        "description": "Learn design principles and tools to create stunning visuals.",
        "image": "graphic.jpg",
    },
    {
        "id": 3,
        "name": "Digital Marketing",
        "description": "Grow your brand and career with modern marketing strategies.",
        "image": "digital.jpg",
    },
]

enrollments = []  # Store enrollments


# Routes

@app.route("/")
def home():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """API endpoint to fetch all courses."""
    return jsonify(courses)


@app.route("/api/enroll", methods=["POST"])
def enroll_course():
    """API endpoint to enroll in a course."""
    data = request.json
    name = data.get("name")
    email = data.get("email")
    course_id = data.get("courseId")

    # Validation
    if not name or not email or not course_id:
        return jsonify({"error": "All fields are required!"}), 400

    # Find course
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found!"}), 404

    # Save enrollment
    enrollments.append({"name": name, "email": email, "courseId": course_id})
    return jsonify({"message": f"Successfully enrolled in {course['name']}"})


@app.route("/api/enrollments", methods=["GET"])
def get_enrollments():
    """API endpoint to fetch all enrollments (Admin feature)."""
    return jsonify(enrollments)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
