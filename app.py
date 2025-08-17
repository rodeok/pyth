from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_images(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    img_tags = soup.find_all("img")
    images = []

    for img in img_tags:
        img_url = img.get("src") or img.get("data-src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)

        images.append(img_url)

    return images


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", message="❌ Please enter a valid URL.")

        images = scrape_images(url)

        if not images:
            return render_template("index.html", message="⚠️ No images found.")

        return render_template("index.html", images=images)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
