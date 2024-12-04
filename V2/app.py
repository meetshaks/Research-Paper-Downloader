from flask import Flask, render_template, request, send_from_directory
import os
import itertools
from scholarly import scholarly

app = Flask(__name__)

# Folder to store the generated files
DOWNLOAD_FOLDER = 'static/downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to get top-cited papers for a specific dataset and author
def get_top_cited_papers(query, num_results=10):
    results = []
    for i, paper in enumerate(query):
        if i >= num_results:
            break
        title = paper['bib']['title']
        citations = paper['num_citations']
        # Safely check if 'url' key exists
        url = paper.get('url', 'URL not available')
        author = paper['bib'].get('author', 'Author not available')
        results.append((title, citations, url, author))
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the comma-separated datasets input by the user
        dataset_names = request.form['datasets'].split(',')
        dataset_names = [name.strip() for name in dataset_names]  # Remove extra spaces

        # Get the author name input (optional)
        author_name = request.form.get('author', '').strip()

        # If the user entered nothing or empty datasets, return an error
        if not dataset_names or any(name == "" for name in dataset_names):
            return "Please enter valid dataset names."

        # Get the number of papers to fetch
        try:
            num_papers = int(request.form['num_papers'])
        except ValueError:
            return "Please enter a valid number for papers."
        
        # Generate the search query for the entered datasets
        if author_name:
            query = f"({' AND '.join(dataset_names)}) AND author:{author_name}"
        else:
            query = " AND ".join(dataset_names)

        # Generate the filename for the download
        filename = f"papers_for_{'_'.join(dataset_names)}_{num_papers}_results"
        if author_name:
            filename += f"_author_{author_name}"
        filename += ".txt"
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

        # Open the file to write results
        with open(file_path, 'w', encoding='utf-8') as file:
            # Generate all possible combinations of the entered datasets
            for r in range(1, len(dataset_names) + 1):  # r = 1 to len(datasets) for all combinations
                for combination in itertools.combinations(dataset_names, r):
                    # Create the search query for the current combination
                    query_combination = " AND ".join(combination)
                    if author_name:
                        query_combination = f"({query_combination}) AND author:{author_name}"

                    # Write the combination as a header
                    file.write(f"Results for: {', '.join(combination)}{', ' + author_name if author_name else ''}\n")
                    file.write("=" * 50 + "\n")

                    # Search for papers related to the current combination
                    search_query = scholarly.search_pubs(query_combination)

                    # Get top papers based on citations
                    top_papers = get_top_cited_papers(search_query, num_results=num_papers)

                    # Write the results to the text file
                    for idx, paper in enumerate(top_papers):
                        file.write(f"{idx + 1}. Title: {paper[0]}\n")
                        file.write(f"   Citations: {paper[1]}\n")
                        file.write(f"   URL: {paper[2]}\n")
                        file.write(f"   Author: {paper[3]}\n\n")
                    
                    # Add a separator between combinations
                    file.write("=" * 50 + "\n\n")

        # Return the file for download
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
