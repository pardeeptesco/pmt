function pause() {
    var startBtn = document.querySelector('.start.btn');
    var pauseBtn = document.querySelector('.pause.btn');

    startBtn.disabled = false;
    startBtn.classList.remove('disabled');
    pauseBtn.disabled = true;
    pauseBtn.classList.add('disabled');
}

async function pauseActivity(){
    // pause_activity_entry_to_table
    const activityDropdown = document.getElementById('activity');
    const selectedActivity = activityDropdown.value;
    await eel.pause_activity_entry_to_table(selectedActivity)();
    await fetchActivities();

}

async function stopActivity(){
    const activityDropdown = document.getElementById('activity');
    const selectedActivity = activityDropdown.value;
    const volumeInput = document.getElementById('inputVolume');
    const volume = volumeInput.value;
    await eel.stop_activity_entry_to_table(selectedActivity, volume)();
    await fetchActivities();
    var startBtn = document.querySelector('.start.btn');
    startBtn.disabled = false;
    startBtn.classList.remove('disabled');
    var pauseBtn = document.querySelector('.pause.btn');
    pauseBtn.disabled = true;
    pauseBtn.classList.add('disabled');
    stop();
}


function stop() {
    // var startBtn = document.querySelector('.start.btn');
    var end = document.querySelector('.end');

    // startBtn.disabled = false;
    // startBtn.classList.remove('disabled');
    end.disabled = true;
    end.classList.add('disabled');
}

document.querySelector('.start.btn').addEventListener('click', start);
document.querySelector('.pause.btn').addEventListener('click', pause);


async function populateDropdown() {
    const activityDropdown = document.getElementById('activity');
    const options = await eel.fetch_activity_options()();
    options.forEach(option => {
        let opt = document.createElement('option');
        opt.value = option;
        opt.innerHTML = option;
        activityDropdown.appendChild(opt);
    });
}

populateDropdown(); // fetch drop down list from backend
pause(); // intial pause button disabled
stop(); // intial end button disable

async function fetchActivities(){
    const activeActivities = await eel.fetch_active_activities_from_db()();
    const tableBody = document.getElementById('activeActivities');
    tableBody.innerHTML = '';
    activeActivities.forEach(activity => {
        // console.log(activity[0],activity[1],activity[2],activity[3], activity[4], activity[5], activity[6])
        let row = tableBody.insertRow();
        let activityName = row.insertCell(0);
        let startTime = row.insertCell(1);
        let breakPoint = row.insertCell(2);
        let endTime = row.insertCell(3);
        let totalTime = row.insertCell(4);
        let pause = row.insertCell(5);
        let volume = row.insertCell(6);

        activityName.innerHTML = activity[1];
        startTime.innerHTML = unixTimestampToDateTime(activity[2]);
        breakPoint.innerHTML =  "-";
        endTime.innerHTML = activity[3] === 0 ? "-" :  unixTimestampToDateTime(activity[3]);
        totalTime.innerHTML = secondsToHms(activity[4]);

        let status = null;
        if(activity[5] == 0){
            status = "started";
        }else if(activity[5] == 1){
            status = "paused"
        }else if(activity[5] == 2){
            status = "stopped"
        }
        else{
            status = "n/a"
        }
        pause.innerHTML = status;
        volume.innerHTML = activity[6]

    });
}

fetchActivities(); // fetch all activites for intial loads


async function start() {
    const activityDropdown = document.getElementById('activity');
    const selectedActivity = activityDropdown.value;
    if(selectedActivity){
        await eel.add_activity_entry_to_table(selectedActivity)();
        await fetchActivities();
        var startBtn = document.querySelector('.start.btn');
        var pauseBtn = document.querySelector('.pause.btn');
        var endButton = document.querySelector('.end.btn');

        startBtn.disabled = true;
        startBtn.classList.add('disabled');
        pauseBtn.disabled = false;
        pauseBtn.classList.remove('disabled');
        endButton.disabled = false;
        endButton.classList.remove('disabled');
    }else{
        console.log("Please select activity first")
    }
}


function unixTimestampToDateTime(timestamp) {
    let date = new Date(timestamp * 1000);
    return date.toLocaleString();
}

function secondsToHms(d) {
    d = Number(d);
    let h = Math.floor(d / 3600);
    let m = Math.floor(d % 3600 / 60);
    let s = Math.floor(d % 3600 % 60);

    let hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " h, ") : "";
    let mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " m, ") : "";
    let sDisplay = s > 0 ? s + (s == 1 ? " second" : " s") : "";
    return hDisplay + mDisplay + sDisplay; 
}