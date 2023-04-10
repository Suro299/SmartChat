const settings_window = document.getElementById("settings_window");
const footer = document.getElementById("footer");

const footer_button_div = document.getElementById("footer_button_div")
const user_button = document.getElementById("user_button");
const footer_button = document.getElementById("footer_button");

let settings_window_is_open = false;


user_button.addEventListener("click", open_close_settings_window);;
footer_button.addEventListener("click", opne_close_footer);

function open_close_settings_window() {
  if (settings_window_is_open == false) {
    settings_window.style.right = "4rem"
    settings_window_is_open = true
  } else {
    settings_window.style.right = "-30rem"
    settings_window_is_open = false
  }
}


function opne_close_footer() {
  if (footer_button.innerText == "⇡") {
    footer_button_div.style.bottom = "-0.5vh"
    footer.style.height = "7vh"
    footer_button.innerText = "⇣"
  } else {
    footer_button_div.style.bottom = "5.5vh"
    footer.style.height = "0vh"
    footer_button.innerText = "⇡"
  }
}
