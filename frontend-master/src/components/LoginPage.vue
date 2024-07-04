<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://localhost:8080/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: this.email, password: this.password })
        });
        if (!response.ok) {
          throw new Error('Login failed');
        }
        alert('Login successful');
        // Optionally store token if using JWT for authenticated requests
        // const data = await response.json();
        // localStorage.setItem('token', data.token);
        this.$router.push('/upload');  // Redirect to upload page
      } catch (error) {
        console.error(error);
        alert('An error occurred');
      }
    }
  }
};
</script>
