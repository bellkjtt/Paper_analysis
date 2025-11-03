/**
 * Type definitions for Paper Analysis API
 * Single Responsibility: Type safety
 */

export interface AnalysisResponse {
  markdown_content: string;
  pdf_filename: string;
  total_pages: number;
  analysis_timestamp: string;
  model_used: string;
  output_path: string | null;
}

export interface ErrorResponse {
  detail: string;
}

export type AnalysisState =
  | { type: 'idle' }
  | { type: 'uploading' }
  | { type: 'analyzing' }
  | { type: 'success'; data: AnalysisResponse }
  | { type: 'error'; message: string };
