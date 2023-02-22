function addSkill(team_id) {
    // Given a team, add the skill to the team/overall team DB.
    skills_input = document.getElementById("new_skill_textbox");
    console.log("hey");

    if (skills_input.value != "") {
        // There is a skill to be added
        console.log("ayyy");
        return window.location.href = "/allocation/manager/edit_team/add_skill/" + team_id + "/" + skills_input.value;
    }
}