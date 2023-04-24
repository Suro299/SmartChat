const settings_menu = document.getElementById("settings_menu");
const user_btn = document.getElementById("user_btn");

let settings_menu_is_open = false;

user_btn.addEventListener("click", open_close_settings_window);

function open_close_settings_window() {
  console.log("ASDASDASDASDSADads");
  if (settings_menu_is_open == false) {
    settings_menu.style.display = "flex"
    settings_menu_is_open = true
  
  } else {
    settings_menu.style.display = "none"
    settings_menu_is_open = false
  }

}
