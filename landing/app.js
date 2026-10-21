const form = document.querySelector("#contact-form");
const status = document.querySelector("#form-status");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!form.checkValidity()) {
    status.textContent = "Проверьте, что все поля заполнены корректно.";
    form.reportValidity();
    return;
  }

  status.textContent = "Демо-форма проверена. Для реальной отправки подключается API.";
  form.reset();
});

