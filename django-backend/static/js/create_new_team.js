const select = document.getElementById("group_department");
const text = document.getElementById("department_text");

  select.addEventListener("change", function() {
    if (select.value === "other") {
      select.style.display = "none";
      text.style.display = "block";
      text.focus();
    } else {
      select.style.display = "block";
      text.style.display = "none";
    }
  });

  text.addEventListener("blur", function() {
    select.style.display = "block";
    text.style.display = "none";
    select.value = "other";
    select.options[select.options.length - 1].text = text.value;
  });