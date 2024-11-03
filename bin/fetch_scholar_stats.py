from scholarly import scholarly
import json
import os
from datetime import datetime


def get_scholar_stats():
    try:
        # Search for the author by ID
        author = scholarly.search_author_id("en0zumcAAAAJ")
        # Get all author information
        author_data = scholarly.fill(author)

        # Prepare stats
        stats = {
            "total_publications": len(author_data.get('publications', [])),
            "h_index": author_data.get('hindex', 0),
            "total_citations": author_data.get('citedby', 0),
            "i10_index": author_data.get('i10index', 0),  # Added i10-index
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save to a JSON file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, '..', 'asset', 'data', 'scholar_stats.json')

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print("Scholar stats updated successfully!")
        return stats

    except Exception as e:
        print(f"Error fetching scholar stats: {str(e)}")
        return None


if __name__ == "__main__":
    get_scholar_stats()