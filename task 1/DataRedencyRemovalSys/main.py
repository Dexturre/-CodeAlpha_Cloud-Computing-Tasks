from database_manager import DatabaseManager
from redundancy_detector import RedundancyDetector
from data_validator import DataValidator

def main():
    db_manager = DatabaseManager()
    redundancy_detector = RedundancyDetector()
    data_validator = DataValidator()
    
    # Example data processing loop
    sample_data = [
        {"content": "Sample text data 1", "type": "text"},
        {"content": "Sample text data 2", "type": "text"},
        {"content": "Sample text data 1", "type": "text"},  # Duplicate
        {"content": "12345", "type": "number"},
        {"content": "2023-01-01", "type": "date"},
        {"content": "true", "type": "boolean"},
        {"content": "Sample text data 3", "type": "text"},
    ]
    
    for data in sample_data:
        content = data["content"]
        data_type = data["type"]
        
        # Validate data
        is_valid, validation_msg = data_validator.validate_data(content, data_type)
        if not is_valid:
            print(f"Validation failed for '{content}': {validation_msg}")
            continue
        
        # Process data
        result = redundancy_detector.process_data(content, data_type)
        if result:
            print(f"Processed data: {result.data_content} (Type: {result.data_type})")
        else:
            print(f"Data '{content}' is redundant or not added.")

if __name__ == "__main__":
    main()
