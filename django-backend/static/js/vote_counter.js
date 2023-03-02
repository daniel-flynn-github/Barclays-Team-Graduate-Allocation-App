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
    pluralize(team_id);
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
    pluralize(team_id);
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

        // Reset the JSON object for votes back to 0
        voteCounts[team_id] = 0;
        localStorage.setItem('voteCountsObject', JSON.stringify(voteCounts))
        pluralize(team_id);
    }
}

function pluralize(team_id) {
    // Runs everytime a vote is added of removed
    // Changes the text to "vote" or "votes" as needed
    var voteCounts = JSON.parse(localStorage.getItem("voteCountsObject"));
    if (voteCounts[team_id] == 1) {
        document.getElementById("vote_text_" + team_id).innerHTML = 'vote';
    } else {
        document.getElementById("vote_text_" + team_id).innerHTML = 'votes';
    }
}

function setStateOnLoad() {
    // Run this on page load -- allows for votes state to be reflected in the JS layer.
    // Use this incase user goes to EDIT their PREFILLED votes.
    all_team_votes = document.getElementsByClassName("vote_count_value");
    cached_votes = JSON.parse(localStorage.getItem("voteCountsObject"));

    // For each team...
    for (i=0; i < all_team_votes.length; i++) {
        team_id = all_team_votes[i].id.substring(10);
        number_of_votes = all_team_votes[i].innerHTML
        cached_votes[team_id] = number_of_votes;

        if (number_of_votes == 5) {
            // Like button disabled, ensure dislike button is shown.
            document.getElementById("like_btn_team_" + team_id).classList.add("disabled");
            document.getElementById("remove_vote_team_" + team_id).hidden = false;
        } else if (number_of_votes > 0) {
            // Both the like & dislike buttons are active.
            document.getElementById("remove_vote_team_" + team_id).hidden = false;
        } else {
            // The dislike button is not shown, ensure like button is enabled.
            document.getElementById("like_btn_team_" + team_id).classList.remove("disabled");
            document.getElementById("remove_vote_team_" + team_id).hidden = true;
        }
    }

    localStorage.setItem('voteCountsObject', JSON.stringify(cached_votes))
}

setStateOnLoad();