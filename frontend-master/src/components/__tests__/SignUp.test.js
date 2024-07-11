import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import SignUp from '../SignUp.vue'; 
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import router from '../../router';  

// Mock axios with vi
vi.mock('axios', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    default: actual,
    post: vi.fn(() => Promise.resolve({ data: { message: 'User created successfully' } }))
  };
});

let mock;

// Wrapper factory function for mounting components with options
const factory = () => {
  return mount(SignUp, {
    global: {
      plugins: [router]
    }
  });
};

beforeEach(() => {
  mock = new MockAdapter(axios);
  vi.spyOn(router, 'push').mockImplementation(() => {});
});

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
        mock.onGet("http://127.0.0.1:3000/users").reply(200, [
            { id: '1', email: 'test@example.com', password: 'password123' }
        ]);

        window.alert = vi.fn(); // Mocking window.alert
        await wrapper.setData({ email: 'test@example.com', password: 'password123' });
        await wrapper.find('form').trigger('submit.prevent');
        
        expect(window.alert).toHaveBeenCalledWith('Email already exists. Please log in.');
        expect(router.push).toHaveBeenCalledWith('/');
    });
});


// Import statements
// import { describe, it, expect, beforeEach, vi } from 'vitest';
// import { mount } from '@vue/test-utils';
// import SignUp from '../SignUp.vue'; 
// import axios from 'axios';
// import MockAdapter from 'axios-mock-adapter';
// import router from '../../router';

// // Set up the mock for axios using vi
// vi.mock('axios', async (importOriginal) => {
//   const actual = await importOriginal();
//   return {
//     ...actual,
//     default: {
//       ...actual.default,
//       post: vi.fn(() => Promise.resolve({ data: { message: 'User created successfully' } }))
//     }
//   };
// });

// let mock;

// // Factory function for mounting SignUp component
// const factory = () => {
//   return mount(SignUp, {
//     global: {
//       plugins: [router]
//     }
//   });
// };

// beforeEach(() => {
//   mock = new MockAdapter(axios);
//   vi.spyOn(router, 'push').mockImplementation(() => {});
//   vi.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error
// });


// // Test cases
// describe('SignUp Component', () => {
//   it('handles errors during signup and does not navigate', async () => {
//     const wrapper = factory();
//     mock.onPost("http://127.0.0.1:3000/users").networkError();

//     await wrapper.setData({ email: 'fail@example.com', password: 'failpass123' });
//     await wrapper.find('form').trigger('submit.prevent');

//     expect(console.error).toHaveBeenCalledWith('Signup failed:', expect.anything());
//     expect(router.push).not.toHaveBeenCalled();
//   }); 
// });