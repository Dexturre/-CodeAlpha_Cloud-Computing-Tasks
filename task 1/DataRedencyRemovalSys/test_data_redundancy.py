import unittest
from database_manager import DatabaseManager
from redundancy_detector import RedundancyDetector
from data_validator import DataValidator
from models import Base
from sqlalchemy import create_engine

class TestDataRedundancySystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test database"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        
        # Create test instances
        self.db_manager = DatabaseManager()
        self.redundancy_detector = RedundancyDetector()
        self.data_validator = DataValidator()
    
    def tearDown(self):
        """Clean up test database"""
        Base.metadata.drop_all(self.engine)
    
    def test_data_validation(self):
        """Test data validation functionality"""
        # Test valid data
        is_valid, msg = self.data_validator.validate_data("test content", "text")
        self.assertTrue(is_valid)
        
        # Test invalid data type
        is_valid, msg = self.data_validator.validate_data("test", "invalid_type")
        self.assertFalse(is_valid)
        
        # Test empty content
        is_valid, msg = self.data_validator.validate_data("", "text")
        self.assertFalse(is_valid)
    
    def test_hash_generation(self):
        """Test hash generation consistency"""
        content = "test content"
        hash1 = self.redundancy_detector.hash_data(content)
        hash2 = self.redundancy_detector.hash_data(content)
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 32)  # MD5 hash length
    
    def test_duplicate_detection(self):
        """Test duplicate detection"""
        content = "duplicate test content"
        
        # First insertion should succeed
        result1 = self.redundancy_detector.process_data(content, "text")
        self.assertIsNotNone(result1, "Expected a valid result for the first insertion")
        
        # Second insertion should be detected as duplicate
        result2 = self.redundancy_detector.process_data(content, "text")
        self.assertIsNotNone(result2, "Expected a valid result for the duplicate insertion")
        
        # Check if both results are the same entry
        if result1 and result2:
            self.assertEqual(result1.id, result2.id)
    
    def test_unique_data_processing(self):
        """Test processing of unique data"""
        content = "unique test content"
        
        result = self.redundancy_detector.process_data(content, "text")
        self.assertIsNotNone(result, "Expected a valid result for unique data")
        
        if result:
            self.assertEqual(result.data_content, content)
    
    def test_mixed_data_types(self):
        """Test processing different data types"""
        test_cases = [
            ("123", "number"),
            ("true", "boolean"),
            ("2023-01-01", "date"),
            ("mixed content", "mixed")
        ]
        
        for content, data_type in test_cases:
            result = self.redundancy_detector.process_data(content, data_type)
            self.assertIsNotNone(result, f"Expected a valid result for {data_type} data")
            
            if result:
                self.assertEqual(result.data_type, data_type)
    
    def test_batch_processing(self):
        """Test batch processing scenario"""
        data_batch = [
            {"content": "batch test 1", "type": "text"},
            {"content": "batch test 2", "type": "text"},
            {"content": "batch test 1", "type": "text"},  # Duplicate
            {"content": "batch test 3", "type": "text"},
        ]
        
        results = []
        for data in data_batch:
            result = self.redundancy_detector.process_data(data["content"], data["type"])
            results.append(result)
        
        # Should have 4 results (one duplicate returns the existing entry, not None)
        valid_results = [r for r in results if r is not None]
        self.assertEqual(len(valid_results), 4)

if __name__ == '__main__':
    unittest.main()
