const button = document.getElementById("signup-button");
const validateForm = (event) => {
  event.preventDefault();
  const form = document.getElementById("signup-form");
  const email = form.email.value;
  const errorEmail = document.getElementById("error-email");
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
  form.submit();
};

button.addEventListener("click", validateForm);
