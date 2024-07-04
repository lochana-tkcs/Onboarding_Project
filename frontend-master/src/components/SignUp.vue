<template>
  <div>
    <h1>Signup Page</h1>
    <form @submit.prevent="handleSignup">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Signup</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async handleSignup() {
      try {
        console.log('Signup:', this.username, this.password);
        const result = await axios.post("http://127.0.0.1:3000/users", {
          username: this.username,
          password: this.password
        });
        console.warn(result);
        // Redirect to upload page
        this.$router.push('/upload');
      } catch (error) {
        console.error('There was an error!', error);
      }
    }
  }
};
</script>
