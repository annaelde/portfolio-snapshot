/** @module loader.js */
import { isIE } from './detectIE.js'

/**
 * Manage script loading and DOM additions. Developed for use with Barba.js.
 * @class
 */
export var Loader = {
    nodes: new Array(),
    /**
     * Loads a script and creates a mutation observer to track DOM changes
     * 
     * @method
     * @param {String} source   The url of the script source.
     * @param {String} id       ID to be given to the new script tag.
     */
    load(source, id) {
        // Return if not online
        if (!navigator.onLine) return

        // Create the DOM node
        var script = document.createElement('script')
        if (id) script.id = id
        script.src = source

        // IE ForEach Polyfill
        if (isIE) {
            ;(function() {
                if (typeof NodeList.prototype.forEach === 'function') return false
                NodeList.prototype.forEach = Array.prototype.forEach
            })()
        }

        // Create a new mutation observer
        var observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                // If a node was added during the mutation, track it
                if (mutation.addedNodes) {
                    mutation.addedNodes.forEach(node => {
                        if (!this.nodes.indexOf(node) >= 0) this.nodes.push(node)
                    })
                }
            })
        })

        var config = {
            attributes: false,
            childList: true,
            characterData: false
        }
        observer.observe(document.head, config)
        observer.observe(document.body, config)
        document.head.appendChild(script)
    },
    /** 
     * Cleans up any DOM changes to prepare for the next view
     * 
     * @method
     * @param {String} namespace A namespace to be set as undefined.
     */
    cleanup(namespace) {
        if (this.nodes) {
            var length = this.nodes.length
            for (var i = 0; i < length; i++) {
                var node = this.nodes.pop()
                if (node.parentNode) node.parentNode.removeChild(node)
            }
        }

        if (namespace) window[namespace] = undefined
    }
}
