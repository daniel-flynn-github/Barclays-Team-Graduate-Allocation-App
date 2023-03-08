function addSkill(team_id) {
    // Given a team, add the skill to the team/overall team DB.
    skills_input = document.getElementById("new_skill_textbox");
    if (skills_input.value != "") {
        // There is a skill to be added.
        return window.location.href = "/allocation/manager/edit_team/" + team_id + "/add_skill/" + skills_input.value;
    }
}

function addTech(team_id) {
    // Given a team, add the technology to the team/overall team DB.
    tech_input = document.getElementById("new_tech_textbox");
    if (tech_input.value != "") {
        // There is a technology to be added
        return window.location.href = "/allocation/manager/edit_team/" + team_id + "/add_technology/" + tech_input.value;
    }
}

function checkInput(name) {
    var input = document.getElementById("new_" + name + "_textbox");
    var button = document.getElementById(name + "_btn");

    if (input.value.length > 0) {
        button.classList.remove('disabled');
    } else {
        button.classList.add('disabled');
    }
}