export var isIE = detectIE()

function detectIE() {
    return (
        navigator.userAgent.indexOf('Edge') > -1 ||
        navigator.userAgent.indexOf('Trident/7.0') > -1
    )
}

/**
 * Miscellaneous IE Fixes
 */
if (isIE) {
    // Fix nav menu z-index bug
    var menu = document.querySelector('nav ul')
    if (menu) {
        menu.style.zIndex = 7
    }
}
