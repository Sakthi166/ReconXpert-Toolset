
// firebaseConfig.js
import firebase from "firebase/app";
import "firebase/auth";
import "firebase/database";





// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDt5zOAFzdujEYDhzTheSEsDljLS2QqxZA",
  authDomain: "user-db1-reconxpert.firebaseapp.com",
  databaseURL: "https://user-db1-reconxpert-default-rtdb.firebaseio.com",
  projectId: "user-db1-reconxpert",
  storageBucket: "user-db1-reconxpert.firebasestorage.app",
  messagingSenderId: "79236198877",
  appId: "1:79236198877:web:7712325d86c27af0aa8634"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
export default firebase;
// Reference your database
const contactFormDB = firebase.database().ref("userdatabase");

// Add event listener for form submission
document.getElementById("register-form").addEventListener("submit", submitForm);

// Form submission handler
function submitForm(e) {
  e.preventDefault();

  // Get form values
  const text = getElementVal("text");
  const registerEmail = getElementVal("register-email");
  const password = getElementVal("password");

  // Save data to Firebase
  saveMessages(text, registerEmail, password);

  // Display success alert
  document.querySelector(".alert").style.display = "block";

  // Hide alert after 3 seconds
  setTimeout(() => {
    document.querySelector(".alert").style.display = "none";
  }, 3000);

  // Reset the form
  document.getElementById("register-form").reset();
}

// Save messages to Firebase
function saveMessages(text, registerEmail, password) {
  const newContactForm = contactFormDB.push();
  newContactForm.set({
    text: text,
    registerEmail: registerEmail,
    password: password,
  });
}

// Get element value by ID
function getElementVal(id) {
  return document.getElementById(id).value;
}
