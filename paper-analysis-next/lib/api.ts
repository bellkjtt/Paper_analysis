/**
 * API client for Paper Analysis backend
 * Single Responsibility: HTTP communication
 */

import type { AnalysisResponse, ErrorResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
const API_ENDPOINT = `${API_BASE_URL}/api/v1/analyze`;

export class AnalysisAPI {
  /**
   * Analyze PDF file
   * @param file PDF file to analyze
   * @returns Analysis result
   * @throws Error if API call fails
   */
  static async analyzePDF(file: File): Promise<AnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response
        .json()
        .catch(() => ({ detail: `HTTP ${response.status}: ${response.statusText}` }));

      throw new Error(errorData.detail);
    }

    return response.json();
  }

  /**
   * Get image URL for analysis result
   * @param analysisId Analysis ID
   * @param filename Image filename
   * @returns Full image URL
   */
  static getImageURL(analysisId: string, filename: string): string {
    return `${API_BASE_URL}/api/v1/images/${analysisId}/${filename}`;
  }
}
