from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DocumentationExtractionDetails(BaseModel):
    """
    Structured schema for extracting technical documentation details
    """
    section_name: Optional[str] = Field(
        None, 
        description="Name or title of the documentation section"
    )
    description: Optional[str] = Field(
        None, 
        description="Concise description of the section's purpose and content"
    )
    key_features: Optional[List[str]] = Field(
        None, 
        description="List of key features, capabilities, or important points"
    )
    code_examples: Optional[List[str]] = Field(
        None, 
        description="Relevant code snippets or usage examples"
    )
    configuration_options: Optional[Dict[str, Any]] = Field(
        None, 
        description="Configuration parameters or settings"
    )

    class Config:
        """Pydantic configuration for extra validation and serialization"""
        extra = 'ignore'  # Ignore extra fields
        json_encoders = {
            # Custom JSON encoding if needed
        }
