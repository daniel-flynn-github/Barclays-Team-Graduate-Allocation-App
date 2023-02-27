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

                            // Then want to add this graduate back to the drop-down
                            $("#select_graduate").append($("<option>", {
                                value: grad_id,
                                text: grad_text,
                            }));
                            $("#add_grad_form").attr('hidden', false);

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
