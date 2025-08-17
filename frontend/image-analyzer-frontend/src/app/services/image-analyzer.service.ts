import { inject, Injectable, signal } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

export interface ImageLabel { label: string; confidence: number; }
export interface ImageAnalysisResponse {
  message: string;
  filename: string;
  format: string;
  analysis?: string; // raw JSON string coming from backend (OpenAI output)
  max_size_bytes?: number;
  analysis_error?: string;
}

@Injectable({ providedIn: 'root' })
export class ImageAnalyzerService {
  private http = inject(HttpClient);
  apiUrl = 'http://localhost:8000/api/analyze';

  async analyze(file: File): Promise<ImageAnalysisResponse> {
    const form = new FormData();
    form.append('file', file);
    try {
      const obs$ = this.http.post<ImageAnalysisResponse>(this.apiUrl, form);
      return await lastValueFrom(obs$);
    } catch (e) {
      const err = e as HttpErrorResponse;
      throw new Error(err.error?.error || err.message || 'Error desconocido');
    }
  }
}
