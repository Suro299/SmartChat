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



