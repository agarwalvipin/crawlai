from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..models.extraction_schema import DocumentationExtractionDetails

class BaseExtractor(ABC):
    """
    Abstract base class for content extraction strategies
    """
    @abstractmethod
    def extract(
        self, 
        url: str, 
        html: str, 
        **kwargs
    ) -> List[Dict[str, str]]:
        """
        Abstract method for extracting content from a web page
        
        Args:
            url (str): Source URL
            html (str): HTML content to extract from
            **kwargs: Additional arguments for extraction
        
        Returns:
            List of extracted content dictionaries
        """
        pass

    def _validate_extraction(
        self, 
        extraction_result: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Validate and sanitize extraction results
        
        Args:
            extraction_result (List[Dict[str, str]]): Raw extraction result
        
        Returns:
            List of validated extraction results
        """
        validated_results = []
        for result in extraction_result:
            try:
                # Attempt to validate against schema
                parsed_data = DocumentationExtractionDetails.model_validate_json(
                    result.get('content', '{}')
                )
                
                # Convert to dictionary, filtering out None values
                content_dict = {
                    k: v for k, v in parsed_data.model_dump().items() 
                    if v is not None
                }
                
                # If content is empty, skip
                if not content_dict:
                    continue
                
                validated_results.append({
                    'content': content_dict
                })
            
            except Exception as parse_err:
                # Log parsing errors or handle as needed
                print(f"Validation error: {parse_err}")
        
        return validated_results
