localStorage.setItem("voteCountsObject", "{}");
const MAX_VOTES_PER_TEAM = 5;

function countVotes(team_id) {
    var voteCounts = JSON.parse(localStorage.getItem("voteCountsObject"));

    if (voteCounts[team_id] == null) {
        voteCounts[[team_id]] = 1;
    } else {
        if (voteCounts[team_id] < MAX_VOTES_PER_TEAM) {
            voteCounts[team_id]++;
        } 
        
        if (voteCounts[team_id] == MAX_VOTES_PER_TEAM) {
            document.getElementById("like_btn_team_" + team_id).classList.add("disabled");
        }
    }

    document.getElementById("remove_vote_team_" + team_id).hidden = false;
    document.getElementById("voteCount_" + team_id).innerHTML = voteCounts[team_id];
    localStorage.setItem("voteCountsObject", JSON.stringify(voteCounts));
}

function removeVotes(team_id) {
    var voteCounts = JSON.parse(localStorage.getItem("voteCountsObject"));
    document.getElementById("like_btn_team_" + team_id).classList.remove("disabled");

    if (voteCounts[team_id] > 0) {
        voteCounts[team_id]--;

        if (voteCounts[team_id] == 0) {
            document.getElementById("remove_vote_team_" + team_id).hidden = true;
        }
    }

    document.getElementById("voteCount_" + team_id).innerHTML = voteCounts[team_id];
    localStorage.setItem("voteCountsObject", JSON.stringify(voteCounts));
}

function resetVotes() {
    // When button is clicked:
    //  1. Set votes for each team back to 0
    //  2. Remove the red cross (if its there)
    //  3. Ensure the thumbs up button is there and useable

    var voteCounts = JSON.parse(localStorage.getItem("voteCountsObject"));
    for (const [team_id, votes] of Object.entries(voteCounts)) {
        document.getElementById("voteCount_" + team_id).innerHTML = 0;
        document.getElementById("like_btn_team_" + team_id).classList.remove("disabled");
        document.getElementById("remove_vote_team_" + team_id).hidden = true;
    }

    // Reset the JSON object for votes back to 0
    localStorage.setItem("voteCountsObject", "{}");
}