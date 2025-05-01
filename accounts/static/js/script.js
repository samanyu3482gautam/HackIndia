
// document.addEventListener("DOMContentLoaded", function () {
//   // Your full existing script goes here
//   const formTitle = document.getElementById('form-title');
// const toggleText = document.getElementById('toggle-text');
// const toggleButton = document.getElementById('toggle-button');
// const extraField = document.getElementById('extra-field');
// const authForm = document.getElementById('auth-form');
// const takeOffButton = document.getElementById('takeoff-button');
// const forgotBox = document.getElementById('forgot-box');

// let isLogin = true;

// function clearInputs() {
//   const inputs = authForm.querySelectorAll('input');
//   inputs.forEach(input => input.value = '');
// }

// function toggleForm() {
//   isLogin = !isLogin;
//   clearInputs();

//   if (isLogin) {
//     formTitle.textContent = "Welcome Back, Pilot!";
//     toggleText.textContent = "Don't have a Flight ID?";
//     toggleButton.textContent = "Sign Up";
//     extraField.classList.add('hidden');
//     forgotBox.classList.remove('hidden'); // Show forgot password
//   } else {
//     formTitle.textContent = "Create Your Flight ID";
//     toggleText.textContent = "Already have an account?";
//     toggleButton.textContent = "Login";
//     extraField.classList.remove('hidden');
//     forgotBox.classList.add('hidden'); // Hide forgot password
//   }
// }

// function togglePassword() {
//   const passwordInput = document.getElementById('password');
//   passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
// }

// function saveUser(email, password) {
//   let users = JSON.parse(localStorage.getItem('users')) || [];
//   const existingUser = users.find(user => user.email === email);
//   if (existingUser) {
//     alert("🚫 User already exists! Please login.");
//     return false;
//   }
//   users.push({ email, password });
//   localStorage.setItem('users', JSON.stringify(users));
//   return true;
// }

// function validateUser(email, password) {
//   let users = JSON.parse(localStorage.getItem('users')) || [];
//   return users.find(user => user.email === email && user.password === password);
// }

// // ✅ FORGOT PASSWORD FUNCTION
// function handleForgotPassword() {
//   const email = prompt("📧 Enter your registered email:");

//   if (!email) return;

//   const users = JSON.parse(localStorage.getItem('users')) || [];
//   const user = users.find(user => user.email === email);

//   if (user) {
//     alert(`📩 A password reset link has been sent to ${email}. (Simulation)`);
//   } else {
//     alert("🚫 No such Flight ID found! Please sign up.");
//   }
// }

// // ✅ TAKE OFF BUTTON HANDLER
// takeOffButton.addEventListener('click', (e) => {
//   e.preventDefault();

//   const email = authForm.querySelector('input[type="email"]').value.trim();
//   const password = document.getElementById('password').value.trim();

//   if (email === "" || password === "") {
//     alert("⚠️ Please fill all fields!");
//     return;
//   }

//   if (isLogin) {
//     const user = validateUser(email, password);

//     if (user) {
//       alert("✅ You are successfully logged in!");
//       clearInputs();
//     } else {
//       let users = JSON.parse(localStorage.getItem('users')) || [];
//       const userExists = users.find(user => user.email === email);

//       if (!userExists) {
//         alert("🛑 You should register first!");
//         toggleForm(); // Switch to signup
//       } else {
//         alert("❌ Incorrect password. Try again!");
//       }
//     }

//   } else {
//     const confirmPassword = document.getElementById('confirm-password').value.trim();

//     if (password !== confirmPassword) {
//       alert("🚫 Passwords do not match!");
//       return;
//     }

//     const signupSuccess = saveUser(email, password);
//     if (signupSuccess) {
//       alert(`✅ Flight ID created for ${email}. Now login to take off!`);
//       clearInputs();
//       toggleForm();
//     }
//   }
// });
// });


document.addEventListener("DOMContentLoaded", function () {
  const formTitle = document.getElementById('form-title');
  const toggleText = document.getElementById('toggle-text');
  const toggleButton = document.getElementById('toggle-button');
  const extraField = document.getElementById('extra-field');
  const forgotBox = document.getElementById('forgot-box');
  let isLogin = true;

  function toggleForm() {
    isLogin = !isLogin;
    if (isLogin) {
      formTitle.textContent = "Welcome Back, Pilot!";
      toggleText.textContent = "Don't have a Flight ID?";
      toggleButton.textContent = "Sign Up";
      extraField.classList.add('hidden');
      forgotBox.classList.remove('hidden');
    } else {
      formTitle.textContent = "Create Your Flight ID";
      toggleText.textContent = "Already have an account?";
      toggleButton.textContent = "Login";
      extraField.classList.remove('hidden');
      forgotBox.classList.add('hidden');
    }
  }

  toggleButton.addEventListener('click', toggleForm);
});
