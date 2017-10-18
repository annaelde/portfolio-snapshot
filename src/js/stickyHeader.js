import { isIE } from './detectIE.js'

var header = document.getElementsByTagName('header')[0]
var main = document.getElementsByTagName('main')[0]

// Sticky point after we scroll to the bottom of the header
var stickyPoint = 0
var headerHeight = 0

// Use the correct parseInt function based on the browser
if (!isIE)
    headerHeight = Number.parseInt(
        window.getComputedStyle(header).getPropertyValue('height')
    )
else {
    document.getElementsByTagName('nav')[0].className += ' ie'
    headerHeight = parseInt(
        window
            .getComputedStyle(header)
            .getPropertyValue('height')
            .replace('px', '')
    )
    stickyPoint = 77
}

var stuck = false
window.addEventListener('scroll', stick)

function stick() {
    var scrollDistance = window.pageYOffset
    var hiddenHeight = document.body.clientHeight - window.innerHeight

    // Return if the height is too small
    if (hiddenHeight < headerHeight && !stuck) return

    // If scrolled past a certain point
    if (stickyPoint - scrollDistance <= 0 && !stuck) {
        if (!isIE) {
            header.classList.add('sticky')
            main.classList.add('sticky')
        } else {
            header.className += ' sticky--ie'
            main.className += ' sticky'
        }

        stuck = true
    } else if (stuck && scrollDistance <= stickyPoint) {
        // If scrolled back up
        if (!isIE) {
            header.classList.remove('sticky')
            main.classList.remove('sticky')
        } else {
            header.className = header.className.replace(' sticky--ie', '')
            main.className = main.className.replace(' sticky', '')
        }

        stuck = false
    }
}
