'use strict'

import { default as Cookies, cookie, setCookie } from './cookies.js'
import { isIE } from './detectIE.js'

/**
 * A toggle box object.
 * 
 * @param {String} id               Used for cookie naming.
 * @param {Object} wrapper          Outer div element
 * @param {Object} button           Button to toggle open/closed
 * @param {Object} toggle           Animated toggle SVG
 * @param {Object} inner            Div element that toggles.
 * @param {String} innerHeight      Height of inner div element.
 * @param {String} innerHeightIE    Alternate height for IE. Default is 300px
 * @param {Boolean} open            Div toggle state.
 * @param {Boolean} ready           Toggle ready state.
 */
export var ToggleBox = {
    id: '',
    wrapper: null,
    button: null,
    toggle: null,
    inner: null,
    innerHeight: '0',
    innerPadding: '0',
    open: false,
    ready: true,
    init() {
        // Get info from cookie
        if (cookie[this.id]) {
            this.open = cookie[this.id]
        } else {
            setCookie(this.id, this.open)
        }

        // Add event listener for button press
        this.button.style.display = ''
        this.button.addEventListener('click', () => {
            if (this.ready) {
                this.ready = false
                if (this.open) this.closeBox()
                else this.openBox()
            }
        })

        // Set padding
        this.innerPadding = 34

        // Calculate height of the inner list
        this.innerHeight = this.inner.scrollHeight + this.innerPadding + 'px'

        // Add event listener for resize
        window.addEventListener('resize', () => {
            this.inner.style.maxHeight = ''
            this.innerHeight = this.inner.scrollHeight + this.innerPadding + 'px'
            if (this.open) this.inner.style.maxHeight = this.innerHeight
            else {
                this.inner.style.maxHeight = '0'
                this.inner.style.paddingTop = '0'
                this.inner.style.paddingBottom = '0'
            }
        })
        ;(() => {
            if (!this.open) {
                this.inner.style.maxHeight = '0'
                this.inner.style.paddingTop = '0'
                this.inner.style.paddingBottom = '0'
                this.toggle.setAttribute('transform', 'translate(0 0)')
            } else {
                this.inner.style.paddingTop = this.innerPadding / 2 + 'px'
                this.inner.style.paddingBottom = this.innerPadding / 2 + 'px'
                this.innerHeight = this.inner.scrollHeight + this.innerPadding + 'px'
                this.inner.style.maxHeight = this.innerHeight
            }

            setTimeout(() => {
                this.inner.style.transition = 'max-height .3s ease-in-out, padding .3s ease-in-out'
            }, 500)
        })()
    },
    openBox() {
        this.inner.style.paddingTop = this.innerPadding / 2 + 'px'
        this.inner.style.paddingBottom = this.innerPadding / 2 + 'px'
        this.innerHeight = this.inner.scrollHeight + this.innerPadding + 'px'

        this.inner.style.maxHeight = this.innerHeight

        this.toggle.setAttribute('transform', 'translate(8 0)')

        setTimeout(() => {
            this.ready = true
        }, 400)

        this.open = true
        setCookie(this.id, true)
    },
    closeBox() {
        this.inner.style.maxHeight = '0'
        this.inner.style.paddingTop = '0'
        this.inner.style.paddingBottom = '0'

        this.toggle.setAttribute('transform', 'translate(0 0)')

        setTimeout(() => {
            this.ready = true
        }, 400)

        this.open = false
        setCookie(this.id, false)
    }
}
