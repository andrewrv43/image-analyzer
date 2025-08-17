import { Component, computed, signal, effect, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageAnalyzerService, ImageAnalysisResponse, ImageLabel } from './services/image-analyzer.service';

interface ChatMessage { role: 'user' | 'assistant'; content: string; raw?: any; }

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {
  title = 'Image Analyzer';
  messages = signal<ChatMessage[]>([]);
  loading = signal(false);
  error = signal<string | null>(null);
  selectedFile = signal<File | null>(null);
  previewUrl = signal<string | null>(null);
  dragOver = signal(false);
  parsedAnalysis = signal<{ descripcion?: string; labels?: ImageLabel[] } | null>(null);
  private objectUrl: string | null = null;

  constructor(private svc: ImageAnalyzerService) {}

  // Auto-generate preview URL and trigger analysis when a file is selected
  previewEff = effect(() => {
    const f = this.selectedFile();
    this.parsedAnalysis.set(null);
    if (this.objectUrl) {
      URL.revokeObjectURL(this.objectUrl);
      this.objectUrl = null;
    }
    if (f) {
      this.objectUrl = URL.createObjectURL(f);
      this.previewUrl.set(this.objectUrl);
      // Auto send analysis
      this.send();
    } else {
      this.previewUrl.set(null);
    }
  }, { allowSignalWrites: true });

  onFileChange(ev: Event) {
    const input = ev.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.selectedFile.set(input.files[0]);
      this.error.set(null);
    }
  }

  onDragOver(ev: DragEvent) {
    ev.preventDefault();
    this.dragOver.set(true);
  }
  onDragLeave(ev: DragEvent) {
    ev.preventDefault();
    this.dragOver.set(false);
  }
  onDrop(ev: DragEvent) {
    ev.preventDefault();
    this.dragOver.set(false);
    if (ev.dataTransfer?.files?.length) {
      const file = Array.from(ev.dataTransfer.files).find(f => f.type.startsWith('image/')) || ev.dataTransfer.files[0];
      if (file) {
        this.selectedFile.set(file);
        this.error.set(null);
      }
    }
  }

  clear() {
    this.selectedFile.set(null);
    this.messages.set([]);
    this.parsedAnalysis.set(null);
    this.error.set(null);
  }

  async send() {
    const file = this.selectedFile();
    if (!file) {
      this.error.set('Selecciona una imagen');
      return;
    }
    this.loading.set(true);
    this.error.set(null);
    this.messages.update((arr: ChatMessage[]) => [...arr, { role: 'user', content: `Analiza la imagen: ${file.name}` }]);
    try {
      const resp = await this.svc.analyze(file);
      const raw = resp.analysis || resp.analysis_error || 'Sin análisis';
      let parsed: any = null;
      if (resp.analysis) {
        try { parsed = JSON.parse(resp.analysis); } catch { /* ignore */ }
      }
      if (parsed) {
        this.parsedAnalysis.set(parsed);
      }
      this.messages.update((arr: ChatMessage[]) => [...arr, { role: 'assistant', content: raw, raw: resp }]);
    } catch (e: any) {
      this.error.set(e.message);
      this.messages.update((arr: ChatMessage[]) => [...arr, { role: 'assistant', content: 'Error: ' + e.message }]);
    } finally {
      this.loading.set(false);
    }
  }

  labels = computed(() => this.parsedAnalysis()?.labels || []);
  descripcion = computed(() => this.parsedAnalysis()?.descripcion || '');

  ngOnDestroy(): void {
    if (this.objectUrl) URL.revokeObjectURL(this.objectUrl);
  }
}
