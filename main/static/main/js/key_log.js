
document.getElementById("comm_inp").addEventListener('keydown', function(event) {
    if (event.code == 'Enter' && !event.shiftKey) {
      document.getElementById("com_btn").click()
    }
});