import json
import pickle
import pandas as pd
from pathlib import Path

PICKLE_CACHE_DIR = Path("pickle_cache")
    

def write_bib(paper):
    """
    Generate a BibTeX entry from a paper dictionary.
    
    Parameters
    ----------
    paper : dict
        A dictionary containing bibliographic information under the "bib" key.
    
    Returns
    -------
    str
        A string representation of the paper in BibTeX format.
    """
    bib_entry = paper.get("bib", {})
    bib_str = f"@article{{{bib_entry.get('bib_id')},\n"
    for key, value in bib_entry.items():
        if key != "bib_id":
            bib_str += f"  {key} = {{{value}}},\n"
    bib_str += "}\n\n"
    return bib_str

def read_pickles(directory): 
    """
    Read and deserialize all pickle files in a directory.
    
    Parameters
    ----------
    directory : Path
        A pathlib.Path object representing the directory containing pickle files.
    
    Returns
    -------
    list of dict
        A list of dictionaries, each representing a deserialized paper object 
        with an added "query" key set to the name of the directory it was found in.
    """
    papers = []
    for dirpath, __, filenames in directory.walk():
        for file in filenames:
            if not file.endswith('.pickle'):
                continue
            path = dirpath / file
            
            with open(path, 'rb') as f:
                paper = pickle.load(f)
                paper['query'] = dirpath.stem
                
                papers.append(paper)       
    return papers
 
    
def filter_data(papers):
    """
    Extract relevant metadata from a list of paper dictionaries and generate BibTeX entries.
    
    Parameters
    ----------
    papers : list of dict
        A list of dictionaries, each containing bibliographic information 
        under the "bib" key and other metadata.
    
    Returns
    -------
    results : list of dict
        List of paper metadata including title, authors, 
          year, venue, abstract, citations, URL, and query.

    bib_entries: list of str
        List of BibTex entries 
    """
    results = []
    bib_entries = []
    for paper in papers:                
        entry = {
                "title": paper.get("bib", {}).get("title", "N/A"),
                "authors": str(paper.get("bib", {}).get("author", "N/A")),
                "year": paper.get("bib", {}).get("pub_year", "N/A"),
                "venue": paper.get("bib", {}).get("venue", "N/A"),
                "abstract": paper.get("bib", {}).get("abstract", "N/A"),
                "citations": paper.get("num_citations", 0),
                "url": paper.get("pub_url", "N/A"),
                "query": paper.get("query")
            }
            
        results.append(entry)
        bib_entry = write_bib(paper)
        bib_entries.append(bib_entry)
                
    return results, bib_entries


def save_results(results, bib_entries, output_json, output_csv, output_bib):
    """
    Save the results to a JSON, csv and bib file.

    Parameters
    ----------
    results : list
        List of dictionaries containing paper metadata.
        
    bib_entries : list
        List of strings containing BibTex entries. 
        
    output_json : str
        Path to the output JSON file.
        
    output_csv : str
        Path to the output csv file.
        
    output_bib : str
        Path to the output bib file.
    """

    # Save to Json
    with open(output_json, 'w', encoding="UTF-8") as file:
        json.dump(results, file, indent=4)

    # Save to cvs
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    # Save to bib
    with open(output_bib, 'w', encoding="UTF-8") as file:
        for entry in bib_entries:
            file.write(entry)


def main():
    """
    Main function to process and save bibliographic data from pickle files.
    
    This function performs the following steps:
    1. Reads and deserializes all pickle files from the specified directory.
    2. Extracts relevant metadata and generates BibTeX entries.
    3. Saves the processed results in JSON, CSV, and BibTeX formats.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    """

    papers = read_pickles(PICKLE_CACHE_DIR)
    results, bib_entries = filter_data(papers)
    save_results(results, bib_entries, "scholar_results.json",
                "scholar_results.csv", "scholar_results.bib")


if __name__=="__main__":
    main()