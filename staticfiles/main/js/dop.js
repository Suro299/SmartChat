

// Erb vor ejy bacvum a 
window.onload = function() {
  // settings menyun pakum a
  document.getElementById("settings_menu").style.display = "none";
};


//  Lyuboy tex sxmeluc Settings menuen pakvum a 
window.addEventListener("click", function(event) {
  document.getElementById("settings_menu").style.display = "none"
})


// Settings Menyun bacel pakely
function OpenSettingsWindow() {


  event.stopPropagation(); // Esni nra hamar a vor window.addeventlistenery chashxati
  
  const settings_menu = document.getElementById("settings_menu");
  if (settings_menu.style.display == "none") {
    settings_menu.style.display = "flex";
    console.log("Sarqeci flex");
  } else {
    settings_menu.style.display = "none";
    console.log("Pakeci");
  }
}



//  Post sarqeluc vor cuyc ta nkar yntrvac a te che
function ChangeInputLable() {
  const noFile = document.getElementById("noFile")
  noFile.innerText = "File chosen !";
}



//  Vor settingsum avatarkid sxmes u pravadniky bacvi vor nor nkar yntres
function OpenFileSelect() {
  document.getElementById("avatar_input").click();
}


// Vor nor nkar yntreluc miangamic avatarkid texy nor nkary lini
function ChangeAvatar() {
  image = document.getElementById("user_avatar");
  input = document.getElementById('avatar_input');
  image.src = URL.createObjectURL(input.files[0]);
}



