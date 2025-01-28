import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getDatabase, ref, set, get, child } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-database.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, sendEmailVerification } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "<YOUR_API_KEY>",
  authDomain: "<YOUR_AUTH_DOMAIN>",
  databaseURL: "<YOUR_DATABASE_URL>",
  projectId: "<YOUR_PROJECT_ID>",
  storageBucket: "<YOUR_STORAGE_BUCKET>",
  messagingSenderId: "<YOUR_MESSAGING_SENDER_ID>",
  appId: "<YOUR_APP_ID>"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app);

// DOM Elements
const loginsec = document.querySelector(".login-section");
const loginlink = document.querySelector(".login-link");
const registerlink = document.querySelector(".register-link");
const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");

// Switch to registration form
registerlink.addEventListener("click", () => {
  loginsec.classList.add("active");
});

// Switch back to login form
loginlink.addEventListener("click", () => {
  loginsec.classList.remove("active");
});

// Handle registration form submission
registerForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const username = document.getElementById("text").value; // Username
  const email = document.getElementById("register-email").value; // Email
  const password = document.getElementById("password").value; // Password

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;

      // Save user data to the database
      set(ref(database, `users/${user.uid}`), {
        username: username,
        email: email,
      })
        .then(() => {
          alert("User registered successfully!");

          // Send email verification
          sendEmailVerification(user)
            .then(() => {
              alert("Verification email sent to " + email);
              loginsec.classList.remove("active"); // Show login form
            })
            .catch((error) => {
              console.error("Error sending email verification:", error);
              alert("Failed to send verification email.");
            });
        })
        .catch((error) => {
          console.error("Error storing user data:", error);
          alert("An error occurred while saving user details.");
        });
    })
    .catch((error) => {
      console.error("Error during registration:", error);
      alert("Registration failed: " + error.message);
    });
});

// Handle login form submission
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;

      // Fetch user data from the database
      const dbRef = ref(database);
      get(child(dbRef, `users/${user.uid}`))
        .then((snapshot) => {
          if (snapshot.exists()) {
            const userData = snapshot.val();
            alert(`Welcome back, ${userData.username}!`);
            window.location.href = "/dashboard.html";
          } else {
            alert("No user data found.");
          }
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
          alert("Failed to fetch user details.");
        });
    })
    .catch((error) => {
      console.error("Error during login:", error);
      alert("Login failed: " + error.message);
    });
});

