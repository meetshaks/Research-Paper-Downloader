
# Research Paper Downloader

This is a web application designed to streamline the process of searching and downloading research papers. Built using Flask, this app provides a user-friendly interface and powerful features to assist researchers, students, and professionals in accessing academic papers with ease.

---

## Features

- **Simple Search Interface**: Users can search for research papers by title, author, or keywords.
- **Download Options**: Provides direct download links for open-access papers.
- **Flask Backend**: Handles search requests and integrates with APIs/databases to fetch papers.
- **Responsive Design**: The interface is built using HTML templates for a seamless user experience.

---

## Project Structure

- **`app.py`**:  
  This is the main Flask application file that defines routes, handles user requests, and integrates the backend logic.

- **`templates/index.html`**:  
  The front-end interface for the application. It features a clean and responsive design to make searching and downloading papers intuitive.

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/meetshaks/Research-Paper-Downloader.git
   cd Research-Paper-Downloader/V3
   ```

2. Install dependencies:
   ```bash
   pip install Flask
   pip install scholarly
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Future Enhancements

- Integrate with academic databases like PubMed, IEEE Xplore, or Springer.
- Add user authentication for personalized features.
- Implement advanced filters for refined search results.

---

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Follow the standard GitHub workflow for contributions.

---

## License

This project is licensed under the MIT License.
