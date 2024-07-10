import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import axios from 'axios';
import AuthButtons from '../AuthButtons.vue';
import { setAuthenticated } from '../../auth';
// C:\m3\frontend-master\src\auth.js

//Testing that the component mounts properly and renders all expected sub-components and elements.
describe('AuthButtons', () => {
  it('mounts and renders all elements correctly', () => {
    const wrapper = mount(AuthButtons);
    expect(wrapper.find('.auth-container').exists()).toBe(true);
    expect(wrapper.findAll('.social-button').length).toBe(3);
    expect(wrapper.find('.sign-in-button').exists()).toBe(true);
  });
});

//Testing the sign-up redirection to ensure that it navigates to the appropriate route.
describe('Sign Up redirection', () => {
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
});
