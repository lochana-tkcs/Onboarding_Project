<template>
  <div class="auth-container">
    <div class="auth-left">
      <img :src="logo" alt="Logo" class="logo" />
      <div class="auth-content">
        <h1>Login to Your Account</h1>
        <p>Login using social networks</p>
        <div class="social-buttons">
          <button class="social-button fb">Facebook</button>
          <button class="social-button google">Google</button>
          <button class="social-button linkedin">LinkedIn</button>
        </div>
        <form @submit.prevent="login">
          <input type="email" placeholder="Email" v-model="email" required />
          <input type="password" placeholder="Password" v-model="password" required />
          <button type="submit" class="sign-in-button">Login In</button>
          <p v-if="error" class="error-message">{{ error }}</p>
        </form>
      </div>
    </div>
    <div class="auth-right">
      <h2 class="title">New Here?</h2>
      <p class="subtitle">Sign up and discover a great amount of new opportunities!</p>
      <button class="sign-up-button" @click="signUp">Sign Up</button>
      <div class="description">
        <h3 class="about-title">About Our Platform</h3>
        <p class="about-text">
          Our web app allows you to upload CSV files and view them in a streamlined, intuitive manner. 
          Transform and analyze your data effortlessly with our powerful tools and visual editor.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import logo from '../assets/logo.png';
import axios from 'axios';
import { setAuthenticated } from '../auth';

export default {
  data() {
    return {
      email: '',
      password: '',
      error: '',
      logo: logo
    };
  },
  methods: {
    async login() {
      if (!this.email || !this.password) {
        this.error = 'Please fill in all fields';
        return;
      }

      try {
        const { data: users } = await axios.get("http://127.0.0.1:3000/users");
        const user = users.find(user => user.email === this.email && user.password === this.password);

        if (user) {
          setAuthenticated(true);
          this.$router.push('/upload');
        } else {
          this.error = 'Invalid email or password. Please try again.';
        }
      } catch (error) {
        console.error('There was an error!', error);
      }
    },
    signUp() {
      this.$router.push('/signup');
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  height: 100vh;
}

.auth-left,
.auth-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
}

.auth-left {
  background-color: #ffffff; /* White */
}

.auth-right {
  background-color: #004d40; /* Dark Green */
  color: #ffffff; /* White */
}

.logo {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 100px;
}

.auth-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 400px;
  margin-top: 50px;
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

p {
  margin-bottom: 30px;
}

.social-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.social-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: #ffffff; /* White */
  cursor: pointer;
  transition: background-color 0.3s;
}

.fb {
  background-color: #3b5998; /* Facebook Blue */
}

.google {
  background-color: #db4437; /* Google Red */
}

.linkedin {
  background-color: #0e76a8; /* LinkedIn Blue */
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 300px;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.sign-in-button {
  background-color: #004d40; /* Dark Green */
  color: #ffffff; /* White */
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.sign-in-button:hover {
  background-color: #ffffff; /* White */
  color: #004d40; /* Dark Green */
  border: 1px solid #004d40; /* Dark Green */
}

.sign-up-button {
  background-color: #ffffff; /* White */
  color: #004d40; /* Dark Green */
  border: none;
  border-radius: 5px;
  padding: 15px 30px; /* Increased padding for size */
  font-size: 1.2rem; /* Increased font size */
  font-weight: bold; /* Bold text */
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  margin-bottom: 30px; /* Added margin for spacing */
}

.sign-up-button:hover {
  background-color: #004d40; /* Dark Green */
  color: #ffffff; /* White */
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff; /* White */
}

.subtitle {
  font-size: 1.2rem;
  color: #ffffff; /* White */
}

.about-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff; /* White */
}

.about-text {
  font-size: 1rem;
  color: #ffffff; /* White */
  text-align: center;
  margin-top: 10px;
}

.description {
  text-align: center;
  max-width: 300px;
}
</style>
