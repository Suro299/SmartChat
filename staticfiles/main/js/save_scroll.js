window.addEventListener('beforeunload', function() {
    var postsSection = document.getElementById('scrol_section');
    if (postsSection) {
      localStorage.setItem('scrollPosition', postsSection.scrollTop);
    }
  });
  
  window.addEventListener('load', function() {
    var savedScrollPosition = localStorage.getItem('scrollPosition');
    var postsSection = document.getElementById('scrol_section');
    if (savedScrollPosition && postsSection) {
  
      for (let i = 0; i < savedScrollPosition; i++) {
        (function(index) {
          setTimeout(function() {
            console.log(index); 
            postsSection.scrollTop += 1
          }, 07);
        })(i);
      }
      localStorage.removeItem('scrollPosition');
    }
  
  });