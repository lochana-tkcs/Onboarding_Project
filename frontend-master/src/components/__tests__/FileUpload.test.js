import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import FileUpload from '../FileUpload.vue';
import axios from 'axios';

// Mock axios to prevent actual network calls
vi.mock('axios', () => ({
  default: {
    post: vi.fn(() => Promise.resolve({ data: { data: [] } }))  // Directly return the mock resolved value
  }
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
  
  it('calls onSubmit when the submit button is clicked with a valid file', async () => {
    const { getByLabelText, getByText } = customRender(FileUpload);
    const input = getByLabelText('Choose file');
    const submitButton = getByText('Submit');
  
    // Simulate file selection
    Object.defineProperty(input, 'files', { value: [mockFile], writable: false });
    await fireEvent.change(input);
  
    // Mock axios to simulate successful upload
    axios.post.mockResolvedValue({ data: { data: [] } });
  
    // Click submit button
    await fireEvent.click(submitButton);
  
    // Check if axios.post was called
    expect(axios.post).toHaveBeenCalled();
  });
});
