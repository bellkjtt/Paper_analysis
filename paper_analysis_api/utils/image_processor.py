"""
Image processing utilities
Handles figure insertion into markdown analysis
"""

import re
from pathlib import Path
from typing import Dict, List


def insert_figure_images(
    markdown_content: str,
    output_dir: Path,
    analysis_id: str
) -> str:
    """
    Insert figure images into markdown content
    Finds "Figure X (Page Y, Index Z)" patterns and adds actual figure image references

    Args:
        markdown_content: Original markdown text
        output_dir: Directory containing figure images
        analysis_id: Unique ID for this analysis

    Returns:
        Markdown with embedded figure image references
    """
    # Pattern: Figure X (Page Y, Index Z)
    pattern = r'Figure\s+(\d+)\.?\s*\(Page\s+(\d+),\s*Index\s+(\d+)\)'

    def replace_with_image(match):
        figure_num = match.group(1)
        page_num = match.group(2)
        index = match.group(3)

        # Original text
        original = match.group(0)

        # Find the actual figure file
        # Files are named: page_{page_num}_figure_{index}.{ext}
        figure_pattern = f"page_{page_num}_figure_{index}.*"
        figure_files = list(output_dir.glob(figure_pattern))

        if figure_files:
            # Use the first matching file
            figure_filename = figure_files[0].name
            # Image path relative to API (includes /api/v1 prefix)
            image_url = f"/api/v1/images/{analysis_id}/{figure_filename}"

            # Create markdown with actual figure image
            return f"{original}\n\n![Figure {figure_num}]({image_url})\n"
        else:
            # If figure file not found, just return original text
            return original

    # Replace all occurrences
    processed = re.sub(pattern, replace_with_image, markdown_content)

    return processed


def create_image_mapping(pages_data: List) -> Dict[int, Path]:
    """
    Create mapping of page numbers to image paths

    Args:
        pages_data: List of PageData objects

    Returns:
        Dictionary mapping page number to image path
    """
    mapping = {}
    for page_data in pages_data:
        mapping[page_data.page_number] = page_data.image_path

    return mapping
