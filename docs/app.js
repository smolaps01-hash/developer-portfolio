const year = document.getElementById("year");
const form = document.getElementById("brief-form");
const output = document.getElementById("brief-output");
const status = document.getElementById("brief-status");
const copyButton = document.getElementById("copy-brief");

year.textContent = new Date().getFullYear();

function value(id, fallback) {
  const text = document.getElementById(id).value.trim();
  return text || fallback;
}

function buildBrief() {
  const type = document.getElementById("project-type").value;
  const current = value("current-state", "пока не описано");
  const result = value("desired-result", "пока не описано");
  const deadline = value("deadline", "нужно обсудить");
  const budget = value("budget", "нужно обсудить");
  output.value = [
    "Здравствуйте! Хочу обсудить задачу.", "", `Тип: ${type}`,
    `Что есть сейчас: ${current}`, `Нужный результат: ${result}`,
    `Желаемый срок: ${deadline}`, `Ориентир по бюджету: ${budget}`, "",
    "Для оценки могу предоставить обезличенный пример без паролей и персональных данных."
  ].join("\n");
}

async function copyBrief() {
  const required = ["current-state", "desired-result"];
  const missing = required.find((id) => !document.getElementById(id).value.trim());
  if (missing) {
    document.getElementById(missing).focus();
    status.textContent = "Заполните два обязательных поля, чтобы заявка была полезной.";
    status.classList.remove("success");
    return;
  }
  try { await navigator.clipboard.writeText(output.value); }
  catch (error) { output.focus(); output.select(); document.execCommand("copy"); }
  status.textContent = "Заявка скопирована. Отправьте её в чате или на площадке, где нашли портфолио.";
  status.classList.add("success");
  copyButton.textContent = "Скопировано ✓";
  window.setTimeout(() => { copyButton.textContent = "Скопировать заявку"; }, 2400);
}

form.addEventListener("input", buildBrief);
copyButton.addEventListener("click", copyBrief);
buildBrief();
