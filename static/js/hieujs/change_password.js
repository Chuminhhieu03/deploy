const button = document.getElementById("changePassword_btn");
const validateForm = (event) => {
  event.preventDefault();
  const form = document.getElementById("changePassword_form");
  const oldPassword = form.oldPassword.value;
  const newPassword = form.newPassword.value;
  const confirmPassword = form.confirmNewPassword.value;
  const errorOldPassword = document.getElementById("oldPassword_error");
  const errorNewPassword = document.getElementById("newPassword_error");
  const errorConfirmPassword = document.getElementById(
    "confirmNewPassword_error"
  );
  //   check valid username
  if (oldPassword === "") {
    errorOldPassword.textContent = "Mật khẩu cũ không được để trống";
    return false;
  } else {
    errorOldPassword.textContent = "";
  }
  // check valid password
  if (newPassword === "") {
    errorNewPassword.textContent = "Mật khẩu mới không được để trống";
    return false;
  } else {
    errorNewPassword.textContent = "";
  }
  // check valid confirm password
  if (confirmPassword === "") {
    errorConfirmPassword.textContent = "Xác nhận mật khẩu không được để trống";
    return false;
  } else if (confirmPassword !== newPassword) {
    errorConfirmPassword.textContent = "Mật khẩu xác nhận không trùng khớp";
    return false;
  } else {
    errorConfirmPassword.textContent = "";
  }
  form.submit();
};

button.addEventListener("click", validateForm);
