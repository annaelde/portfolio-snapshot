var menuIcon = document.getElementById('menu-icon')
var nav = document.getElementsByTagName('nav')[0]
var ul = nav.getElementsByTagName('ul')[0]
var open = false

// Remove noscript help text from menu icon
menuIcon.title = ''

// Add on-click for hamburger icon
menuIcon.addEventListener('click', toggleDrawer)

// Add on-click for clicking outside menu
document.addEventListener('click', function(event) {
    var clickOut = !nav.contains(event.target)
    if (clickOut && open) toggleDrawer()
})

// Add on-touch for touching outside menu
document.addEventListener('touchstart', function(event) {
    var clickOut = !nav.contains(event.target)
    if (clickOut && open) toggleDrawer()
})

// Add on-keyup for esc key
document.addEventListener('keyup', function(event) {
    if (event.keyCode == 27 && open) toggleDrawer()
})

// Toggle the drawer
function toggleDrawer() {
    if (open) {
        menuIcon.classList.remove('open')
        nav.classList.remove('open')
        open = false
    } else {
        menuIcon.classList.add('open')
        nav.classList.add('open')
        open = true
    }
}
