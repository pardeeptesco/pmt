async function fetchList(){
    
  
    document.getElementById("popup").style.display = "block";
   
    //Fetching activities from db
     
    let activities = await eel.get_activity_list()();
    var dropdown = document.getElementById("activities");
    console.log(activities.activityList)
    //Clear existing options
    dropdown.innerHTML = '<option value="">Select activity...</option>';
    // var db = openDatabase('trial.db');
    activities.activityList.forEach(function (activity) {
      console.log(activity)
      var option = document.createElement("option");
      option.value = activity.ActivityName; // Use activity ID as option value
      option.text = activity.ActivityName; // Use activity name as option text
      dropdown.appendChild(option);
    });
}

fetchList();

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

  document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault();

    let tasks = [];

    const startDate = new Date(document.getElementById("startDate").value);
    const endDate = new Date(document.getElementById("endDate").value);
    const startTime = document.getElementById("startTime").value;

    const endTime = document.getElementById("endTime").value;

    const activity = document.getElementById("activities").value;
    const today = new Date();
    const detailContainer = document.getElementById("detail");

    //setting time format
    // const timeFormat =
    //   today.toLocaleDateString() === startDateTime.toLocaleDateString()
    //     ? "HH:mm:ss"
    //     : "YYYY DD MM HH:mm:ss";

    

    //pushing selected activity in list of activities

    let task = {
      id:Date.now(), //using timestamp as unique id
      Activity: activity,
      startDate: startDate,
      endDate: endDate,
      startTime: startTime,
      endTime: endTime,
    };
    //inserting into db
    tasks.push(task);

    detailContainer.innerHTML = "Activites";

    //listing all present activites
    listActivities(tasks);

    detailContainer.style.display = "block";

    closePopup();
  });

  //function to list all activities
  function listActivities(tasks) {
    const detailContainer = document.getElementById("detail");
       detailContainer.innerHTML='';
    tasks.forEach(function (act) {
      var activityToInsert = `
       <li class="activity" id="${act.id}">
        <p><strong>Activity:</strong>${act.Activity} &nbsp;&nbsp;<strong>Start:</strong> ${act.startTime} &nbsp;&nbsp;<strong>End:</strong> ${act.endTime} 
            <button class="deleteButton" onclick="deleteActivity(${act.id})">Delete</button></p>
        
    </li>
  `;
      detailContainer.insertAdjacentHTML("beforeend", activityToInsert);
    });
  }

  function deleteActivity(id){
    var deleteButton=document.getElementById(id);
    deleteButton.addEventListener('click',function(){
        var index=tasks.findIndex(function(task){
             return task.id===id;
        })
        tasks.splice(index,1);
        listActivities(tasks)
    })
  }