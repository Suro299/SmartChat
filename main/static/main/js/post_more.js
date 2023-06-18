const post_dop = document.getElementById("post_dop")

let post_dop_window = false;

function OpenPostMoreWindow() {
  if (post_dop_window == false) {
    post_dop.style.display = "flex"
    post_dop_window = true
  
  } else {
    post_dop.style.display = "none"
    post_dop_window = false
  }

}
