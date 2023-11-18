from flask import Flask, render_template
import re

app = Flask(__name__)

def parse_text_and_images(text):
    # Split text into paragraphs
    paragraphs = text.split('###################################################\n\n')

    # Use regular expression to find image URLs and create <img> tags
    summary_and_images = []
    for paragraph in paragraphs:
        # Split each paragraph into summary and image
        parts = paragraph.split('\n\n')
        summary = parts[0].replace('Summary:\n', '')
        img_tags = ''
        if len(parts) > 1:
            image_urls = re.findall(r'(https?://[^\s]+)', parts[1])
            for url in image_urls:
                img_tags += f'<img src="{url}" alt="Image">\n'
        summary_and_images.append((summary, img_tags))

    return summary_and_images

@app.route('/')
def index():
    try:
        # Read the content from the 'save_data' file
        with open('../save_data.txt', 'r', encoding='utf-8') as file:
            data = file.read()

        # Parse text and images, combining them into a list of tuples
        summary_and_images = parse_text_and_images(data)
    except FileNotFoundError:
        summary_and_images = []

    return render_template('index.html', summary_and_images=summary_and_images)

if __name__ == '__main__':
    app.run(debug=True)
