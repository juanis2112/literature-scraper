#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: juanitagomez
"""
import json
import pickle
import time
from pathlib import Path
from scholarly import scholarly

PICKLE_CACHE_DIR = Path("pickle_cache")


def load_config(config_file):
    """
    Load queries and year range from config file.

    Parameters
    ----------
    config_file : str
        Path to the configuration file.

    Returns
    -------
    list
        List of queries.
    int
        Start year.
    int
        End year.

    """

    with open(config_file, 'r') as file:
        config = json.load(file)
    return config.get("queries", []), config.get("start_year", None), config.get("end_year", None)


def search_papers(queries):
    """
    Search for papers matching the queries

    Parameters
    ----------
    queries : list
        List of search queries.
    start_year : int
        The starting year for filtering papers.
    end_year : int
        The ending year for filtering papers.

    Returns
    -------
    results : list
        List of paper metadata
        
    bib_entries: list
        List of BibTex entries 

    """
    try: 
        for query in queries:
            query_cache_dir = PICKLE_CACHE_DIR / query
            query_cache_dir.mkdir(parents=True, exist_ok=True)
            
            search_results = scholarly.search_pubs(query)
              
            for idx, paper in enumerate(search_results):
                time.sleep(5)
                scholarly.fill(paper)
                with open(query_cache_dir / (str(idx) + '.pickle'), 'wb') as pickle_f:
                    pickle.dump(paper, pickle_f)
                
                time.sleep(5)
    
    except BaseException as e:      
        completed = False
        error = str(e)
    else:
        completed = True
        error = "dummy"
    finally:
        with open("progress.json", 'w', encoding="UTF-8") as f:
            json.dump({"query": query, "idx": idx, "completed": completed, "error": error}, f, indent=4)


def scrape():
    queries, start_year, end_year = load_config("config.json")
    search_papers(queries)

scrape()


