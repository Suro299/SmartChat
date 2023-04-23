const settings_window = document.getElementById("settings_window");

const user_button = document.getElementById("user_button");

let settings_window_is_open = false;

user_button.addEventListener("click", open_close_settings_window);;

function open_close_settings_window() {
  if (settings_window_is_open == false) {
    settings_window.style.right = "4rem"
    settings_window_is_open = true
  } else {
    settings_window.style.right = "-30rem"
    settings_window_is_open = false
  }
}
