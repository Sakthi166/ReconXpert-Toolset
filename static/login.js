import firebase from './firebaseConfig';

const login = async (email, password) => {
  try {
    const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
    console.log("User logged in successfully", userCredential.user);
  } catch (error) {
    console.error("Error logging in: ", error.message);
  }
};
