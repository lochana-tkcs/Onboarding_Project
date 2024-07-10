import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import FileUpload from '../FileUpload.vue';
import axios from 'axios';

// Mock axios to prevent actual network calls
vi.mock('axios', () => ({
  post: vi.fn()
}));

// Setup custom render with Vuetify
const customRender = (ui, options = {}, vuetifyOptions = {}) => {
  const app = createApp(ui);
  const vuetify = createVuetify(vuetifyOptions);

  app.use(vuetify);

  return render(ui, { ...options, global: { plugins: [vuetify] } });
};

const mockFile = new File(['content'], 'test.csv', { type: 'text/csv' });

describe('FileUpload.vue', () => {
  it('should display default label when no file is selected', async () => {
    const { getByText } = customRender(FileUpload);
    expect(getByText('Choose file')).toBeInTheDocument();
  });

  it('checks for file size larger than 1GB', async () => {
    const { getByLabelText, getByText } = customRender(FileUpload);
    const input = getByLabelText('Choose file');
    const largeFile = new File([''], 'large.csv', { type: 'text/csv' });
    Object.defineProperty(largeFile, 'size', { value: 1024 * 1024 * 1024 + 1 });

    Object.defineProperty(input, 'files', {
      value: [largeFile],
      writable: false,
    });

    await fireEvent.change(input);
    expect(getByText('File too large, max size allowed is 1 GB')).toBeInTheDocument();
  });

  it('checks for unsupported file types', async () => {
    const { getByLabelText, getByText } = customRender(FileUpload);
    const input = getByLabelText('Choose file');
    const unsupportedFile = new File(['content'], 'test.txt', { type: 'text/plain' });

    Object.defineProperty(input, 'files', {
      value: [unsupportedFile],
      writable: false,
    });

    await fireEvent.change(input);
    expect(getByText('File type is not supported!')).toBeInTheDocument();
  });

  it('successfully selects a file', async () => {
    const { getByLabelText, getByText } = customRender(FileUpload);
    const input = getByLabelText('Choose file');
    
    // Set the files property directly to simulate a file selection
    Object.defineProperty(input, 'files', { value: [mockFile], writable: false });
    
    await fireEvent.change(input); // This should trigger the input event correctly
    expect(getByText('test.csv')).toBeInTheDocument();
  });    
  
});
