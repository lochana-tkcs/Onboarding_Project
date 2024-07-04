<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = ''; // Reset error message
      try {
        const response = await fetch('http://localhost:8080/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: this.email, password: this.password })
        });

        const contentType = response.headers.get('content-type');
        if (!response.ok) {
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Registration failed');
          } else {
            throw new Error('Unexpected error occurred');
          }
        }
        
        alert('Registration successful');
        this.$router.push('/upload');  // Redirect to upload page
      } catch (error) {
        console.error('Registration error:', error);
        this.errorMessage = error.message || 'An error occurred';
      }
    }
  }
};
</script>

<style>
.error {
  color: red;
}
</style>
