/**
 * Markdown utility functions for image embedding and conversion
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

/**
 * Convert image URL to base64 data URI
 * @param imageUrl Image URL to fetch and convert
 * @returns Base64 data URI string
 */
async function imageUrlToBase64(imageUrl: string): Promise<string> {
  try {
    const response = await fetch(imageUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.statusText}`);
    }

    const blob = await response.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } catch (error) {
    console.error('Error converting image to base64:', error);
    throw error;
  }
}

/**
 * Embed all images in markdown as base64 data URIs
 * @param markdownContent Original markdown content with image URLs
 * @returns Markdown content with embedded base64 images
 */
export async function embedImagesAsBase64(markdownContent: string): Promise<string> {
  // Find all image URLs in markdown: ![alt](url)
  const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  const matches = Array.from(markdownContent.matchAll(imageRegex));

  if (matches.length === 0) {
    return markdownContent;
  }

  let updatedContent = markdownContent;

  // Process each image URL
  for (const match of matches) {
    const fullMatch = match[0]; // Full markdown image syntax
    const altText = match[1]; // Alt text
    let imageUrl = match[2]; // Image URL

    // Fix relative URLs to point to backend server
    if (imageUrl.startsWith('/api/')) {
      imageUrl = `${API_BASE_URL}${imageUrl}`;
    }

    try {
      // Convert image to base64
      const base64DataUri = await imageUrlToBase64(imageUrl);

      // Replace URL with base64 data URI in markdown
      const newImageMarkdown = `![${altText}](${base64DataUri})`;
      updatedContent = updatedContent.replace(fullMatch, newImageMarkdown);
    } catch (error) {
      console.error(`Failed to embed image ${imageUrl}:`, error);
      // Keep original URL if conversion fails
    }
  }

  return updatedContent;
}

/**
 * Download markdown content as file
 * @param content Markdown content
 * @param filename Download filename
 */
export function downloadMarkdown(content: string, filename: string): void {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
