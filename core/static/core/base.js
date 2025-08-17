// Create a MediaQueryList object
const mq = window.matchMedia('(max-width: 980px)');
const home = document.getElementById("sidebar-home");
const search = document.getElementsByClassName("sidebar-search");
const messages = document.getElementsByClassName("sidebar-messages");
const logout = document.getElementsByClassName("sidebar-logout");
const login = document.getElementsByClassName("sidebar-login");
const profile = document.getElementsByClassName("sidebar-profile");

// Function to run when media query status changes
function handleViewportChange(e) {
  if (e.matches) {
    // Viewport is 1024px or smaller
    // Update content or styles here
    
  } else {
    // If viewport is more than 1024px
    // Update content or styles here
  }
}

// Initial check
handleViewportChange(mq);

// Listen for changes in viewport size
mq.addEventListener('change', handleViewportChange);
