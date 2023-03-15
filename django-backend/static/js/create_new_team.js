//department
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

//skills
  $(document).ready(function() {
  var select = $('#group_skills');
  var input = $('#skill_text');
  var prevValues = [];

  select.on('change.bs.select', function(e, clickedIndex, isSelected, previousValue) {
    if (select.val() && select.val().includes('add')) {
      select.selectpicker('hide');
      input.show().focus();

      input.on('blur', function(event) {
        var new_skill = $(this).val().trim();
        if (new_skill) {
          select.append('<option value="' + new_skill + '">' + new_skill + '</option>');
          select.selectpicker('refresh');
        }
        $(this).hide().val('');
        select.selectpicker('show');

        if (prevValues.length > 0) {
          var index = prevValues.indexOf('add');
          if (index !== -1) {
            prevValues.splice(index, 1);
            }
          prevValues.push(new_skill);
          select.selectpicker('val', prevValues);
          prevValues = [];
        }
      });
      prevValues = select.val();
    }
  });
});

  //technologies
$(document).ready(function() {
  var t_select = $('#group_technologies');
  var t_input = $('#technologies_text');
  var t_prevValues = [];

  t_select.on('change.bs.select', function(e, clickedIndex, isSelected, previousValue) {
    if (t_select.val() && t_select.val().includes('add')) {
      t_select.selectpicker('hide');
      t_input.show().focus();

      t_input.on('blur', function(event) {
        var new_tech = $(this).val().trim();
        if (new_tech) {
          t_select.append('<option value="' + new_tech + '">' + new_tech + '</option>');
          t_select.selectpicker('refresh');
        }
        $(this).hide().val('');
        t_select.selectpicker('show');

        if (t_prevValues.length > 0) {
          var index = t_prevValues.indexOf('add');
          if (index !== -1) {
            t_prevValues.splice(index, 1);
            }
          t_prevValues.push(new_tech);
          t_select.selectpicker('val', t_prevValues);
          t_prevValues = [];
        }
      });
      t_prevValues = t_select.val();
    }
  });
});