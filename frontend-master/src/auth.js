// src/auth.js
export const auth = {
    isAuthenticated: false
  };
  
  export function setAuthenticated(value) {
    auth.isAuthenticated = value;
  }
  
  export function isAuthenticated() {
    return auth.isAuthenticated;
  }
  