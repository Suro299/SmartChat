const settings_menu = document.getElementById("settings_menu");
const user_btn = document.getElementById("user_btn");
const noFile = document.getElementById("noFile")
const show_activity = document.getElementById("show_activity")


let settings_menu_is_open = false;



function OpenSettingsWindow() {
  if (settings_menu_is_open == false) {
    settings_menu.style.display = "flex"
    settings_menu_is_open = true
  
  } else {
    settings_menu.style.display = "none"
    settings_menu_is_open = false
  }
}

function ChangeInputLable() {
  noFile.innerText = "File chosen !"
}

function OpenFileSelect() {
  document.getElementById("avatar_input").click()
}

function ChangeAvatar() {
  image = document.getElementById("user_avatar")
  input = document.getElementById('avatar_input')
  image.src = URL.createObjectURL(input.files[0])
  
}


function SumbitProfileForm() {
  document.getElementById('submit_button').click();
}


function ShowActivity() {
  console.log()
  if (show_activity.value == "0") {
    activity_polz.style.justifyContent = "end";
    show_activity.value = "1"
    document.getElementById("activity_circ").style.backgroundColor = "green"
  } else {
    activity_polz.style.justifyContent = "start";
    show_activity.value = "0"
    document.getElementById("activity_circ").style.backgroundColor = "#ac1616"
  }
}