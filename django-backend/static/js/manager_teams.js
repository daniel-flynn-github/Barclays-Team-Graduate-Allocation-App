var gradRows = document.querySelectorAll(".grads_in_team");

gradRows.forEach(function(gradRow) {
    gradRow.addEventListener("click", function(event) {
        var gradRowId = gradRow.getAttribute("id");  // gets something like "grad_7"

        if (event.target.classList.contains("delete-btn")) {
            // When the delete (X) button, within the graduate's row, is clicked
            event.preventDefault();
            event.stopPropagation();

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

                            // Then want to add this graduate back to the drop-down IN ALL TEAMS!
                            var addGradForms = document.getElementsByClassName('add_grad_forms');
                            for (i=0; i < addGradForms.length; i++) {
                                $(".add_grad_forms").eq(i).attr("hidden", false);
                            }
                          
                            $(".select_graduate_forms").each(function() {
                                $(this).append($("<option>", {
                                  value: grad_id,
                                  text: grad_text,
                                }));
                            });
                        } else {
                            alert("Failed to delete team member. Please wait a few seconds and try again.");
                        }
                    } else {
                        alert("Failed to delete team member. Please wait a few seconds and try again.");
                    }
                }
            };
            xhr.send();
        }
    });
});

var addGradForms = document.getElementsByClassName('add_grad_forms');

for (i=0; i < addGradForms.length; i++) {
    const thisForm = addGradForms[i];
    const selected_grad = document.getElementsByClassName("select_graduate_forms")[i];
    const teamMembers = document.getElementsByClassName('team_members_in_each_team')[i];
    const selected_grad_form = $(".select_graduate_forms").eq(i);
    const thisFormjQuery = $(".add_grad_form")[i];

    thisForm.addEventListener('submit', function(event) {
        event.preventDefault(); // prevent default form submission
        var xhr = new XMLHttpRequest();
        
        xhr.open('POST', thisForm.action);
        xhr.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[i].value); // add CSRF token
        xhr.onload = function() {
            if (xhr.status === 200) {
                var newMemberItem = document.createElement('li');
                var grad_id = selected_grad.options[selected_grad.selectedIndex].value;
                var grad_text = selected_grad.options[selected_grad.selectedIndex].text;
                var name = grad_text.split('|')[0].trim();
                var email = grad_text.split('|')[1].trim();
                var url = grad_id + '/';
                var link = '<a href="/allocation/manager/delete_team_member/' + url;

                newMemberItem.innerHTML = '<div class="row grads_in_team" id="grad_' + grad_id + '">' + '<div class="col" id="grad_text_' + grad_id + '">' + name  + ' | <a href="mailto:' + email + '">' + email + '</a>' + '</div>' + '<div class="col">' + link + '" class="btn btn-danger delete-btn">&times;</a>' + '</div>' + '</div>';
                var teamMemberList = teamMembers.querySelector('ul');
                teamMemberList.appendChild(newMemberItem);

                $(".select_graduate_forms option[value='" + grad_id + "']").remove();

                if (selected_grad_form.find("option").length === 0) {
                    // Hide all add_grad forms
                    for (j=0; j < addGradForms.length; j++) {
                        $(".add_grad_forms").eq(j).attr("hidden", true);
                    }
                }

                newMemberItem.querySelector(".delete-btn").addEventListener("click", function(event) {
                    event.preventDefault();
                    event.stopPropagation();

                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", event.target.href);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 200) {
                                var response = JSON.parse(xhr.responseText);
                                if (response.success) {
                                    var element = document.getElementById("grad_" + grad_id);
                                    var grad_text = $("#grad_text_" + grad_id).text();
                                    element.parentNode.parentNode.removeChild(element.parentNode);
                                    thisFormjQuery.attr('hidden', false);
                                    selected_grad.appendChild($("<option>", {
                                        value: grad_id,
                                        text: grad_text,
                                    }));
                                } else {
                                    alert("Failed to delete team member. Please wait seconds and try again.");
                                }
                            } else {
                                alert("Failed to delete team member. Please wait seconds and try again.");
                            }
                        }
                    };
                    xhr.send();
                });
            } else {
                alert("Failed to add team member. Please wait seconds and try again.");
            }
        };
        xhr.send(new FormData(thisForm));
    });
}