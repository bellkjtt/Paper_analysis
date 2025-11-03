"""
Layout detection service for figure extraction
Uses detectron2 for accurate figure detection
Single Responsibility: Layout-based figure extraction
"""

import os
from pathlib import Path
from typing import List, Tuple
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

try:
    import torch
    from detectron2.engine import DefaultPredictor
    from detectron2.config import get_cfg
    from detectron2 import model_zoo
    DETECTRON2_AVAILABLE = True
except ImportError:
    DETECTRON2_AVAILABLE = False


class LayoutDetectorService:
    """
    Service for detecting and extracting figures using layout detection
    Falls back to simple extraction if detectron2 not available
    """

    def __init__(self, output_dir: Path):
        """
        Initialize layout detector service

        Args:
            output_dir: Directory where figure images will be saved
        """
        self._output_dir = output_dir
        self._predictor = self._initialize_predictor() if DETECTRON2_AVAILABLE else None

    def _initialize_predictor(self):
        """Initialize detectron2 predictor for layout detection"""
        try:
            cfg = get_cfg()
            cfg.merge_from_file(model_zoo.get_config_file(
                "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
            ))
            cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
            cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
            )
            cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

            return DefaultPredictor(cfg)
        except Exception:
            return None

    def extract_figures_from_page(
        self,
        doc: fitz.Document,
        page: fitz.Page,
        page_number: int
    ) -> List[Path]:
        """
        Extract figures from a PDF page using layout detection

        Args:
            doc: PDF document
            page: PDF page object
            page_number: One-based page number

        Returns:
            List of paths to extracted figure images
        """
        if self._predictor:
            return self._extract_with_layout_detection(page, page_number)
        else:
            return self._extract_embedded_images(doc, page, page_number)

    def _extract_with_layout_detection(
        self,
        page: fitz.Page,
        page_number: int
    ) -> List[Path]:
        """
        Extract figures using detectron2 layout detection

        Args:
            page: PDF page object
            page_number: One-based page number

        Returns:
            List of paths to extracted figure images
        """
        # Convert page to image
        mat = fitz.Matrix(2, 2)  # 2x scaling
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_array = np.array(img)

        # Detect layouts
        outputs = self._predictor(img_array)
        instances = outputs["instances"].to("cpu")

        figure_paths = []

        # Extract detected regions that might be figures
        for idx, (box, score) in enumerate(zip(instances.pred_boxes, instances.scores)):
            if score < 0.7:  # Confidence threshold
                continue

            x1, y1, x2, y2 = [int(coord) for coord in box]

            # Crop figure region
            figure_img = img_array[y1:y2, x1:x2]

            if figure_img.size == 0:
                continue

            # Save figure
            figure_pil = Image.fromarray(figure_img)
            figure_filename = f"page_{page_number}_figure_{idx}.png"
            figure_path = self._output_dir / figure_filename

            figure_pil.save(str(figure_path))
            figure_paths.append(figure_path)

        return figure_paths

    def _extract_embedded_images(
        self,
        doc: fitz.Document,
        page: fitz.Page,
        page_number: int
    ) -> List[Path]:
        """
        Extract complete figure images using layout analysis (image blocks)

        Args:
            doc: PDF document
            page: PDF page object
            page_number: One-based page number

        Returns:
            List of paths to extracted figure images
        """
        figure_paths = []

        # Use layout analysis to find image blocks
        blocks = page.get_text("dict")["blocks"]

        # Filter for image blocks only
        image_blocks = [b for b in blocks if b.get("type") == 1]  # type 1 = image block

        if not image_blocks:
            # Fallback: try to find images using get_images if no blocks found
            return self._extract_images_fallback(doc, page, page_number)

        # Process each image block
        for img_index, block in enumerate(image_blocks):
            try:
                # Get bounding box of the image block
                bbox = block.get("bbox")
                if not bbox:
                    continue

                # Create a rectangular area for cropping
                rect = fitz.Rect(bbox)

                # Expand the rectangle slightly to include borders (5 pixels)
                rect.x0 -= 5
                rect.y0 -= 5
                rect.x1 += 5
                rect.y1 += 5

                # Check if the image is large enough to be a figure (not an icon)
                width = rect.x1 - rect.x0
                height = rect.y1 - rect.y0

                # Skip very small images (likely icons or decorations)
                if width < 100 or height < 50:
                    continue

                # Render the cropped area at high resolution
                mat = fitz.Matrix(3, 3)  # 3x zoom for quality
                pix = page.get_pixmap(matrix=mat, clip=rect)

                # Save as PNG
                figure_filename = f"page_{page_number}_figure_{img_index}.png"
                figure_path = self._output_dir / figure_filename

                pix.save(str(figure_path))
                figure_paths.append(figure_path)

            except Exception:
                continue

        return figure_paths

    def _extract_images_fallback(
        self,
        doc: fitz.Document,
        page: fitz.Page,
        page_number: int
    ) -> List[Path]:
        """
        Fallback method: Extract embedded images when layout analysis fails

        Args:
            doc: PDF document
            page: PDF page object
            page_number: One-based page number

        Returns:
            List of paths to extracted figure images
        """
        figure_paths = []
        image_list = page.get_images(full=True)

        # Only extract if there are very few images (to avoid tiny fragments)
        if len(image_list) > 5:
            return []

        for img_index, img_info in enumerate(image_list):
            try:
                xref = img_info[0]
                base_image = doc.extract_image(xref)

                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # Check image size to filter out tiny images
                    if len(image_bytes) < 10000:  # Skip images smaller than 10KB
                        continue

                    figure_filename = f"page_{page_number}_figure_{img_index}.{image_ext}"
                    figure_path = self._output_dir / figure_filename

                    with open(figure_path, "wb") as f:
                        f.write(image_bytes)

                    figure_paths.append(figure_path)
            except Exception:
                continue

        return figure_paths
