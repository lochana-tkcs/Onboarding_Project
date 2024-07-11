import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import SignUp from '../SignUp.vue'; 
import axios from 'axios';
import router from '../../router';  

// Mock axios with vi
vi.mock('axios', () => ({
  post: vi.fn(() => Promise.resolve({ data: { message: 'User created successfully' } }))
}));

// Wrapper factory function for mounting components with options
const factory = () => {
  return mount(SignUp, {
    global: {
      plugins: [router]
    }
  });
};

describe('SignUp Component', () => {
    it('renders the signup form', () => {
      const wrapper = factory();
      expect(wrapper.find('.signup-container').exists()).toBe(true);
      expect(wrapper.find('form').exists()).toBe(true);
      expect(wrapper.find('input[type="email"]').exists()).toBe(true);
      expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    });

    it('has Facebook, Google, and LinkedIn signup buttons', () => {
        const wrapper = factory();
        expect(wrapper.find('.social-button.fb').exists()).toBe(true);
        expect(wrapper.find('.social-button.google').exists()).toBe(true);
        expect(wrapper.find('.social-button.linkedin').exists()).toBe(true);
    });

    it('shows an alert and prevents navigation if the email already exists', async () => {
        const wrapper = factory();
        mock.onGet("http://127.0.0.1:3000/users").reply(200, {
            data: [{ id: '1', email: 'test@example.com', password: 'password123' }]
        });

        window.alert = vi.fn(); // Mocking window.alert
        await wrapper.setData({ email: 'test@example.com', password: 'password123' });
        await wrapper.find('form').trigger('submit.prevent');
        
        expect(window.alert).toHaveBeenCalledWith('Email already exists. Please log in.');
        expect(router.push).toHaveBeenCalledWith('/');
    });
});
