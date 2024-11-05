# bin/fetch_scholar_stats.py

import json
import os
import time
from datetime import datetime
from scholarly import scholarly, ProxyGenerator


def setup_proxy():
    """Setup proxy to avoid Google Scholar blocking"""
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    return success


def fetch_scholar_stats(retries=3, delay=5):
    """
    Fetch Google Scholar statistics with retry mechanism
    """
    author_id = "en0zumcAAAAJ"  # Shipei Xing's Google Scholar ID

    for attempt in range(retries):
        try:
            # Setup proxy for each attempt
            setup_proxy()

            # Search for author and get complete profile
            author = scholarly.search_author_id(author_id)
            author_info = scholarly.fill(author)

            # Extract relevant statistics
            stats = {
                "total_publications": author_info['publications_total'],
                "h_index": author_info['hindex'],
                "total_citations": author_info['citedby'],
                "i10_index": author_info['i10index'],
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            return stats

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise Exception(f"Failed to fetch scholar stats after {retries} attempts")


def save_stats(stats, filepath):
    """Save stats to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(stats, f, indent=2)


def main():
    try:
        # Set the output file path
        output_file = "asset/data/scholar_stats.json"

        # Fetch current stats
        stats = fetch_scholar_stats()

        # If we have existing stats, load them for comparison
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                old_stats = json.load(f)

            # Only update if there are actual changes in the metrics
            if (old_stats["total_publications"] == stats["total_publications"] and
                    old_stats["h_index"] == stats["h_index"] and
                    old_stats["total_citations"] == stats["total_citations"] and
                    old_stats["i10_index"] == stats["i10_index"]):
                print("No changes in stats detected. Skipping update.")
                return

        # Save new stats
        save_stats(stats, output_file)
        print(f"Successfully updated scholar stats: {stats}")

    except Exception as e:
        print(f"Error updating scholar stats: {str(e)}")
        raise e


if __name__ == "__main__":
    main()