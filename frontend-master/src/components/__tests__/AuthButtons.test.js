import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import axios from 'axios';
import AuthButtons from '../AuthButtons.vue';

// Mock axios
vi.mock('axios');

beforeEach(() => {
  vi.clearAllMocks();
});

// Testing that the component mounts properly and renders all expected sub-components and elements.
describe('AuthButtons', () => {
  it('mounts and renders all elements correctly', () => {
    const wrapper = mount(AuthButtons);
    expect(wrapper.find('.auth-container').exists()).toBe(true);
    expect(wrapper.findAll('.social-button').length).toBe(3);
    expect(wrapper.find('.sign-in-button').exists()).toBe(true);
  });

  // Testing the login functionality with correct credentials
  it('allows user to login with correct credentials', async () => {
    const mockData = { users: [{ email: 'correct@example.com', password: 'password123' }] };
    axios.get.mockResolvedValue({ data: mockData });

    const wrapper = mount(AuthButtons, {
      data() {
        return {
          email: 'correct@example.com',
          password: 'password123',
          redirecting: false
        };
      }
    });

    await wrapper.find('form').trigger('submit.prevent');
    await wrapper.vm.$nextTick(); // Wait for DOM updates

    // Assuming the component sets a redirect message on successful login
    expect(wrapper.text()).toContain('Redirecting...');
  });

  it('displays an error message on failed login due to incorrect credentials', async () => {
    axios.get.mockResolvedValue({ data: { users: [] } });  // Simulating no matching user found
    const wrapper = mount(AuthButtons, {
      data() {
        return {
          email: 'wrong@example.com',
          password: 'wrongpassword',
        };
      }
    });
    await wrapper.find('form').trigger('submit.prevent');
    await wrapper.vm.$nextTick();  // Wait for DOM updates
  
    expect(wrapper.text()).toContain('Invalid email or password. Please try again.');
  });  

  // Testing the sign-up redirection to ensure that it navigates to the appropriate route.
  it('navigates to signup page on clicking sign up', async () => {
    const mockRouter = {
      push: vi.fn()
    };
    const wrapper = mount(AuthButtons, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    });

    await wrapper.find('.sign-up-button').trigger('click');
    expect(mockRouter.push).toHaveBeenCalledWith('/signup');
  });

  it('prevents login when input fields are empty', async () => {
    const wrapper = mount(AuthButtons, {
      data() {
        return {
          email: '',
          password: '',
        };
      }
    });
  
    await wrapper.find('form').trigger('submit.prevent');
    await wrapper.vm.$nextTick();  // Wait for DOM updates
  
    expect(wrapper.text()).toContain('Please fill in all fields');
  });

  it('shows a redirecting message while processing login', async () => {
    const mockData = { users: [{ email: 'correct@example.com', password: 'password123' }] };
    axios.get.mockResolvedValue({ data: mockData });
  
    const wrapper = mount(AuthButtons, {
      data() {
        return {
          email: 'correct@example.com',
          password: 'password123',
          redirecting: true  // simulate redirecting state
        };
      }
    });
  
    expect(wrapper.text()).toContain('Redirecting...');
  });
});
