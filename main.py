from flask import Flask, render_template, request, send_file, Response
from scraper import scrape_and_process_text, save_scraped_text
import os
from datetime import datetime
from ai_filter import generate_frames
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

# Create a directory to store scraped text files if it doesn't exist
os.makedirs('scraped_text', exist_ok=True)

@app.route('/')
def main():
    # Render the main HTML page
    return render_template('main.html')

@app.route('/ai-filter')
def ai_filter():
    # Render the AI filter HTML page
    return render_template('ai_filter.html')

@app.route('/video_feed')
def video_feed():
    global camera
    if not camera.isOpened():
        # Open the camera if it is not already opened
        camera = cv2.VideoCapture(0)
    # Return the video feed as a response
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    scraped_text = None
    download_filename = None

    if request.method == 'POST':
        # Get the URL from the submitted form
        url = request.form.get('url')
        if url:
            # Generate a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'scraped_text_{timestamp}.txt'
            filepath = os.path.join('scraped_text', filename)

            # Scrape the text from the provided URL
            text = scrape_and_process_text(url)
            # Save the scraped text to a file
            save_scraped_text(filepath, text)

            # Prepare the scraped text and filename for rendering
            scraped_text = text
            download_filename = filename

    # Render the scraper results page
    return render_template('scraper.html', scraped_text=scraped_text, download_filename=download_filename)

@app.route('/download/<filename>')
def download_file(filename):
    # Prepare the filepath for the file to be downloaded
    filepath = os.path.join('scraped_text', filename)
    # Send the file as an attachment for download
    return send_file(filepath, as_attachment=True)

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    camera.release()  # Release the camera
    return '', 204  # Return an empty response with status 204 (No Content)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)