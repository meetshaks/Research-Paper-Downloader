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

# Function to get top-cited papers for a specific query
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
        search_type = request.form['search_type']
        dataset_names = request.form.get('datasets', '').strip().split(',')
        dataset_names = [name.strip() for name in dataset_names]  # Clean up any spaces
        topic_name = request.form.get('topic', '').strip()
        author_name = request.form.get('author', '').strip()
        try:
            num_papers = int(request.form['num_papers'])
        except ValueError:
            return "Please enter a valid number for papers."
        
        # Based on search type, build query
        query_parts = []
        
        # Handle Dataset search type
        if 'Dataset' in search_type and dataset_names:
            # If only Dataset is selected, include combinations as well
            combinations = []
            for r in range(1, len(dataset_names) + 1):  # Generate all combinations (1 to N datasets)
                combinations.extend(itertools.combinations(dataset_names, r))
            query_parts = [(" AND ".join(combination)) for combination in combinations]
        
        # Handle other search types (Topic and Author)
        if 'Topic' in search_type and topic_name:
            query_parts = [f"topic:{topic_name}"]
        
        if 'Author' in search_type and author_name:
            query_parts = [f"author:{author_name}"]

        # If no valid fields are filled out, return an error
        if not query_parts:
            return "Please select at least one valid search option (Dataset, Author, or Topic)."

        # Generate the filename for the download
        filename = f"papers_{search_type.replace(' ', '_')}_{num_papers}_results.txt"
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

        # Open the file to write results
        with open(file_path, 'w', encoding='utf-8') as file:
            if 'Dataset' in search_type:
                file.write("Searched By: Dataset(s) and Combinations\n")
                file.write("=" * 50 + "\n")
            else:
                file.write(f"Searched By: {search_type}\n")
                file.write("=" * 50 + "\n")
            
            # Perform search for each combination
            for query in query_parts:
                file.write(f"Query: {query}\n")
                file.write("=" * 50 + "\n")
                search_query = scholarly.search_pubs(query)
                top_papers = get_top_cited_papers(search_query, num_results=num_papers)

                # Write results to the file
                for idx, paper in enumerate(top_papers):
                    file.write(f"{idx + 1}. Title: {paper[0]}\n")
                    file.write(f"   Citations: {paper[1]}\n")
                    file.write(f"   URL: {paper[2]}\n")
                    file.write(f"   Author: {paper[3]}\n\n")
                
                file.write("=" * 50 + "\n")

        # Return the file for download
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
