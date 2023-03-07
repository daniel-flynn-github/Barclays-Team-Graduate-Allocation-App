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

                            // Then want to add this graduate back to the drop-down
                            $("#add_grad_form").attr('hidden', false);
                            $("#select_graduate").append($("<option>", {
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
        }
    });
});

var addForm = document.getElementById('add_grad_form');
var teamMemberList = document.getElementById('team_members').querySelector('ul');

addForm.addEventListener('submit', function(event) {
    event.preventDefault(); // prevent default form submission

    var xhr = new XMLHttpRequest();
    xhr.open('POST', addForm.action);
    xhr.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[0].value); // add CSRF token
    xhr.onload = function() {
        if (xhr.status === 200) {
            var newMemberItem = document.createElement('li');
            var selected_grad = document.getElementById("select_graduate");
            var grad_id = selected_grad.options[selected_grad.selectedIndex].value;
            var grad_text = selected_grad.options[selected_grad.selectedIndex].text;
            var name = grad_text.split('|')[0].trim();
            var email = grad_text.split('|')[1].trim();
            var url = grad_id + '/';
            var link = '<a href="/allocation/manager/delete_team_member/' + url;

            newMemberItem.innerHTML = '<div class="row grads_in_team" id="grad_' + grad_id + '">' + '<div class="col" id="grad_text_' + grad_id + '">' + name  + ' | <a href="mailto:' + email + '">' + email + '</a>' + '</div>' + '<div class="col">' + link + '" class="btn btn-danger delete-btn">&times;</a>' + '</div>' + '</div>';
            teamMemberList.appendChild(newMemberItem);
            $("#select_graduate option[value='" + grad_id + "']").remove();
            if ($("#select_graduate option").length === 0) {
                $("#add_grad_form").attr("hidden", true);
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
                                $("#add_grad_form").attr('hidden', false);
                                $("#select_graduate").append($("<option>", {
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
    xhr.send(new FormData(addForm));
});