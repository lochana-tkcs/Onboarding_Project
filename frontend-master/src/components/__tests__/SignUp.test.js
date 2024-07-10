import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import SignUp from '../SignUp.vue'; // Ensure the path to your component is correct
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import router from '../../router';  // Adjust the path as necessary

// Create a mock for axios
const mock = new MockAdapter(axios);
axios.post = vi.fn(() => Promise.resolve({ data: { message: 'User created successfully' } }));

// Wrapper factory function for mounting components with options
const factory = () => {
  return mount(SignUp, {
    global: {
      plugins: [router]
    }
  });
};

beforeEach(() => {
  // Reset the mocks before each test
  mock.reset();
  router.push = vi.fn();  // Reset the router push method
});

describe('SignUp Component', () => {
    it('renders the signup form', () => {
      const wrapper = factory();
      expect(wrapper.find('.signup-container').exists()).toBe(true);
      expect(wrapper.find('form').exists()).toBe(true);
      expect(wrapper.find('input[type="email"]').exists()).toBe(true);
      expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    });
});

// describe('SignUp.vue', () => {
//     it('submits form data and navigates on successful signup', async () => {
//       mock.onPost('/users').reply(200, { message: 'User created successfully' });
  
//       const wrapper = factory();
//       wrapper.setData({ email: 'test@example.com', password: 'secure123' });
  
//       await wrapper.find('form').trigger('submit.prevent');
  
//       // Ensure axios.post is called with the correct parameters
//       expect(axios.post).toHaveBeenCalledWith('/users', {
//         email: 'test@example.com',
//         password: 'secure123'
//       });
  
//       // Ensure router.push is called with the correct route
//       expect(router.push).toHaveBeenCalledWith('/upload'); // Assuming '/upload' is the route after signup
//     });
//   });

