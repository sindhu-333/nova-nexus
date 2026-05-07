import re
from typing import Optional, List


class RegexUtils:
    """
    Utility functions for pattern matching and data extraction.
    Used by intent detection and response formatting.
    """
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """
        Extract all numbers from text.
        
        Returns: List of integers
        """
        matches = re.findall(r'\d+', text)
        return [int(m) for m in matches]
    
    @staticmethod
    def extract_order_id(text: str) -> Optional[int]:
        """
        Extract order ID from text.
        Patterns: "order 3", "#3", "Order #3"
        
        Returns: order_id or None
        """
        match = re.search(r'order\s+#?(\d+)|#(\d+)', text, re.IGNORECASE)
        if match:
            return int(match.group(1) or match.group(2))
        return None
    
    @staticmethod
    def extract_quantity(text: str) -> Optional[int]:
        """
        Extract quantity from text.
        Patterns: "100 units", "qty 100", "200 brackets"
        
        Returns: quantity or None
        """
        # Prefer explicit quantity language so order numbers are not mistaken for quantities.
        match = re.search(
            r'\b(?:qty|quantity|need|needs|require|requires|want|wants|with)\b[^\d]{0,20}(\d+)\b',
            text,
            re.IGNORECASE
        )
        if not match:
            match = re.search(
                r'\b(\d+)\b\s*(?:units|pieces|items|brackets|flanges|shafts|rods|plates|pins|gears)\b',
                text,
                re.IGNORECASE
            )
        if not match:
            match = re.search(
                r'\bwith\b\s*(\d+)\s+(?:steel|titanium|aluminum|aluminium|copper|brass|iron|nickel|zinc|plastic|rubber)?\s*(?:brackets|flanges|shafts|rods|plates|pins|gears|parts?)\b',
                text,
                re.IGNORECASE
            )
        if match:
            qty = int(match.group(1))
            # Valid manufacturing quantities: 1-10000
            if 1 <= qty <= 10000:
                return qty
        return None
    
    @staticmethod
    def extract_material(text: str) -> Optional[str]:
        """
        Extract material from text.
        Recognizes: steel, titanium, aluminum, copper, brass, iron, nickel, zinc
        
        Returns: Material name or None
        """
        materials = {
            'steel': r'\bsteel\b',
            'titanium': r'\btitanium\b',
            'aluminum': r'\b(?:aluminum|aluminium)\b',
            'copper': r'\bcopper\b',
            'brass': r'\bbrass\b',
            'iron': r'\biron\b',
            'nickel': r'\bnickel\b',
            'zinc': r'\bzinc\b',
            'plastic': r'\bplastic\b',
            'rubber': r'\brubber\b'
        }
        
        text_lower = text.lower()
        for material, pattern in materials.items():
            if re.search(pattern, text_lower):
                return material.capitalize()
        
        return None
    
    @staticmethod
    def extract_deadline(text: str) -> Optional[str]:
        """
        Extract deadline from text.
        Recognizes: days of week, months, dates like "July 20"
        
        Returns: Deadline string or None
        """
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
        
        text_lower = text.lower()
        
        # Check for days
        for day in days:
            if day in text_lower:
                return day.capitalize()
        
        # Check for months
        for month in months:
            if month in text_lower:
                # Try to find date like "July 20"
                match = re.search(rf'{month}\s+(\d+)', text_lower, re.IGNORECASE)
                if match:
                    return f"{month.capitalize()} {match.group(1)}"
                return month.capitalize()
        
        return None
    
    @staticmethod
    def extract_part_name(text: str) -> Optional[str]:
        """
        Extract manufacturing part name from text.
        Looks for common part types followed by descriptors.
        
        Returns: Part name or None
        """
        part_patterns = {
            r'(\w+\s+bracket\s*)', 'bracket',
            r'(\w+\s+flange\s*)', 'flange',
            r'(\w+\s+shaft\s*)', 'shaft',
            r'(\w+\s+plate\s*)', 'plate',
            r'(\w+\s+rod\s*)', 'rod',
            r'(\w+\s+pin\s*)', 'pin',
            r'(\w+\s+gear\s*)', 'gear',
        }
        
        text_lower = text.lower()
        
        # Try to find descriptive pattern (e.g., "steel bracket")
        match = re.search(r'(\w+\s+(?:bracket|flange|shaft|plate|rod|pin|gear))', text_lower)
        if match:
            return match.group(1).title()
        
        return None
    
    @staticmethod
    def is_positive_response(text: str) -> bool:
        """
        Check if text contains positive sentiment.
        
        Returns: True if positive
        """
        positive_words = ['yes', 'ok', 'okay', 'sure', 'accept', 'confirm', 'approved', 'good']
        return any(word in text.lower() for word in positive_words)
    
    @staticmethod
    def is_negative_response(text: str) -> bool:
        """
        Check if text contains negative sentiment.
        
        Returns: True if negative
        """
        negative_words = ['no', 'reject', 'denied', 'bad', 'fail', 'failed', 'not approved']
        return any(word in text.lower() for word in negative_words)
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """
        Extract email from text.
        
        Returns: Email string or None
        """
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """
        Extract phone number from text.
        
        Returns: Phone string or None
        """
        match = re.search(r'\b[\d\-\+\(\)\s]{10,}\b', text)
        return match.group(0).strip() if match else None
