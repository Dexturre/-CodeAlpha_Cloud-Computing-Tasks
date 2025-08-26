import re
from config import Config

class DataValidator:
    """Validates data content and type before processing"""
    
    def __init__(self):
        self.max_length = Config.MAX_STRING_LENGTH
        self.required_fields = Config.REQUIRED_FIELDS
    
    def validate_data_content(self, data_content):
        """Validate the data content meets requirements"""
        if not isinstance(data_content, str):
            return False, "Data content must be a string"
        
        if len(data_content.strip()) == 0:
            return False, "Data content cannot be empty"
        
        if len(data_content) > self.max_length:
            return False, f"Data content exceeds maximum length of {self.max_length} characters"
        
        return True, "Valid data content"
    
    def validate_data_type(self, data_type):
        """Validate the data type"""
        valid_types = ['text', 'number', 'mixed', 'boolean', 'date', 'datetime']
        
        if not isinstance(data_type, str):
            return False, "Data type must be a string"
        
        if data_type.lower() not in valid_types:
            return False, f"Invalid data type. Must be one of: {', '.join(valid_types)}"
        
        return True, "Valid data type"
    
    def validate_numeric_data(self, data_content):
        """Validate if data content is numeric"""
        try:
            float(data_content)
            return True, "Valid numeric data"
        except ValueError:
            return False, "Data content is not numeric"
    
    def validate_boolean_data(self, data_content):
        """Validate if data content is boolean"""
        boolean_values = ['true', 'false', '1', '0', 'yes', 'no']
        if data_content.lower() in boolean_values:
            return True, "Valid boolean data"
        return False, "Data content is not boolean"
    
    def validate_date_data(self, data_content):
        """Validate if data content is a date"""
        # Simple date pattern matching
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',   # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}'    # DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            if re.fullmatch(pattern, data_content):
                return True, "Valid date data"
        
        return False, "Data content is not a valid date format"
    
    def validate_mixed_data(self, data_content):
        """Validate mixed data content"""
        # For mixed data, we accept any non-empty string
        if len(data_content.strip()) > 0:
            return True, "Valid mixed data"
        return False, "Mixed data cannot be empty"
    
    def validate_data(self, data_content, data_type):
        """Comprehensive data validation"""
        # Validate data content
        is_valid_content, content_msg = self.validate_data_content(data_content)
        if not is_valid_content:
            return False, content_msg
        
        # Validate data type
        is_valid_type, type_msg = self.validate_data_type(data_type)
        if not is_valid_type:
            return False, type_msg
        
        # Type-specific validation
        data_type_lower = data_type.lower()
        if data_type_lower == 'number':
            return self.validate_numeric_data(data_content)
        elif data_type_lower == 'boolean':
            return self.validate_boolean_data(data_content)
        elif data_type_lower == 'date' or data_type_lower == 'datetime':
            return self.validate_date_data(data_content)
        elif data_type_lower == 'mixed':
            return self.validate_mixed_data(data_content)
        elif data_type_lower == 'text':
            return True, "Valid text data"  # Text data is already validated by content validation
        
        return False, "Unknown validation error"
