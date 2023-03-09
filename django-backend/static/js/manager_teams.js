var gradRows = document.querySelectorAll(".grads_in_team");

gradRows.forEach(function(gradRow) {
    gradRow.addEventListener("click", function(event) {
        var gradRowId = gradRow.getAttribute("id");  // gets something like "grad_7"

        if (event.target.classList.contains("delete-btn")) {
            // When the delete (X) button, within the graduate's row, is clicked
            event.preventDefault();


            var xhr = new XMLHttpRequest();
            xhr.open("GET", event.target.href);  // delete the graduate e.g. /delete_team_member/7/
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        if (response.success) {
                            // Remove the <li> containing the grad dynamically
                            var element = document.getElementById(gradRowId);
                            var grad_id = gradRowId.substring(5);
                            var grad_text = $("#grad_text_" + grad_id).text();
                            element.parentNode.parentNode.removeChild(element.parentNode);
                            enable_dropdown();
                            add_to_dropdown(grad_id, grad_text);

                        } else {
                            alert("Failed to delete team member. Please wait seconds and try again.");
                        }
                    } else {
                        alert("Failed to delete team member. Please wait seconds and try again.");
                    }
                }
            };
            xhr.send();
        }
    });
});
function add_to_dropdown(grad_id, grad_text){
    var dropdown = document.querySelectorAll("select#select_graduate");
    dropdown.forEach(function (dropdown){
        var option = document.createElement("option");
        option.value = grad_id;
        option.text = grad_text;
        dropdown.appendChild(option);
});
}

function enable_dropdown() {
    var teamSelects = document.querySelectorAll("form[id^= add_grad_form]");
    teamSelects.forEach(function(teamSelect) {
        teamSelect.hidden = false;
    });
}

function delete_from_dropdown(grad_id){
     $("#select_graduate option[value='" + grad_id + "']").remove();
}

function disable_dropdown(){
    var teamSelects = document.querySelectorAll("form[id^= add_grad_form]");
    teamSelects.forEach(function(teamSelect) {
         if ($("#select_graduate option").length === 0){
             teamSelect.hidden = true;
         }
    });
}

var add_forms = document.querySelectorAll("form[id ^= add_grad_form]");
var team_mem_lists = document.querySelectorAll('ul[id ^= team_member]');


add_forms.forEach(function (add_form){
    add_form.addEventListener('submit', function (event){
        event.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.open('POST', add_form.action);
        xhr.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
        xhr.onload = function(){
            if (xhr.status === 200){
                var select_grad = document.getElementById("select_graduate");
                var grad_id = select_grad.options[select_grad.selectedIndex].value;
                var grad_text = select_grad.options[select_grad.selectedIndex].text;
                var grad_name = grad_text.split('|')[0].trim();
                var grad_email = grad_text.split('|')[1].trim();
                var link = '<a href="/allocation/manager/delete_team_member/' + grad_id + '/';
                var add_form_id = add_form.id.split('_').pop();
                var new_member = document.createElement('li');

                team_mem_lists.forEach(function (team_mem_list){
                    var team_list_id = team_mem_list.id.split('_').pop();
                    if (add_form_id === team_list_id){
                        new_member.innerHTML = '<div class="row grads_in_team" id="grad_' + grad_id + '">' + '<div class="col" id="grad_text_' + grad_id + '">' + grad_name + ' | <a href="mailto:' + grad_email + '">' + grad_email + '</a>' + '</div>' + '<div class="col">' + link + '" class="btn btn-danger delete-btn">&times;</a>' + '</div>' + '</div>';
                        team_mem_list.appendChild(new_member);
                    }
                });
                delete_from_dropdown(grad_id);
                disable_dropdown();

                new_member.querySelector('.delete-btn').addEventListener('click', function (event){
                    event.preventDefault();

                     var xhr = new XMLHttpRequest();
                     xhr.open('GET', event.target.href);
                     xhr.onreadystatechange = function (){
                             if (xhr.status === 200){
                                 var response = JSON.parse(xhr.responseText);
                                 if(response.success){
                                     var element = document.getElementById("grad_" + grad_id);
                                     var delete_text = $('#grad_text_' + grad_id).text();
                                     if(element !== null){
                                          element.parentNode.parentNode.removeChild(element.parentNode);
                                          add_to_dropdown(grad_id, delete_text);
                                     }
                                     enable_dropdown();
                                 }
                                 else {
                                     alert("response failed");
                                 }
                             }
                             else {
                                 alert("status have problem");
                             }
                     }
                     xhr.send();
                });
            }
            else {
                alert("Failed to delete team member. Please wait seconds and try again.");
            }
        }
        xhr.send(new FormData(add_form));
    });
});