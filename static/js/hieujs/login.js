const button = document.getElementById("signup-button");
const validateForm = (event) => {
  event.preventDefault();
  const form = document.getElementById("signup-form");
  const username = form.username.value;
  const password = form.password.value;
  const errorUsername = document.getElementById("error-username");
  const errorPassword = document.getElementById("error-pass1");
  // check valid username
  if (username === "") {
    errorUsername.textContent = "Tài khoản không được để trống";
    return false;
  } 
  else {
    errorUsername.textContent = "";
  }
  // check valid password
  if (password === "") {
    errorPassword.textContent = "Mật khẩu không được để trống";
    return false;
  }
  else {
    errorPassword.textContent = "";
  }
  // if all valid, submit form
  form.submit();
};

button.addEventListener("click", validateForm);
