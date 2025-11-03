'use client';

/**
 * Main page component
 * Single Responsibility: Page layout and state management
 */

import { useState } from 'react';
import type { AnalysisState } from '@/types';
import { AnalysisAPI } from '@/lib/api';
import ReactMarkdown from 'react-markdown';

const MAX_FILE_SIZE_MB = 50;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export default function HomePage() {
  const [state, setState] = useState<AnalysisState>({ type: 'idle' });
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState<{
    totalPages: number;
    currentPage: number;
    stage: 'extracting' | 'analyzing' | 'finalizing';
  } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      alert('PDF 파일만 업로드 가능합니다.');
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE_BYTES) {
      alert(`파일 크기는 ${MAX_FILE_SIZE_MB}MB를 초과할 수 없습니다.`);
      return;
    }

    setFile(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file) return;

    // Show uploading state immediately
    setState({ type: 'uploading' });

    try {
      // Simulate small delay for uploading feedback
      await new Promise(resolve => setTimeout(resolve, 300));

      setState({ type: 'analyzing' });

      // Estimate 10 pages average, 12 seconds per page
      const estimatedPages = 10;
      const secondsPerPage = 12;

      // Start progress simulation
      setProgress({ totalPages: estimatedPages, currentPage: 0, stage: 'extracting' });

      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (!prev) return null;

          const { currentPage, totalPages, stage } = prev;

          // Extracting stage (first 10%)
          if (stage === 'extracting' && currentPage < 1) {
            return { ...prev, currentPage: 1, stage: 'analyzing' };
          }

          // Analyzing stage (10% - 90%)
          if (stage === 'analyzing' && currentPage < totalPages) {
            return { ...prev, currentPage: currentPage + 1 };
          }

          // Finalizing stage (90% - 100%)
          if (stage === 'analyzing' && currentPage >= totalPages) {
            return { ...prev, stage: 'finalizing' };
          }

          return prev;
        });
      }, secondsPerPage * 1000);

      const result = await AnalysisAPI.analyzePDF(file);

      clearInterval(progressInterval);
      setProgress(null);
      setState({ type: 'success', data: result });
    } catch (error) {
      setProgress(null);
      setState({ type: 'error', message: error instanceof Error ? error.message : '분석 실패' });
    }
  };

  const handleReset = () => {
    setState({ type: 'idle' });
    setFile(null);
    setProgress(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="text-center mb-12 pb-8 border-b border-gray-200">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">논문 분석 시스템</h1>
          <p className="text-gray-600">Gemini Flash 2.5 기반 학술 논문 분석</p>
        </header>

        {state.type === 'idle' && (
          <div className="bg-white rounded-lg border border-gray-200 p-8">
            <div className="text-center mb-8 p-12 border-2 border-dashed border-gray-300 rounded-lg">
              <div className="text-5xl mb-4">📄</div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">PDF 파일 선택</h2>
              <p className="text-gray-600 mb-6">분석할 학술 논문을 업로드하세요</p>
              <label className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors font-medium">
                파일 선택
                <input type="file" accept=".pdf" onChange={handleFileChange} className="hidden" />
              </label>
            </div>

            {file && (
              <div className="mt-6 p-4 bg-gray-100 rounded-lg">
                <p className="text-sm text-gray-700">
                  선택된 파일: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </p>
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!file}
              className="w-full mt-6 py-4 bg-blue-600 text-white rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              분석 시작
            </button>
          </div>
        )}

        {state.type === 'uploading' && (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">파일 업로드 중...</h2>
            <p className="text-gray-600">PDF 파일을 서버에 전송하고 있습니다.</p>
          </div>
        )}

        {state.type === 'analyzing' && (
          <div className="bg-white rounded-lg border border-gray-200 p-8">
            <div className="text-center mb-8">
              <div className="relative w-20 h-20 mx-auto mb-6">
                <div className="absolute inset-0 border-4 border-blue-200 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
              </div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">논문 분석 중...</h2>
              <p className="text-gray-600 mb-2">PDF 페이지를 추출하고 Gemini Flash 2.5로 분석하고 있습니다.</p>

              {progress && (
                <div className="mt-4">
                  <div className="flex items-center justify-center gap-2 text-sm text-gray-700 mb-2">
                    <span className="font-semibold">
                      {progress.stage === 'extracting' && 'PDF 추출 중'}
                      {progress.stage === 'analyzing' && `페이지 ${progress.currentPage}/${progress.totalPages} 분석 중`}
                      {progress.stage === 'finalizing' && '최종 정리 중'}
                    </span>
                  </div>
                  <div className="w-full max-w-md mx-auto bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                      style={{
                        width: progress.stage === 'extracting'
                          ? '5%'
                          : progress.stage === 'finalizing'
                          ? '95%'
                          : `${5 + (progress.currentPage / progress.totalPages) * 85}%`
                      }}
                    ></div>
                  </div>
                </div>
              )}
            </div>

            <div className="max-w-2xl mx-auto space-y-3">
              {progress && Array.from({ length: progress.totalPages }).map((_, index) => {
                const pageNum = index + 1;
                const isDone = progress.stage === 'finalizing' || (progress.stage === 'analyzing' && progress.currentPage > pageNum);
                const isCurrent = progress.stage === 'analyzing' && progress.currentPage === pageNum;
                const isPending = progress.stage === 'extracting' || (progress.stage === 'analyzing' && progress.currentPage < pageNum);

                return (
                  <div
                    key={pageNum}
                    className={`flex items-center gap-3 p-3 rounded-lg transition-all ${
                      isDone ? 'bg-green-50 border border-green-200' :
                      isCurrent ? 'bg-blue-50 border border-blue-200' :
                      'bg-gray-50 border border-gray-200'
                    }`}
                  >
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                      isDone ? 'bg-green-600 text-white' :
                      isCurrent ? 'bg-blue-600 text-white' :
                      'bg-gray-300 text-gray-600'
                    }`}>
                      {isDone ? '✓' : pageNum}
                    </div>
                    <div className="flex-1">
                      <div className={`font-medium ${isDone ? 'text-green-700' : isCurrent ? 'text-blue-700' : 'text-gray-500'}`}>
                        Page {pageNum}
                        {isDone && <span className="ml-2 text-xs font-normal">(완료)</span>}
                        {isCurrent && <span className="ml-2 text-xs font-normal">(분석 중...)</span>}
                        {isPending && <span className="ml-2 text-xs font-normal">(대기 중)</span>}
                      </div>
                    </div>
                    {isCurrent && (
                      <div className="flex-shrink-0">
                        <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                      </div>
                    )}
                  </div>
                );
              })}

              {progress && progress.stage === 'finalizing' && (
                <div className="flex items-center gap-3 p-3 rounded-lg bg-blue-50 border border-blue-200 mt-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold bg-blue-600 text-white">
                    ⚡
                  </div>
                  <div className="flex-1 font-medium text-blue-700">
                    최종 분석 및 Figure 삽입 중...
                  </div>
                  <div className="flex-shrink-0">
                    <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                </div>
              )}
            </div>

            <p className="mt-6 text-center text-xs text-gray-400">예상 소요 시간: 페이지당 약 10-15초</p>
          </div>
        )}

        {state.type === 'success' && (
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="flex justify-between items-center p-6 border-b border-gray-200">
              <h2 className="text-2xl font-semibold text-gray-900">분석 결과</h2>
              <div className="flex gap-3">
                <a
                  href={`data:text/markdown;charset=utf-8,${encodeURIComponent(state.data.markdown_content)}`}
                  download={`${state.data.pdf_filename.replace('.pdf', '')}_분석.md`}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  마크다운 다운로드
                </a>
                <button onClick={handleReset} className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors">
                  새 분석
                </button>
              </div>
            </div>

            <div className="p-4 bg-gray-50 border-b border-gray-200 text-sm text-gray-600">
              PDF: {state.data.pdf_filename} | 페이지: {state.data.total_pages} | 모델: {state.data.model_used} | 생성: {state.data.analysis_timestamp}
            </div>

            <div className="p-8 prose prose-gray max-w-none">
              <ReactMarkdown
                components={{
                  img: ({ src, alt }) => {
                    // Fix image URLs to point to backend server
                    const imageUrl = src?.startsWith('/api/')
                      ? `http://127.0.0.1:8000${src}`
                      : src;

                    return (
                      <img
                        src={imageUrl}
                        alt={alt || ''}
                        className="max-w-full h-auto my-4 rounded-lg shadow-md"
                        loading="lazy"
                      />
                    );
                  },
                }}
              >
                {state.data.markdown_content}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {state.type === 'error' && (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="text-5xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-red-600 mb-2">분석 실패</h2>
            <p className="text-gray-600 mb-6">{state.message}</p>
            <button onClick={handleReset} className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
              다시 시도
            </button>
          </div>
        )}

        <footer className="mt-12 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          Powered by Gemini Flash 2.5
        </footer>
      </div>
    </div>
  );
}
