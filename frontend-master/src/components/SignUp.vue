<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1>Signup</h1>
      <form @submit.prevent="handleSignup">
        <div class="input-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="input-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" class="signup-button">Signup</button>
      </form>
      <div class="social-signup">
        <p>Signup using</p>
        <div class="social-buttons">
          <button class="social-button fb">Facebook</button>
          <button class="social-button google">Google</button>
          <button class="social-button linkedin">LinkedIn</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async handleSignup() {
      try {
        // Fetch existing users
        const { data: users } = await axios.get("http://127.0.0.1:3000/users");

        // Check if the email already exists
        const existingUser = users.find(user => user.email === this.email);

        if (existingUser) {
          alert('Email already exists. Please log in.');
          this.$router.push('/');
          return;
        }

        // Determine the new ID
        let newId = 1;
        if (users.length > 0) {
          const ids = users.map(user => parseInt(user.id, 10));
          newId = Math.max(...ids) + 1;
        }

        // Create new user with the new ID
        const newUser = {
          id: newId.toString(),
          email: this.email,
          password: this.password
        };

        // Post new user to the database
        const result = await axios.post("http://127.0.0.1:3000/users", newUser);
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

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #004d40, #00796b); /* Gradient Background */
}

.signup-box {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 2rem;
  color: #004d40; /* Dark Green Text */
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #004d40; /* Dark Green Text */
}

input {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.signup-button {
  width: 100%;
  padding: 12px;
  background-color: #004d40; /* Dark Green Background */
  border: none;
  border-radius: 5px;
  color: #ffffff;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.signup-button:hover {
  background-color: #003730; /* Darker Green */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.social-signup {
  margin-top: 30px;
}

.social-signup p {
  margin-bottom: 10px;
  color: #004d40; /* Dark Green Text */
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.social-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: #ffffff;
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

.social-button:hover {
  opacity: 0.8;
}
</style>
