var element = document.getElementById("message_div");
element.scrollTop = element.scrollHeight;



window.onload = function() {
  close_all_cont_menues()
};




document.getElementById("send_message").addEventListener('keydown', function(event) {
  if (event.code == 'Enter' && !event.shiftKey) {
    document.getElementById("send_message_btn").click()
  }
});



// Soombshenyaneeri Kontekst mneyui bacelu u pakelu hamar
function open_message_context_menu(id) {
  const context_menu = document.getElementById(id);
  event.preventDefault();

  if (context_menu.style.display != "none") {
    context_menu.style.display = "none";
    context_menu.style.width = "0";
    context_menu.style.opacity = "0";
  } else {
    close_all_cont_menues();

    if (window.getComputedStyle(context_menu.parentNode).alignItems == "start") {
      context_menu.style.top = parseFloat(event.clientY) - 60 + "px";
      context_menu.style.left = parseFloat(event.clientX) + 50 + "px";
    } else {
      context_menu.style.top = parseFloat(event.clientY) - 130 + "px";
      context_menu.style.left = parseFloat(event.clientX) - 100 + "px";
    }
    
    increase_context_menu_width(context_menu);
  }
}


// Context Menyui animacian BACVELUC
function increase_context_menu_width(element) {
  element.style.display = "flex";
  let width = parseFloat(element.style.width);
  let computedStyle = getComputedStyle(element);
  let opacity = parseFloat(computedStyle.opacity);

  let i = 0;
  function increase() {
    element.style.transition = "width 0.2s, opacity 0.4s";
    element.style.width = width + i + "rem";
    
    element.style.opacity = String(opacity + (i / 20))


    i++;
    if (i <= 20) {
      setTimeout(increase, 1);
    }
  }

  increase();
}


// sax bacac context menyunery pakum a
window.addEventListener("click", close_all_cont_menues);
window.addEventListener("touchstart", close_all_cont_menues);

function close_all_cont_menues() {
    const cont_menues = document.getElementsByClassName("message_context_menu");
    
    for (let i = 0; i < cont_menues.length; i++) {
      cont_menues[i].style.display = "none";
      cont_menues[i].style.width = "0";
      cont_menues[i].style.opacity = "0";
    }
}


// Context menyun a heraxosneri vra bacum pakum 
var buttons = document.querySelectorAll(".message");
var isTouchDown = false;
var touchXStart = 0;

buttons.forEach(function(button) {
  var isTouchDown = false;
  var touchXStart = 0;

  button.addEventListener("touchstart", function(event) {
    isTouchDown = true;
    touchXStart = event.touches[0].clientX;
  });

  button.addEventListener("touchend", function(event) {
    isTouchDown = false;
    button.style.marginLeft = 0 + "px";
  });

  button.addEventListener("touchmove", function(event) {
    if (isTouchDown) {
        var margin_left = parseFloat(window.getComputedStyle(button).marginLeft);
        var touchXCurrent = event.touches[0].clientX;
        if (margin_left < 80 && margin_left > -1) {
          button.style.marginLeft = (touchXCurrent - touchXStart) + "px";
        }

        if (margin_left > 80) {
          isTouchDown = false;
          button.style.marginLeft = 0 + "px";

          var contextMenu = button.parentNode.querySelector(".message_context_menu");

          if (contextMenu.style.display === "none") {
                open_message_context_menu(contextMenu.id)
                contextMenu.style.position = "relative"
                contextMenu.style.marginBottom = "-20px";
                contextMenu.style.backgroundColor = "#1f1f1f" 

                if (window.getComputedStyle(contextMenu.parentNode).alignItems == "start") {
                    contextMenu.style.marginLeft = "30px";
                } else {
                    contextMenu.style.marginRight = "30px";
                }
          }
        }
    }
  });
});


// Message-i copy-n
function copy_text(id) {
    event.preventDefault();
    
    const message_text = document.getElementById("message_text_" + id)

    var range = document.createRange();
    range.selectNode(message_text);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();

}


// function close_edit_text() {
//     event.preventDefault();
//     const cont_menues = document.getElementsByClassName("message");
    
//     for (let i = 0; i < cont_menues.length; i++) {
//       cont_menues[i].style.border = "none"
//     }
// }




// Reply Section-i animacian BACVELUC
function increase_reply_section_height(element) {
  element.style.display = "flex";
  let height = parseFloat(element.style.height);
  let computedStyle = getComputedStyle(element);
  let opacity = parseFloat(computedStyle.opacity);

  let i = 0;
  function increase() {
    element.style.transition = "height 0.05s, opacity 0.1s";
    element.style.height = height + i + "%";
    
    element.style.opacity = String(opacity + (i / 40))

    i++;
    if (i <= 40) {
      setTimeout(increase, 1);
    }
  }

  increase();
}


// Replynery 
function reply_msg(id) {
  event.preventDefault();
  
  
  const username = document.getElementById("message_sender_username_" + id)
  const message_text = document.getElementById("message_text_" + id)

  const reply_section = document.getElementById("reply_section")
  const reply_username = document.getElementById("reply_username")
  const reply_message = document.getElementById("reply_message")
  const reply_message_id  = document.getElementById("reply_message_id")

  reply_message_id.value = id


  if (message_text.innerText.length <= 50) {
    reply_message.innerText = message_text.innerText
  } else {
    reply_message.innerText = message_text.innerText.substring(0, 50) + "..."
  }
  reply_username.innerText = username.value
  
  increase_reply_section_height(reply_section)

}


// Reply-i patuhany pakum a 
document.getElementById("reply_close_btn").addEventListener("click", function() {
  event.preventDefault();
  const reply_section = document.getElementById("reply_section")
  reply_section.style.display = "none"
  reply_section.style.opacity = "0"
  reply_section.style.height = "0%"
  document.getElementById("reply_message_id").value = ""

})



function close_user_forward(){
  document.getElementById("user_for_forward").style.display = "none"
}




// Forward-y
function forward(id) {
  event.preventDefault();

  document.getElementById("user_for_forward").style.display = "flex"
  document.getElementById("forwarding_id").value = id;
}


function close_forward_window() {
  document.getElementById("user_for_forward").style.display = "none"
  document.getElementById("forwarding_id").value = "";
}