import hashlib
try:
    from Levenshtein import distance as levenshtein_distance
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    print("Warning: python-Levenshtein not installed. Using simple string comparison.")
from database_manager import DatabaseManager

class RedundancyDetector:
    """Detects redundant and false positive data entries"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def hash_data(self, data_content):
        """Generate a hash for the given data content"""
        return hashlib.md5(data_content.encode('utf-8')).hexdigest()
    
    def is_duplicate(self, data_content):
        """Check if the data content is a duplicate"""
        content_hash = self.hash_data(data_content)
        existing_entry = self.db_manager.get_data_entry_by_hash(content_hash)
        return existing_entry is not None, existing_entry
    
    def classify_data(self, new_data_content):
        """Classify new data as redundant or false positive"""
        is_duplicate, existing_entry = self.is_duplicate(new_data_content)
        
        if is_duplicate:
            return True, existing_entry  # Data is a duplicate
        
        # Fuzzy matching for false positives (only if Levenshtein is available)
        if LEVENSHTEIN_AVAILABLE:
            for entry in self.db_manager.get_all_data_entries():
                if levenshtein_distance(new_data_content, str(entry.data_content)) < 3:  # Threshold for similarity
                    return True, entry  # Data is similar to an existing entry
        else:
            # Fallback: simple string comparison for similarity
            for entry in self.db_manager.get_all_data_entries():
                if new_data_content.lower() == str(entry.data_content).lower():
                    return True, entry  # Data is similar to an existing entry
        
        return False, None  # Data is unique
    
    def process_data(self, data_content, data_type):
        """Process new data content"""
        is_redundant, existing_entry = self.classify_data(data_content)
        
        if is_redundant and existing_entry:
            print(f"Data is redundant: {existing_entry.data_content}")
            return existing_entry
        elif is_redundant:
            print(f"Data is redundant but no existing entry found")
            return None
        
        # If data is unique, add it to the database
        content_hash = self.hash_data(data_content)
        new_entry = self.db_manager.add_data_entry(data_content, data_type, content_hash)
        return new_entry
