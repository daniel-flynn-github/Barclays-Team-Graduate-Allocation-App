localStorage.setItem("voteCountsObject", "{}");
const MAX_VOTES_PER_TEAM = 5;

function countVotes(team_id) {
    var voteCounts = JSON.parse(localStorage.getItem("voteCountsObject"));
    console.log(JSON.stringify(voteCounts));

    if (voteCounts[team_id] == null) {
        voteCounts[[team_id]] = 1;
    } else {
        if (voteCounts[team_id] < MAX_VOTES_PER_TEAM) {
            voteCounts[team_id]++;
        } 
        
        if (voteCounts[team_id] == 5) {
            document.getElementById("like_btn_team_" + team_id).classList.add("disabled");
        }
    }

    document.getElementById("voteCount_" + team_id).innerHTML = voteCounts[team_id];

    console.log(JSON.stringify(voteCounts));
    localStorage.setItem("voteCountsObject", JSON.stringify(voteCounts));
}