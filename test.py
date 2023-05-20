from flask import Flask, render_template, send_file, send_from_directory
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import tempfile

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

def convert_svg_to_png(svg_content):
    # Parse the SVG content to get width and height
    svg_tree = etree.fromstring(svg_content.encode())
    width = int(float(svg_tree.get("width", "800")))
    height = int(float(svg_tree.get("height", "600")))

    # Set the browser window size to match the SVG dimensions
    driver.set_window_size(width, height)

    # Create a temporary file to store the SVG content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as svg_file:
        svg_file.write(svg_content)
        svg_file.flush()

        # Load the SVG file in the existing WebDriver instance
        driver.get(f"file:///{svg_file.name}")

        # Capture the screenshot as PNG
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False) as png_file:
            driver.get_screenshot_as_file(png_file.name)

    return png_file.name

@app.route('/svg')
def svg():
    # Render the SVG template with the desired text
    svg_content = render_template('template.svg', placeholder_text='Hello, World!')
    return svg_content, 200, {'Content-Type': 'image/svg+xml'}

@app.route('/png')
def png():
    # Render the SVG template with the desired text
    svg_content = render_template('template.svg', placeholder_text='Hello, World!')

    # Convert the SVG content to a PNG
    png_file_path = convert_svg_to_png(svg_content)

    # Serve the PNG image
    return send_file(png_file_path, mimetype='image/png', as_attachment=False)

@app.route('/fonts/<path:filename>')
def send_font(filename):
    return send_from_directory('fonts', filename)

if __name__ == '__main__':
    app.run(debug=True)
