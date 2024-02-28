const button = document.getElementById("signup-button");
const validateForm = (event) => {
  event.preventDefault();
  const form = document.getElementById("signup-form");
  const username = form.username.value;
  const email = form.email.value;
  const password = form.pass1.value;
  const confirmPassword = form.pass2.value;
  const errorEmail = document.getElementById("error-email");
  const errorUsername = document.getElementById("error-username");
  const errorPassword = document.getElementById("error-pass1");
  const errorConfirmPassword = document.getElementById("error-pass2");
  // check valid username
  if (username === "") {
    errorUsername.textContent = "Tài khoản không được để trống";
    return false;
  } else if (username.length < 6) {
    errorUsername.textContent = "Tài khoản phải có ít nhất 6 ký tự";
    return false;
  } else {
    errorUsername.textContent = "";
  }
  // check valid email
  if (email === "") {
    errorEmail.textContent = "Email không được để trống";
    return false;
  } else if (!email.includes("@")) {
    errorEmail.textContent = "Email không hợp lệ";
    return false;
  } else {
    errorEmail.textContent = "";
  }
  // check valid password
  const regex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (password === "") {
    errorPassword.textContent = "Mật khẩu không được để trống";
    return false;
  }
  // check valid password with condition that password must have at least 1 uppercase, 1 lowercase, 1 number and 1 special character
  else if (!regex.test(password)) {
    errorPassword.textContent = "Mật khẩu không hợp lệ";
    return false;
  } else {
    errorPassword.textContent = "";
  }
  // check valid confirm password
  if (confirmPassword === "") {
    errorConfirmPassword.textContent = "Mật khẩu không được để trống";
    return false;
  } else if (password !== confirmPassword) {
    errorConfirmPassword.textContent = "Mật khẩu không khớp";
    return false;
  } else {
    errorConfirmPassword.textContent = "";
  }
  // if all valid, submit form
  form.submit();
};

button.addEventListener("click", validateForm);
