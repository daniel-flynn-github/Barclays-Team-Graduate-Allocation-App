localStorage.voteCount = {};

function countVotes(team_id) {
    if (localStorage.voteCount[team_id] != undefined) {
        console.log(localStorage.voteCount[team_id]);
        localStorage.voteCount[team_id]++;
    } else {
        console.log(localStorage.voteCount[team_id]);
        localStorage.voteCount[team_id] = 1;
        console.log(localStorage.voteCount[team_id]);
    }

    document.getElementById("voteCount_" + team_id).innerHTML = localStorage.voteCount.team_id;
}