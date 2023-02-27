var gradRows = document.querySelectorAll(".row");

gradRows.forEach(function(gradRow) {
    gradRow.addEventListener("click", function(event) {
        var gradRowId = gradRow.getAttribute("id");

        if (event.target.classList.contains("delete-btn")) {
            event.preventDefault();

            var deleteBtn = event.target;
            deleteBtn.disabled = true;

            var xhr = new XMLHttpRequest();
            xhr.open("GET", event.target.href);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    deleteBtn.disabled = false;
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        if (response.success) {
                            // 删除成功，移除对应的 HTML 元素
                            var element = document.getElementById(gradRowId);
                            element.parentNode.removeChild(element);
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
